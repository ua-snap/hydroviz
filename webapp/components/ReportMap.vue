<script setup lang="ts">
const { $L, $config } = useNuxtApp()
import { useStreamSegmentStore } from '~/stores/streamSegment'
import { getHandleCoord } from '~/utils/map'
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
            interactive: false,
          },
        })
        .addTo(map)
      map.fitBounds(geoJsonLayer.getBounds(), { padding: [25, 25] })
    })
    .catch(error => {
      console.error('Error fetching HUC GeoJSON data:', error)
    })

  let segUrl = segBaseUrl + `huc8=${hucId.value}`
  fetch(segUrl)
    .then(response => response.json())
    .then(data => {
      let regularSegments = data.features.filter(
        (feature: any) => feature.properties.h8_outlet === 0
      )
      let outletSegments = data.features.filter(
        (feature: any) => feature.properties.h8_outlet === 1
      )

      // Add regular segments to the map first.
      regularSegments.forEach(feature => {
        $L.geoJSON(feature, {
          style: {
            weight: 3,
            color: '#0000ff',
            interactive: false,
          },
        }).addTo(map)

        let latlng = getHandleCoord(feature)
        $L.circleMarker(latlng, {
          radius: 4,
          color: '#0000ff',
          fillColor: '#0000ff',
          fillOpacity: 1,
        }).addTo(map)
      })

      // Add outlet segments next so they effectively have a higher z-index.
      outletSegments.forEach(feature => {
        $L.geoJSON(feature, {
          style: {
            weight: 3,
            color: '#ff0000',
            interactive: false,
          },
        }).addTo(map)

        let latlng = getHandleCoord(feature)
        $L.circleMarker(latlng, {
          radius: 4,
          color: '#ff0000',
          fillColor: '#ff0000',
          fillOpacity: 1,
        }).addTo(map)

        // Place a pin at the same coordinate for outlet segments.
        // It's sometimes too hard to see them otherwise.
        $L.marker(latlng).addTo(map)
      })
    })
    .catch(error => {
      console.error('Error fetching segment GeoJSON data:', error)
    })
}

const addSegment = () => {
  const streamSegmentStore = useStreamSegmentStore()
  const { segmentId } = storeToRefs(streamSegmentStore)
  let url = segBaseUrl + `seg_id_nat=${segmentId.value}`
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
}

onMounted(() => {
  initializeMap()
})
</script>

<template>
  <div id="report-map" style="height: 400px"></div>
</template>

<style lang="scss"></style>
