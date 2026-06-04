<script setup lang="ts">
const { $L, $config } = useNuxtApp()
import { fetchAndAddSegmentsByBounds, clearSegmentLayers } from '~/utils/map'
import { getHandleCoord } from '~/utils/map'
import proj4 from 'proj4'

const props = defineProps<{
  region?: 'conus' | 'alaska'
}>()

const region = props.region || 'conus'
const wfsBaseUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&outputFormat=application%2Fjson`

// Region-specific configuration
const regionConfig = {
  conus: {
    mapId: 'map-conus',
    defaultZoom: 4,
    defaultCenter: [37.8, -96] as [number, number],
    minZoom: 4,
    maxZoom: 12,
    crs: 'EPSG:4326',
    segLayer: 'hydrology:seg_h8_outlet_stats_simplified_subset',
    hucLayer: 'hydrology:huc8_conus_stats_simplified',
    perimeterAsset: '@/assets/conus_perimeter.json',
    hucsAsset: '@/assets/conus_hucs_simplified.json',
    segBaseUrl: `${wfsBaseUrl}&typeName=hydrology%3Aseg_h8_outlet_stats_simplified_subset`,
    hucBaseUrl: `${wfsBaseUrl}&typeName=hydrology%3Ahuc8&srsName=EPSG:4326`,
  },
  alaska: {
    mapId: 'map-alaska',
    defaultZoom: 0,
    defaultCenter: [64.2, -152.0] as [number, number],
    minZoom: 0,
    maxZoom: 12,
    crs: 'EPSG:3338',
    segLayer: 'hydrology:arctic_rivers_segments_joined_3338_simplified',
    hucLayer: 'hydrology:arctic_rivers_watersheds_stats_simplified',
    perimeterAsset: '@/assets/conus_perimeter.json',
    hucsAsset: '@/assets/alaska_hucs_simplified4326.json',
    segBaseUrl: `${wfsBaseUrl}&typeName=hydrology%3Aarctic_rivers_segments_joined_3338_simplified`,
    hucBaseUrl: `${wfsBaseUrl}&typeName=hydrology%3Aarctic_rivers_watersheds_stats_simplified&srsName=EPSG:4326`,
  },
}

const config = regionConfig[region]

let segmentWmsThreshold: number
let clickToZoomThreshold: number
let hucSelectThreshold: number
let segViewThreshold: number

if (region === 'alaska') {
  segmentWmsThreshold = 1
  clickToZoomThreshold = 2
  hucSelectThreshold = 2
  segViewThreshold = 3
} else {
  segmentWmsThreshold = 6
  clickToZoomThreshold = 7
  hucSelectThreshold = 7
  segViewThreshold = 8
}

let hucBasedGeoJson = false

// GeoJSON to load dynamically on mount.
let perimeter: any
let simplifiedHucs: any

let map: any
let hucWmsLayer: any
let segWmsLayer: any
let perimeterLayer: any
let simplifiedHucsLayer: any
let simplifiedHucLayer: any
let detailedHucLayer: any

const initializeMap = () => {
  const mapOptions: any = {
    scrollWheelZoom: false,
    zoomSnap: 0.1,
    minZoom: config.minZoom,
    maxZoom: config.maxZoom,
  }

  let proj: any = null

  if (config.crs === 'EPSG:3338') {
    let resolutions = [4096, 2048, 1024, 512, 256, 128, 64]
    proj = new $L.Proj.CRS(
      'EPSG:3338',
      '+proj=aea +lat_1=55 +lat_2=65 +lat_0=50 +lon_0=-154 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs',
      {
        // Lower-left corner of GeoServer's gridset bounds for EPSG:3338
        origin: [-4648005.934316417, 444809.882955059],
        resolutions: resolutions,
      }
    )
    mapOptions.crs = proj
  }

  map = $L
    .map(config.mapId, mapOptions)
    .setView(config.defaultCenter, config.defaultZoom)

  if (config.mapId === 'map-conus') {
    $L.tileLayer(
      'https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}',
      {
        attribution: 'Map data © USGS',
      }
    ).addTo(map)
  } else if (config.mapId === 'map-alaska') {
    let url = `${$config.public.geoserverUrl}/wms`
    $L.tileLayer
      .wms(url, {
        transparent: true,
        crs: proj,
        format: 'image/png',
        version: '1.3.0',
        layers: 'atlas_mapproxy:alaska_osm_retina',
      })
      .addTo(map)
  }

  hucWmsLayer = $L.tileLayer
    .wms(`${$config.public.geoserverUrl}/wms`, {
      transparent: true,
      format: 'image/png',
      layers: config.hucLayer,
      styles: 'hydrology:hydroviz-choropleth',
      zIndex: 10,
      opacity: 0.85,
    })
    .addTo(map)

  // Initialize but don't add to map until later.
  segWmsLayer = $L.tileLayer.wms(`${$config.public.geoserverUrl}/wms`, {
    transparent: true,
    format: 'image/png',
    layers: config.segLayer,
    zIndex: 20,
    opacity: 0.2,
  })

  if (simplifiedHucs) {
    simplifiedHucsLayer = $L.geoJSON(simplifiedHucs, {
      style: {
        opacity: 0,
        fillOpacity: 0,
        color: 'transparent',
        fillColor: 'transparent',
        weight: 0,
      },
      onEachFeature: hucFeatureHandler,
    })
    simplifiedHucsLayer.addTo(map)
  }

  if (perimeter) {
    perimeterLayer = $L
      .geoJSON(perimeter, {
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
            map.removeLayer(perimeterLayer)
          })
        },
      })
      .addTo(map)
  }

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
      clearSegmentLayers(map)
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
      if (perimeterLayer && !map.hasLayer(perimeterLayer)) {
        map.addLayer(perimeterLayer)
      }
    } else {
      if (perimeterLayer && map.hasLayer(perimeterLayer)) {
        map.removeLayer(perimeterLayer)
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
      fetchAndAddSegmentsByBounds({
        map,
        $L,
        fitBounds: false,
        mapType: 'main',
      })
    }
  })
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
    const outletValue =
      region === 'alaska'
        ? (feature.properties.Outlet ?? feature.properties.outlet)
        : feature.properties.h8_outlet
    const isOutlet = outletValue === 1
    if (isOutlet) {
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

    // Add a circle marker as a handle.
    let latlng = getHandleCoord(feature)
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
          if (region === 'conus') {
            let segmentName = feature.properties.GNIS_NAME
            if (segmentName !== '') {
              layer
                .bindTooltip(segmentName, {
                  className: 'is-size-6 px-3',
                  opacity: 1,
                })
                .openTooltip()
            }
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
          if (config.mapId === 'map-conus') {
            navigateTo('/conus/stream/' + feature.properties.seg_id_nat)
          } else if (config.mapId === 'map-alaska') {
            navigateTo('/alaska/stream/' + feature.properties.COMID)
          }
        })
      // segGeoJsonLayers.push(layer)
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
  let minLon, maxLon, minLat, maxLat
  minLon = bounds.getWest()
  maxLon = bounds.getEast()
  minLat = bounds.getSouth()
  maxLat = bounds.getNorth()

  let segUrl =
    regionConfig[region].segBaseUrl +
    `&srsName=${regionConfig[region].crs}&cql_filter=` +
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
      if (config.crs === 'EPSG:3338') {
        data.features.forEach((feature: any) => {
          feature.geometry.coordinates = feature.geometry.coordinates.map(
            (line: any) =>
              line.map((coord: any) => proj4('EPSG:3338', 'EPSG:4326', coord))
          )
        })
      }
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
    let hucName =
      region === 'alaska' ? feature.properties.Name : feature.properties.name
    let hucId =
      region === 'alaska' ? feature.properties.ID_2 : feature.properties.huc8
    if (hucName && hucId) {
      layer
        .bindTooltip(`${hucName} (${hucId})`, {
          className: 'is-size-6 px-3',
          opacity: 1,
        })
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
    // if (feature.properties && feature.properties.huc8) {
    if (feature.properties) {
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

      let hucUrl =
        region === 'alaska'
          ? `${regionConfig[region].hucBaseUrl}&cql_filter=ID_2='${feature.properties.ID_2}'`
          : `${regionConfig[region].hucBaseUrl}&cql_filter=huc8=${feature.properties.huc8}`

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

const loadPerimeter = async () => {
  if (!config.perimeterAsset) {
    return
  }
  try {
    if (region === 'conus') {
      perimeter = await import('@/assets/conus_perimeter.json')
    } else if (region === 'alaska') {
      perimeter = await import('@/assets/alaska_perimeter.json')
    }
  } catch (error) {
    console.error('Failed to load perimeter:', error)
  }
}

const loadSimplifiedHucs = async () => {
  if (!config.hucsAsset) {
    return
  }
  try {
    if (region === 'conus') {
      simplifiedHucs = await import('@/assets/conus_hucs_simplified.json')
    } else if (region === 'alaska') {
      simplifiedHucs = await import('@/assets/alaska_hucs_simplified.json')
    }
  } catch (error) {
    console.error('Failed to load simplified HUCs:', error)
  }
}

onMounted(() => {
  Promise.all([loadSimplifiedHucs(), loadPerimeter()]).then(() => {
    initializeMap()
  })
})
</script>

<template>
  <div :id="config.mapId" style="height: 500px"></div>
</template>

<style lang="scss">
.leaflet-interactive:focus,
.leaflet-interactive:active {
  outline: none;
}
</style>
