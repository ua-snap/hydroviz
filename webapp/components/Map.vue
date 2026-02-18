<script setup lang="ts">
const { $L } = useNuxtApp()
import { useStreamSegmentStore } from '~/stores/streamSegment'

const streamSegmentStore = useStreamSegmentStore()

let zoomAddGeoJson = false
let moveAddGeoJson = false
let selectedSeg = null // will have a reference to a stream segment Leaflet object
onMounted(() => {
  var map = $L
    .map('map', {
      scrollWheelZoom: false,
    })
    .setView([37.8, -96], 8)
  var geoJsonlayer: any = null

  $L.tileLayer(
    'https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}',
    {
      maxZoom: 13,
      attribution: 'Map data © USGS',
    }
  ).addTo(map)

  var wmsLayer = $L.tileLayer
    .wms('https://gs.earthmaps.io/geoserver/wms', {
      transparent: true,
      format: 'image/png',
      layers: 'hydrology:seg',
      zIndex: 10,
    })
    .addTo(map)

  map.on('zoomend', function () {
    if (moveAddGeoJson) {
      return
    } else {
      zoomAddGeoJson = true
    }
    if (map.getZoom() > 8) {
      if (!geoJsonlayer) {
        var bounds = map.getBounds()
        var minLon = bounds.getWest()
        var maxLon = bounds.getEast()
        var minLat = bounds.getSouth()
        var maxLat = bounds.getNorth()
        addGeoJson(minLon, maxLon, maxLat, minLat)
      }
    } else {
      if (!map.hasLayer(wmsLayer)) {
        map.addLayer(wmsLayer)
      }
      if (geoJsonlayer && map.hasLayer(geoJsonlayer)) {
        map.removeLayer(geoJsonlayer)
        geoJsonlayer = null
      }
    }
  })

  map.on('moveend', function () {
    if (zoomAddGeoJson) {
      return
    } else {
      moveAddGeoJson = true
    }
    if (geoJsonlayer) {
      map.removeLayer(geoJsonlayer)
      geoJsonlayer = null
    }
    if (map.getZoom() > 8) {
      var bounds = map.getBounds()
      var minLon = bounds.getWest()
      var maxLon = bounds.getEast()
      var minLat = bounds.getSouth()
      var maxLat = bounds.getNorth()
      addGeoJson(minLon, maxLon, maxLat, minLat)
    } else {
      if (!map.hasLayer(wmsLayer)) {
        map.addLayer(wmsLayer)
      }
      if (geoJsonlayer && map.hasLayer(geoJsonlayer)) {
        map.removeLayer(geoJsonlayer)
        geoJsonlayer = null
      }
    }
  })

  const addGeoJson = async (
    minLon: number,
    maxLon: number,
    maxLat: number,
    minLat: number
  ) => {
    if (geoJsonlayer) return
    // "get geojson of matching stream segments"
    // TODO: switch between a simplified geometry at farther-out zoom levels
    // to improve performance
    fetch(
      'https://gs.earthmaps.io/geoserver/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Aseg&outputFormat=application%2Fjson&srsName=EPSG:4326&cql_filter=INTERSECTS(the_geom,ENVELOPE(' +
        minLon +
        ',' +
        maxLon +
        ',' +
        maxLat +
        ',' +
        minLat +
        '))'
    )
      .then(response => response.json())
      .then(data => {
        geoJsonlayer = $L
          .geoJSON(data, {
            style: {
              weight: 5,
            },
          })
          .addTo(map)
          .on('click', function (e) {
            // Navigate to report page
            navigateTo('/conus/' + e.sourceTarget.feature.properties.seg_id_nat)
          })
        zoomAddGeoJson = false
        moveAddGeoJson = false
        map.removeLayer(wmsLayer)
      })
  }
})
</script>

<template>
  <div id="map" style="height: 500px"></div>
</template>

<style lang="scss"></style>
