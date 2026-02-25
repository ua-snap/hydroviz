<script setup lang="ts">
const { $L, $config } = useNuxtApp()
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { hucId } = storeToRefs(streamSegmentStore)

const hucBaseUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Ahuc8&outputFormat=application%2Fjson&srsName=EPSG:4326&cql_filter=huc8=`
const segBaseUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Aseg_h8_outlet_stats_simplified&outputFormat=application%2Fjson&srsName=EPSG:4326&cql_filter=`

let map: any = null

const addHuc = () => {
  let hucUrl = hucBaseUrl + hucId.value
  fetch(hucUrl)
    .then(response => response.json())
    .then(data => {
      let geoJsonLayer = $L
        .geoJSON(data, {
          style: {
            weight: 0,
            color: '#111111',
            fillOpacity: 0.25,
            interactive: false,
          },
          interactive: false,
        })
        .addTo(map)
      map.fitBounds(geoJsonLayer.getBounds())
    })
    .catch(error => {
      console.error('Error fetching HUC GeoJSON data:', error)
    })

  let segUrl = segBaseUrl + `huc8=${hucId.value}`
  fetch(segUrl)
    .then(response => response.json())
    .then(data => {
      data.features.forEach(feature => {
        let segmentColor: string
        if (feature.properties.h8_outlet === 1) {
          segmentColor = '#ff0000' // Red for outlet segments
        } else {
          segmentColor = '#0000ff' // Blue for non-outlet segments
        }
        let line = $L
          .geoJSON(feature, {
            style: {
              weight: 3,
              color: segmentColor,
              interactive: false,
            },
          })
          .addTo(map)
      })
    })
    .catch(error => {
      console.error('Error fetching segment GeoJSON data:', error)
    })
}

const addSegment = () => {
  const streamSegmentStore = useStreamSegmentStore()
  const segmentId = streamSegmentStore.segmentId
  let url = segBaseUrl + `seg_id_nat=${segmentId}`
  fetch(url)
    .then(response => response.json())
    .then(data => {
      let geoJsonLayer = $L
        .geoJSON(data, {
          style: {
            color: '#0000ff',
            weight: 3,
          },
          interactive: false,
        })
        .addTo(map)
      map.fitBounds(geoJsonLayer.getBounds())
    })
    .catch(error => {
      console.error('Error fetching GeoJSON data:', error)
    })
}

const initializeMap = () => {
  map = $L
    .map('report-map', {
      scrollWheelZoom: false,
      dragging: false,
      zoomControl: false,
    })
    .setView([37.8, -96], 8)

  $L.tileLayer(
    'https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}',
    {
      maxZoom: 13,
      attribution: 'Map data © USGS',
    }
  ).addTo(map)

  if (hucId.value !== null) {
    addHuc()
  } else {
    addSegment()
  }
}

onMounted(() => {
  initializeMap()
})
</script>

<template>
  <div id="report-map" style="height: 400px"></div>
</template>

<style lang="scss"></style>
