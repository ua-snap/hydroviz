<script setup lang="ts">
const { $L } = useNuxtApp()
import { useStreamSegmentStore } from '~/stores/streamSegment'
import { fetchAndAddSegmentsByBounds, fetchSegmentById } from '~/utils/map'
const streamSegmentStore = useStreamSegmentStore()
let { isLoading, segmentRegion, segmentId } = storeToRefs(streamSegmentStore)
let map: any = null
const mapReady = ref(false)

// Set maxBounds to a large square around current map viewport.
const setMapMaxBounds = () => {
  let bounds = map.getBounds()
  let sw = bounds.getSouthWest()
  let ne = bounds.getNorthEast()
  let latPadding = (ne.lat - sw.lat) * 2
  let lngPadding = (ne.lng - sw.lng) * 1
  let paddedBounds = $L.latLngBounds(
    [sw.lat - latPadding, sw.lng - lngPadding],
    [ne.lat + latPadding, ne.lng + lngPadding]
  )
  map.setMaxBounds(paddedBounds)
}

const initializeMap = async () => {
  if (!segmentId.value) {
    const route = useRoute()
    segmentId.value = parseInt(route.params.segment)
  }

  map = $L.map('report-map', {
    scrollWheelZoom: false,
    zoomControl: false,
    doubleClickZoom: false,
    zoomSnap: 0.1,
  })

  let maxZoom = segmentRegion.value === 'alaska' ? 12 : 13

  $L.tileLayer(
    'https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}',
    {
      maxZoom: maxZoom,
      attribution: 'Map data © USGS',
      opacity: 0.75,
    }
  ).addTo(map)

  // Fetch the selected segment before giving the map its first view, so the
  // only tiles ever requested are for the segment's own location: setting a
  // default view here and moving it after the segment arrived made the map
  // visibly jump to the right place.
  let segmentBounds: any = null
  try {
    const segmentData = await fetchSegmentById({ segmentId: segmentId.value })
    segmentBounds = $L.geoJSON(segmentData).getBounds()
  } catch (error) {
    console.error('Error fetching selected segment:', error)
  }

  if (segmentBounds?.isValid()) {
    map.fitBounds(segmentBounds, { padding: [50, 50] })
  } else {
    // Segment fetch failed or returned no geometry: show the whole region.
    let regionCenter =
      segmentRegion.value === 'alaska' ? [64.2, -152.0] : [37.8, -96]
    map.setView(regionCenter, 4)
  }

  setMapMaxBounds()

  await fetchAndAddSegmentsByBounds({
    map,
    $L,
    fitBounds: false,
    mapType: 'report',
  })

  mapReady.value = true

  map.on('moveend', function (e) {
    fetchAndAddSegmentsByBounds({
      map,
      $L,
      fitBounds: false,
      mapType: 'report',
    })
  })
}

watch(isLoading, (newValue, oldValue) => {
  if (oldValue === true && newValue === false && map === null) {
    initializeMap()
  }
})

onMounted(() => {
  if (isLoading.value) return
  initializeMap()
})
</script>

<template>
  <p class="is-size-5 mb-2">
    <span
      class="outflow-legend-swatch"
      :style="{ backgroundColor: outletRed }"
      aria-hidden="true"
    ></span>
    Watershed outflow segments in the map below are shown in red.
  </p>
  <div class="report-map-wrapper mb-6">
    <div id="report-map"></div>
    <MapLoadingOverlay v-if="!mapReady">Loading map&hellip;</MapLoadingOverlay>
  </div>
</template>

<style lang="scss" scoped>
.report-map-wrapper {
  position: relative;
}

#report-map {
  height: 60vh;
<style lang="scss">
.outflow-legend-swatch {
  display: inline-block;
  width: 0.8em;
  height: 0.8em;
}
</style>
