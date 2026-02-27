<script setup lang="ts">
const { $L, $config } = useNuxtApp()

const segBaseUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Aseg_h8_outlet_stats_simplified&outputFormat=application%2Fjson&srsName=EPSG:4326&cql_filter=`
const hucBaseUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Ahuc8&outputFormat=application%2Fjson&srsName=EPSG:4326&cql_filter=huc8=`

const defaultMapZoom = 4
const defaultMapCenter = [37.8, -96]
const segmentWmsThreshold = 6
const clickToZoomThreshold = 7
const hucSelectThreshold = 7
const segViewThreshold = 8

let hucBasedGeoJson = false

// GeoJSON to load dynamically on mount.
let conusPerimeter: any
let simplifiedHucs: any

let map: any
let hucWmsLayer: any
let segWmsLayer: any
let conusPerimeterLayer: any
let simplifiedHucsLayer: any
let simplifiedHucLayer: any
let detailedHucLayer: any
let segGeoJsonLayers: any[] = []

const initializeMap = () => {
  map = $L
    .map('map', {
      scrollWheelZoom: false,
      zoomSnap: 0.1,
      minZoom: 4,
      maxZoom: 12,
    })
    .setView(defaultMapCenter, defaultMapZoom)

  $L.tileLayer(
    'https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}',
    {
      attribution: 'Map data © USGS',
    }
  ).addTo(map)

  hucWmsLayer = $L.tileLayer
    .wms(`${$config.public.geoserverUrl}/wms`, {
      transparent: true,
      format: 'image/png',
      layers: 'hydrology:huc8_conus_stats_simplified',
      styles: 'hydrology:hydroviz-choropleth',
      zIndex: 10,
      opacity: 0.85,
    })
    .addTo(map)

  // Initialize but don't add to map until later.
  segWmsLayer = $L.tileLayer.wms(`${$config.public.geoserverUrl}/wms`, {
    transparent: true,
    format: 'image/png',
    layers: 'hydrology:seg_h8_outlet_stats_simplified',
    zIndex: 20,
    opacity: 0.2,
  })

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

  conusPerimeterLayer = $L
    .geoJSON(conusPerimeter, {
      style: {
        opacity: 0,
        fillOpacity: 0,
        interactive: true,
      },
      onEachFeature: function (feature, layer) {
        layer.on('click', function (e) {
          if (map.getZoom() < clickToZoomThreshold) {
            map.setView(e.latlng, clickToZoomThreshold)
          }
          map.removeLayer(conusPerimeterLayer)
        })
      },
    })
    .addTo(map)

  map.on('zoomend', function () {
    let zoomLevel = map.getZoom()
    if (zoomLevel >= segViewThreshold) {
      if (map.hasLayer(segWmsLayer)) {
        map.removeLayer(segWmsLayer)
      }
      if (hucBasedGeoJson) {
        addMapBoundsSegments()
      }
    } else {
      clearSegments()
      if (!map.hasLayer(hucWmsLayer)) {
        map.addLayer(hucWmsLayer)
      }
      if (!map.hasLayer(simplifiedHucsLayer)) {
        map.addLayer(simplifiedHucsLayer)
      }
    }
    if (zoomLevel < hucSelectThreshold || zoomLevel >= segViewThreshold) {
      if (map.hasLayer(simplifiedHucsLayer)) {
        map.removeLayer(simplifiedHucsLayer)
      }
    }
    if (zoomLevel >= segmentWmsThreshold && zoomLevel < segViewThreshold) {
      if (!map.hasLayer(segWmsLayer)) {
        map.addLayer(segWmsLayer)
      }
    } else {
      if (map.hasLayer(segWmsLayer)) {
        map.removeLayer(segWmsLayer)
      }
    }
    if (zoomLevel < clickToZoomThreshold) {
      if (!map.hasLayer(segWmsLayer)) {
        map.addLayer(conusPerimeterLayer)
      }
    } else {
      if (map.hasLayer(conusPerimeterLayer)) {
        map.removeLayer(conusPerimeterLayer)
      }
    }
    if (zoomLevel < segViewThreshold) {
      resetHUC()
    }
  })

  map.on('moveend', function () {
    if (hucBasedGeoJson) {
      return
    }
    if (map.getZoom() >= segViewThreshold) {
      addMapBoundsSegments()
    }
  })
}

const clearSegments = () => {
  segGeoJsonLayers.forEach(layer => {
    map.removeLayer(layer)
  })
  segGeoJsonLayers = []
}

const resetHUC = () => {
  if (detailedHucLayer) {
    map.removeLayer(detailedHucLayer)
  }
  hucBasedGeoJson = false
}

const addDetailedHucLayer = (data: any) => {
  let huc = data
  if (map.hasLayer(hucWmsLayer)) {
    map.removeLayer(hucWmsLayer)
  }
  if (detailedHucLayer && map.hasLayer(detailedHucLayer)) {
    map.removeLayer(detailedHucLayer)
  }
  detailedHucLayer = $L
    .geoJSON(huc, {
      style: {
        weight: 0,
        fillColor: '#111111',
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
    let line = $L
      .geoJSON(feature, {
        style: {
          weight: 3,
          color: segmentColor,
        },
      })
      .addTo(map)

    // Extract the first coordinate to place the handle.
    let firstCoord = feature.geometry.coordinates[0][0]
    let latlng = $L.latLng(firstCoord[1], firstCoord[0])

    // Add a circle marker as a handle.
    let handle = $L
      .circleMarker(latlng, {
        radius: 4,
        color: segmentColor,
        fillColor: segmentColor,
        fillOpacity: 1,
      })
      .addTo(map)

    let segmentParts = [line, handle]
    segmentParts.forEach(layer => {
      layer
        .on('mouseover', function (e) {
          segmentParts.forEach(part => {
            part.setStyle({
              color: '#ffff00',
              fillColor: '#ffff00',
            })
          })
          let segmentName = feature.properties.GNIS_NAME
          if (segmentName !== '') {
            layer
              .bindTooltip(segmentName, {
                className: 'is-size-6 px-3',
                opacity: 1,
              })
              .openTooltip()
          }
        })
        .on('mouseout', function (e) {
          segmentParts.forEach(part => {
            part.setStyle({
              color: segmentColor,
              fillColor: segmentColor,
            })
          })
        })
        .on('click', function (e) {
          navigateTo('/conus/' + feature.properties.seg_id_nat)
        })
      segGeoJsonLayers.push(layer)
    })
  })
}

const addMapBoundsSegments = () => {
  if (map.hasLayer(hucWmsLayer)) {
    map.removeLayer(hucWmsLayer)
  }
  if (simplifiedHucLayer && map.hasLayer(simplifiedHucLayer)) {
    map.removeLayer(simplifiedHucLayer)
  }
  let bounds = map.getBounds()
  let minLon = bounds.getWest()
  let maxLon = bounds.getEast()
  let minLat = bounds.getSouth()
  let maxLat = bounds.getNorth()
  let segUrl =
    segBaseUrl +
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
      addSegmentsGeoJson(data)
    })
    .catch(error => {
      console.error('Error fetching segment data for map bounds:', error)
    })
}

const hucFeatureHandler = (feature: any, layer: any) => {
  layer.on('mouseover', function (e: any) {
    let mapZoom = map.getZoom()
    if (mapZoom < hucSelectThreshold || mapZoom >= segViewThreshold) {
      return
    }
    e.target.setStyle({
      color: '#ffff00',
      fillColor: '#ffff00',
      fillOpacity: 0.5,
    })
    const hoverText = `${feature.properties.name} (${feature.properties.huc8})`
    if (hoverText) {
      layer
        .bindTooltip(hoverText, { className: 'is-size-6 px-3', opacity: 1 })
        .openTooltip()
    }
  })
  layer.on('mouseout', function (e) {
    let mapZoom = map.getZoom()
    if (mapZoom < hucSelectThreshold || mapZoom >= segViewThreshold) {
      return
    }
    e.target.setStyle({
      color: 'transparent',
      fillColor: 'transparent',
      fillOpacity: 0,
    })
  })
  layer.on('click', function (e) {
    let mapZoom = map.getZoom()
    if (mapZoom < hucSelectThreshold || mapZoom >= segViewThreshold) {
      return
    }
    e.target.setStyle({
      color: 'transparent',
      fillColor: 'transparent',
      fillOpacity: 0,
    })
    hucBasedGeoJson = true
    if (map.hasLayer(simplifiedHucsLayer)) {
      map.removeLayer(simplifiedHucsLayer)
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

      let hucUrl = hucBaseUrl + feature.properties.huc8
      let hucFetch = fetch(hucUrl)

      hucFetch
        .then(async hucResponse => {
          if (!hucResponse.ok) {
            throw new Error(
              `Failed to fetch HUC data (huc status: ${hucResponse.status})`
            )
          }
          const hucData = await hucResponse.json()
          addDetailedHucLayer(hucData)
          addMapBoundsSegments()
        })
        .catch(error => {
          console.error('Error loading HUC data:', error)
        })
    }
  })
}

const loadConusPerimeter = async () => {
  try {
    conusPerimeter = await import('@/assets/conus_perimeter.json')
  } catch (error) {
    console.error('Failed to load CONUS outline:', error)
  }
}

const loadSimplifiedHucs = async () => {
  try {
    simplifiedHucs = await import('@/assets/hucs_simplified.json')
  } catch (error) {
    console.error('Failed to load simplified HUCs:', error)
  }
}

onMounted(() => {
  Promise.all([loadSimplifiedHucs(), loadConusPerimeter()]).then(() => {
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
