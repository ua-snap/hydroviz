<script setup lang="ts">
const { $L, $config } = useNuxtApp()
import { useStreamSegmentStore } from '~/stores/streamSegment'
import { fetchAndAddSegmentsByBounds, getHandleCoord } from '~/utils/map'
const streamSegmentStore = useStreamSegmentStore()
let { isLoading, segmentRegion, segmentId, segmentHuc8Id } =
  storeToRefs(streamSegmentStore)
let map: any = null

const wfsBaseUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&outputFormat=application%2Fjson&srsName=EPSG:4326`

const hucBaseUrl =
  segmentRegion.value === 'alaska'
    ? `${wfsBaseUrl}&typeName=hydrology%3Aarctic_rivers_watersheds_stats_simplified`
    : `${wfsBaseUrl}&typeName=hydrology%3Ahuc8`

const segBaseUrl =
  segmentRegion.value === 'alaska'
    ? `${wfsBaseUrl}&typeName=hydrology%3Aarctic_rivers_segments_joined_3338_simplified`
    : `${wfsBaseUrl}&typeName=hydrology%3Aseg_h8_outlet_stats_simplified`

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
  <div id="report-map" style="height: 400px"></div>
</template>

<style lang="scss"></style>
