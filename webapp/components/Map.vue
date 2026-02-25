<script setup lang="ts">
const { $L, $config } = useNuxtApp()

let segBaseUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Aseg_h8_outlet_stats_simplified&outputFormat=application%2Fjson&srsName=EPSG:4326&cql_filter=huc8=`
let hucBaseUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Ahuc8&outputFormat=application%2Fjson&srsName=EPSG:4326&cql_filter=huc8=`

const defaultMapZoom = 4
const defaultMapCenter = [37.8, -96]
const clickToZoomThreshold = 8

let hucBasedGeoJson = false

let simplifiedHucs: any
let map: any
let wmsLayer: any
let simplifiedHucsLayer: any
let simplifiedHucLayer: any
let detailedHucLayer: any
let segmentsLayer: any[] = []
let resetButton: any
let resetButtonInstance: any

const initializeMap = () => {
  map = $L
    .map('map', {
      scrollWheelZoom: false,
      zoomSnap: 0.1,
    })
    .setView(defaultMapCenter, defaultMapZoom)

  $L.tileLayer(
    'https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}',
    {
      maxZoom: 13,
      attribution: 'Map data © USGS',
    }
  ).addTo(map)

  wmsLayer = $L.tileLayer
    .wms(`${$config.public.geoserverUrl}/wms`, {
      transparent: true,
      format: 'image/png',
      layers: 'hydrology:huc8_conus_stats_simplified',
      styles: 'hydrology:hydroviz-choropleth',
      zIndex: 10,
      opacity: 0.85,
    })
    .addTo(map)

  simplifiedHucsLayer = $L
    .geoJSON(simplifiedHucs, {
      style: {
        opacity: 0,
        fillOpacity: 0,
        color: 'transparent',
        fillColor: 'transparent',
        weight: 0,
      },
      onEachFeature: hucFeatureHandler,
    })
    .addTo(map)

  map.on('zoomend', function () {
    if (map.getZoom() > clickToZoomThreshold) {
      if (!hucBasedGeoJson) {
        if (!resetButtonInstance) {
          resetButtonInstance = new resetButton()
          map.addControl(resetButtonInstance)
        }
        addMapBoundsSegments()
      }
    } else {
      if (resetButtonInstance) {
        map.removeControl(resetButtonInstance)
        resetButtonInstance = null
      }
      clearSegments()
      if (!map.hasLayer(wmsLayer)) {
        map.addLayer(wmsLayer)
      }
      resetHUC()
      map.addLayer(simplifiedHucsLayer)
    }
  })

  map.on('click', function () {
    if (map.getZoom() > clickToZoomThreshold) {
      return
    }
    let latlng = map.mouseEventToLatLng(event)
    map.setView(latlng, clickToZoomThreshold)
  })

  map.on('moveend', function () {
    if (hucBasedGeoJson) {
      return
    }
    if (map.getZoom() > clickToZoomThreshold) {
      addMapBoundsSegments()
    }
  })

  resetButton = $L.Control.extend({
    options: {
      position: 'topright',
    },
    onAdd: function () {
      const btn = $L.DomUtil.create('button', 'button')
      btn.setAttribute('aria-label', 'Unselect HUC')
      btn.innerHTML = 'Unselect HUC'
      $L.DomEvent.disableClickPropagation(btn)
      btn.addEventListener('click', () => {
        map.removeControl(this)
        resetButtonInstance = null
        resetHUC()
        if (map.getZoom() < clickToZoomThreshold && !map.hasLayer(wmsLayer)) {
          map.addLayer(wmsLayer)
        }
        map.addLayer(simplifiedHucsLayer)
      })
      return btn
    },
  })
}

const clearSegments = () => {
  segmentsLayer.forEach(layer => {
    map.removeLayer(layer)
  })
  segmentsLayer = []
}

const resetHUC = () => {
  if (detailedHucLayer) {
    map.removeLayer(detailedHucLayer)
  }
  hucBasedGeoJson = false
}

const addDetailedHucLayer = (data: any) => {
  let huc = data
  if (map.hasLayer(wmsLayer)) {
    map.removeLayer(wmsLayer)
  }
  if (detailedHucLayer && map.hasLayer(detailedHucLayer)) {
    map.removeLayer(detailedHucLayer)
  }
  detailedHucLayer = $L
    .geoJSON(huc, {
      style: {
        weight: 0,
        color: '#444444',
        fillOpacity: 0.25,
      },
    })
    .addTo(map)
  let bounds = $L.geoJSON(huc).getBounds()
  map.fitBounds(bounds, {
    padding: [50, 50],
  })
}

const addSegmentsGeoJson = async (data: any) => {
  // Add each segment individually so we can add hover effects
  // (color change and tooltip) to each segment individually.
  data.features.forEach(feature => {
    let segmentColor: string
    if (feature.properties.h8_outlet === 1) {
      segmentColor = '#ff0000' // Red for outlet segments
    } else {
      segmentColor = '#0000ff' // Blue for non-outlet segments
    }
    const layer = $L
      .geoJSON(feature, {
        style: {
          weight: 3,
          color: segmentColor,
        },
      })
      .addTo(map)
      .on('mouseover', function (e) {
        e.target.setStyle({
          color: '#ffff00',
        })
        let segmentName = feature.properties.GNIS_NAME
        if (segmentName !== '') {
          layer.bindTooltip(segmentName).openTooltip()
        }
      })
      .on('mouseout', function (e) {
        e.target.setStyle({
          color: segmentColor,
        })
      })
      .on('click', function (e) {
        navigateTo('/conus/' + e.sourceTarget.feature.properties.seg_id_nat)
      })
    segmentsLayer.push(layer)
  })
}

const addMapBoundsSegments = () => {
  if (simplifiedHucLayer && map.hasLayer(simplifiedHucLayer)) {
    map.removeLayer(simplifiedHucLayer)
  }
  let bounds = map.getBounds()
  let minLon = bounds.getWest()
  let maxLon = bounds.getEast()
  let minLat = bounds.getSouth()
  let maxLat = bounds.getNorth()
  let segUrl =
    `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Aseg_h8_outlet_stats_simplified&outputFormat=application%2Fjson&srsName=EPSG:4326&cql_filter=` +
    `INTERSECTS(the_geom,ENVELOPE(${minLon},${maxLon},${minLat},${maxLat}))`
  fetch(segUrl)
    .then(response => {
      if (!response.ok) {
        throw new Error(
          `Failed to fetch segment data: ${response.status} ${response.statusText}`
        )
      }
      return response.json()
    })
    .then(data => {
      if (map.hasLayer(wmsLayer)) {
        map.removeLayer(wmsLayer)
      }
      addSegmentsGeoJson(data)
    })
    .catch(error => {
      console.error('Error fetching segment data for map bounds:', error)
    })
}

const hucFeatureHandler = (feature: any, layer: any) => {
  layer.on('mouseover', function (e: any) {
    e.target.setStyle({
      color: '#ffff00',
      fillColor: '#ffff00',
      fillOpacity: 0.25,
    })
    const hucName = feature.properties.name
    if (hucName) {
      layer.bindTooltip(hucName).openTooltip()
    }
  })
  layer.on('mouseout', function (e) {
    e.target.setStyle({
      color: 'transparent',
      fillColor: 'transparent',
      fillOpacity: 0,
    })
  })
  layer.on('click', function (e) {
    e.target.setStyle({
      color: 'transparent',
      fillColor: 'transparent',
      fillOpacity: 0,
    })
    if (map.getZoom() < clickToZoomThreshold) {
      return
    }
    hucBasedGeoJson = true
    if (map.hasLayer(simplifiedHucsLayer)) {
      map.removeLayer(simplifiedHucsLayer)
    }
    if (!resetButtonInstance) {
      resetButtonInstance = new resetButton()
      map.addControl(resetButtonInstance)
    }
    if (feature.properties && feature.properties.huc8) {
      // Make the simplified HUC-8 visible when it is clicked.
      // It will be swapped with a high-vertex HUC-8 before zooming in.
      simplifiedHucLayer = $L
        .geoJSON(feature, {
          style: {
            weight: 3,
            color: '#444444',
            fillOpacity: 0.1,
          },
        })
        .addTo(map)

      let segUrl = segBaseUrl + feature.properties.huc8
      let hucUrl = hucBaseUrl + feature.properties.huc8
      let segFetch = fetch(segUrl)
      let hucFetch = fetch(hucUrl)

      Promise.all([segFetch, hucFetch])
        .then(async ([segResponse, hucResponse]) => {
          if (!segResponse.ok || !hucResponse.ok) {
            throw new Error(
              `Failed to fetch HUC or segment data (segments status: ${segResponse.status}, huc status: ${hucResponse.status})`
            )
          }
          const hucData = await hucResponse.json()
          addDetailedHucLayer(hucData)
          addMapBoundsSegments()
        })
        .catch(error => {
          console.error('Error loading HUC or segment data:', error)
        })
    }
  })
}

const loadSimplifiedHucs = async () => {
  try {
    simplifiedHucs = await import('@/assets/hucs_simplified.json')
  } catch (error) {
    console.error('Failed to load simplified HUCs:', error)
  }
}

onMounted(() => {
  loadSimplifiedHucs().then(() => {
    initializeMap()
  })
})
</script>

<template>
  <div id="map" style="height: 500px"></div>
</template>

<style lang="scss">
.leaflet-interactive:focus,
.leaflet-interactive:active {
  outline: none;
}
</style>
