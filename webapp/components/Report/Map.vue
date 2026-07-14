<script setup lang="ts">
const { $L } = useNuxtApp()
import { useStreamSegmentStore } from '~/stores/streamSegment'
import { fetchAndAddSegmentsByBounds, outletRed } from '~/utils/map'
const streamSegmentStore = useStreamSegmentStore()
let { isLoading, segmentRegion, segmentId } = storeToRefs(streamSegmentStore)
let map: any = null

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

const addSegment = async () => {
  if (!segmentId.value) {
    const route = useRoute()
    const id = computed(() => parseInt(route.params.segment))
    segmentId.value = id.value
  }

  if (isLoading.value) return

  await fetchAndAddSegmentsByBounds({
    map,
    $L,
    fitBounds: true,
    mapType: 'report',
  })

  setMapMaxBounds()
}

const initializeMap = () => {
  map = $L
    .map('report-map', {
      scrollWheelZoom: false,
      zoomControl: false,
      doubleClickZoom: false,
      zoomSnap: 0.1,
    })
    .setView([37.8, -96], 8)

  let maxZoom = segmentRegion.value === 'alaska' ? 12 : 13

  $L.tileLayer(
    'https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}',
    {
      maxZoom: maxZoom,
      attribution: 'Map data © USGS',
      opacity: 0.75,
    }
  ).addTo(map)

  addSegment()

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
  <div id="report-map" style="height: 400px" class="mb-6"></div>
</template>

<style lang="scss">
.outflow-legend-swatch {
  display: inline-block;
  width: 0.8em;
  height: 0.8em;
}
</style>
