<script setup lang="ts">
const { $L, $config } = useNuxtApp()
import { useStreamSegmentStore } from '~/stores/streamSegment'
import { fetchAndAddSegmentsByBounds, getHandleCoord } from '~/utils/map'
const streamSegmentStore = useStreamSegmentStore()
let { isLoading, hucId, segmentType, segmentId } =
  storeToRefs(streamSegmentStore)
let map: any = null

const wfsBaseUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&outputFormat=application%2Fjson&srsName=EPSG:4326`

const hucBaseUrl =
  segmentType.value === 'alaska'
    ? `${wfsBaseUrl}&typeName=hydrology%3Aarctic_rivers_watersheds_stats_simplified`
    : `${wfsBaseUrl}&typeName=hydrology%3Ahuc8`

const segBaseUrl =
  segmentType.value === 'alaska'
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

const getHucOutletSegmentId = async (
  hucIdValue: string
): Promise<number | null> => {
  try {
    const isAlaska = segmentType.value === 'alaska'
    const url = isAlaska
      ? `${segBaseUrl}&cql_filter=ID_1='${hucIdValue}'`
      : `${segBaseUrl}&cql_filter=huc8=${hucIdValue}`

    const response = await fetch(url)
    const data = await response.json()

    const features = Array.isArray(data?.features) ? data.features : []
    if (features.length === 0) {
      console.error('No features returned for HUC:', hucIdValue)
      return null
    }

    const outletProperty = isAlaska ? 'outlet' : 'h8_outlet'
    const segmentIdProperty = isAlaska ? 'COMID' : 'seg_id_nat'

    // Find the outlet segment.
    const outletFeature = features.find(
      (feature: any) => feature?.properties?.[outletProperty] === 1
    )

    if (!outletFeature || !outletFeature.properties) {
      console.error('No outlet feature found for HUC:', hucIdValue)
      return null
    }

    return outletFeature.properties[segmentIdProperty]
  } catch (error) {
    console.error('Error fetching outlet segment for HUC:', error)
    return null
  }
}

const addHuc = async () => {
  const hucUrl =
    segmentType.value === 'alaska'
      ? `${hucBaseUrl}&cql_filter=ID_1='${hucId.value}'`
      : `${hucBaseUrl}&cql_filter=huc8=${hucId.value}`

  // Get the outlet segment ID for this HUC
  const outletSegmentId = await getHucOutletSegmentId(hucId.value)

  fetch(hucUrl)
    .then(response => response.json())
    .then(data => {
      let geoJsonLayer = $L
        .geoJSON(data, {
          style: {
            weight: 0,
            color: '#111111',
            interactive: false,
          },
        })
        .addTo(map)
      map.fitBounds(geoJsonLayer.getBounds(), { padding: [25, 25] })
      setMapMaxBounds()

      segmentId.value = outletSegmentId

      // After fitting bounds, add all segments in the viewport with the outlet highlighted
      fetchAndAddSegmentsByBounds({
        map,
        $L,
        fitBounds: false,
        mapType: 'report',
      })
    })
    .catch(error => {
      console.error('Error fetching HUC GeoJSON data:', error)
    })
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

  let maxZoom = segmentType.value === 'alaska' ? 12 : 13

  $L.tileLayer(
    'https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}',
    {
      maxZoom: maxZoom,
      attribution: 'Map data © USGS',
      opacity: 0.75,
    }
  ).addTo(map)

  if (hucId.value !== null) {
    addHuc()
  } else {
    addSegment()
  }
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
