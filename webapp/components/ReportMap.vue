<script setup lang="ts">
const { $L, $config } = useNuxtApp()
import { useStreamSegmentStore } from '~/stores/streamSegment'
import { fetchAndAddSegmentsByBounds } from '~/utils/map'
const streamSegmentStore = useStreamSegmentStore()
let { isLoading, hucId, segmentId } = storeToRefs(streamSegmentStore)

const hucBaseUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Ahuc8&outputFormat=application%2Fjson&srsName=EPSG:4326&cql_filter=huc8=`
const segBaseUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Aseg_h8_outlet_stats_simplified_subset&outputFormat=application%2Fjson&srsName=EPSG:4326&cql_filter=`

let map: any = null

const getHucOutletSegmentId = async (
  hucIdValue: string
): Promise<number | null> => {
  try {
    const url = `${segBaseUrl}huc8=${hucIdValue}`
    const response = await fetch(url)
    const data = await response.json()

    const features = Array.isArray(data?.features) ? data.features : []
    if (features.length === 0) {
      console.error('No features returned for HUC:', hucIdValue)
      return null
    }

    // Find the outlet segment (h8_outlet === 1)
    const outletFeature = features.find(
      (feature: any) => feature?.properties?.h8_outlet === 1
    )

    if (!outletFeature || !outletFeature.properties) {
      console.error('No outlet feature found for HUC:', hucIdValue)
      return null
    }

    return outletFeature.properties.seg_id_nat
  } catch (error) {
    console.error('Error fetching outlet segment for HUC:', error)
    return null
  }
}

const addHuc = async () => {
  let hucUrl = hucBaseUrl + hucId.value

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

      segmentId.value = outletSegmentId

      // After fitting bounds, add all segments in the viewport with the outlet highlighted
      fetchAndAddSegmentsByBounds({
        map,
        $L,
        segBaseUrl,
        selectedSegmentId: segmentId.value,
        fitBounds: false,
        mapType: 'report',
      })
    })
    .catch(error => {
      console.error('Error fetching HUC GeoJSON data:', error)
    })
}

const addSegment = () => {
  if (!segmentId.value) {
    const route = useRoute()
    const id = computed(() => parseInt(route.params.segment))
    segmentId.value = id.value
  }
  if (isLoading.value) return

  fetchAndAddSegmentsByBounds({
    map,
    $L,
    segBaseUrl,
    interactive: true,
    selectedSegmentId: segmentId.value,
    mapType: 'report',
  })
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

  $L.tileLayer(
    'https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}',
    {
      maxZoom: 13,
      attribution: 'Map data © USGS',
      opacity: 0.75,
    }
  ).addTo(map)

  if (hucId.value !== null) {
    addHuc()
  } else {
    addSegment()
  }

  map.on('dragend', function (e) {
    fetchAndAddSegmentsByBounds({
      map,
      $L,
      segBaseUrl,
      interactive: true,
      selectedSegmentId: segmentId.value,
      fitBounds: false,
      mapType: 'report',
    })
  })
}

onMounted(() => {
  if (isLoading.value) return
  initializeMap()
})
</script>

<template>
  <div id="report-map" style="height: 400px"></div>
</template>

<style lang="scss"></style>
