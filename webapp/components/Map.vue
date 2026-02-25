<script setup lang="ts">
const { $L, $config } = useNuxtApp()

let segBaseUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Aseg_h8_outlet_stats_simplified&outputFormat=application%2Fjson&srsName=EPSG:4326&cql_filter=huc8=`
let hucBaseUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Ahuc8&outputFormat=application%2Fjson&srsName=EPSG:4326&cql_filter=huc8=`

const defaultMapZoom = 4
const defaultMapCenter = [37.8, -96]

let hucBasedGeoJson = false

let simplifiedHucs: any
let map: any
let wmsLayer: any
let simplifiedHucsLayer: any
let simplifiedHucLayer: any
let detailedHucLayer: any
let hucSegmentLayers: any[] = []
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
      onEachFeature: hucClickHandler,
    })
    .addTo(map)

  map.on('zoomend', function () {
    if (map.getZoom() > 9) {
      if (!hucBasedGeoJson) {
        if (!resetButtonInstance) {
          resetButtonInstance = new resetButton()
          map.addControl(resetButtonInstance)
        }
        addMapBoundsSegments()
      }
    } else {
      if (!hucBasedGeoJson) {
        if (resetButtonInstance) {
          map.removeControl(resetButtonInstance)
          resetButtonInstance = null
          if (!map.hasLayer(wmsLayer)) {
            map.addLayer(wmsLayer)
          }
        }
      }
    }
  })

  map.on('moveend', function () {
    if (hucBasedGeoJson) {
      return
    }
    if (!hucBasedGeoJson && hucSegmentLayers.length > 0) {
      hucSegmentLayers.forEach(layer => {
        map.removeLayer(layer)
      })
      hucSegmentLayers = []
    }
    if (map.getZoom() > 9) {
      let bounds = map.getBounds()
      let minLon = bounds.getWest()
      let maxLon = bounds.getEast()
      let minLat = bounds.getSouth()
      let maxLat = bounds.getNorth()
      let segUrl =
        `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Aseg&outputFormat=application%2Fjson&srsName=EPSG:4326&cql_filter=` +
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
          addGeoJson(data)
        })
        .catch(error => {
          console.error('Error fetching segment data for map move:', error)
        })
    }
  })

  resetButton = $L.Control.extend({
    options: {
      position: 'topright',
    },
    onAdd: function () {
      const btn = $L.DomUtil.create('button', 'button')
      btn.setAttribute('aria-label', 'Reset map view')
      btn.innerHTML = 'Reset'
      $L.DomEvent.disableClickPropagation(btn)
      btn.addEventListener('click', () => {
        map.removeControl(this)
        if (detailedHucLayer) {
          map.removeLayer(detailedHucLayer)
        }
        if (!map.hasLayer(wmsLayer)) {
          map.addLayer(wmsLayer)
        }
        map.addLayer(simplifiedHucsLayer)
        if (hucSegmentLayers.length > 0) {
          hucSegmentLayers.forEach(layer => {
            map.removeLayer(layer)
          })
          hucSegmentLayers = []
        }
        hucBasedGeoJson = false
        map.flyTo(defaultMapCenter, defaultMapZoom, {
          duration: 0.25,
        })
      })
      return btn
    },
  })
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
        weight: 3,
        color: '#444444',
        fillOpacity: 0.15,
      },
    })
    .addTo(map)
  let bounds = $L.geoJSON(huc).getBounds()
  map.flyToBounds(bounds, {
    padding: [50, 50],
    duration: 0.25,
  })
}

const addGeoJson = async (data: any) => {
  // Add each segment individually so we can add hover effects
  // (color change and tooltip) to each segment individually.
  data.features.forEach(feature => {
    const layer = $L
      .geoJSON(feature, {
        style: {
          weight: 4,
          color: '#0000ff',
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
          color: '#0000ff',
        })
      })
      .on('click', function (e) {
        navigateTo('/conus/' + e.sourceTarget.feature.properties.seg_id_nat)
      })
    hucSegmentLayers.push(layer)
  })
}

const addHucSegments = (data: any) => {
  if (simplifiedHucLayer && map.hasLayer(simplifiedHucLayer)) {
    map.removeLayer(simplifiedHucLayer)
  }
  addGeoJson(data)
  if (map.hasLayer(wmsLayer)) {
    map.removeLayer(wmsLayer)
  }
}

const addMapBoundsSegments = () => {
  let bounds = map.getBounds()
  let minLon = bounds.getWest()
  let maxLon = bounds.getEast()
  let minLat = bounds.getSouth()
  let maxLat = bounds.getNorth()
  let segUrl =
    `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Aseg&outputFormat=application%2Fjson&srsName=EPSG:4326&cql_filter=` +
    `INTERSECTS(the_geom,ENVELOPE(${minLon},${maxLon},${minLat},${maxLat}))`
  fetch(segUrl)
    .then(response => response.json())
    .then(data => {
      if (map.hasLayer(wmsLayer)) {
        map.removeLayer(wmsLayer)
      }
      addGeoJson(data)
    })
}

const hucClickHandler = (feature: any, layer: any) => {
  layer.on('click', function () {
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

          if (hucSegmentLayers.length > 0) {
            hucSegmentLayers.forEach(layer => {
              map.removeLayer(layer)
            })
            hucSegmentLayers = []
          }

          const hucData = await hucResponse.json()
          addDetailedHucLayer(hucData)

          const segData = await segResponse.json()
          addHucSegments(segData)
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

<style lang="scss"></style>
