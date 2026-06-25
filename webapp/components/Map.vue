<script setup lang="ts">
const { $L, $config } = useNuxtApp()
import { fetchAndAddSegmentsByBounds, clearSegmentLayers } from '~/utils/map'
import { MapPhase, ALL_MAP_PARAMS } from '~/types/map'

const route = useRoute()
const router = useRouter()

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
    maxZoom: 6,
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

// Per-phase zoom levels for this region.
let defaultViewZoom: number
let hucSelectZoom: number
let segmentSelectZoom: number

if (region === 'alaska') {
  defaultViewZoom = 0 // phase 0
  hucSelectZoom = 4 // phase 1
  segmentSelectZoom = 8 // phase 2
} else {
  // conus
  defaultViewZoom = 4
  hucSelectZoom = 7
  segmentSelectZoom = 10
}

// Query param keys per region for phase + HUC + center tracking.
const paramKeys =
  region === 'conus'
    ? { phase: 'cp', huc: 'chuc', lat: 'clat', lng: 'clng' }
    : { phase: 'ap', huc: 'ahuc', lat: 'alat', lng: 'alng' }

// Returns only the known map params from the current route query, as plain strings.
// This prevents stale, undefined, or array-valued keys from leaking into URL updates
// when two Map instances (CONUS + Alaska) share the same route query object.
const safeQuery = (): Record<string, string> => {
  const q: Record<string, string> = {}
  for (const key of ALL_MAP_PARAMS) {
    const val = route.query[key]
    if (typeof val === 'string') q[key] = val
  }
  return q
}

// Reads the target phase from the URL, clamped to a valid MapPhase.
const phaseFromUrl = (): MapPhase => {
  const p = parseInt(route.query[paramKeys.phase] as string)
  if (isNaN(p) || p < MapPhase.Overview || p > MapPhase.HucSelected) {
    return MapPhase.Overview
  }
  return p as MapPhase
}

// Reads the saved center from the URL, falling back to the region default.
const centerFromUrl = (): [number, number] => {
  const lat = parseFloat(route.query[paramKeys.lat] as string)
  const lng = parseFloat(route.query[paramKeys.lng] as string)
  return !isNaN(lat) && !isNaN(lng) ? [lat, lng] : config.defaultCenter
}

let map: any
let hucWmsLayer: any
let segWmsLayer: any
let perimeterLayer: any
let simplifiedHucsLayer: any
let detailedHucLayer: any

// GeoJSON loaded dynamically on mount.
let perimeter: any
let simplifiedHucs: any

// The phase the map is currently displaying. Set only by the enterPhaseN functions.
let currentPhase: MapPhase = MapPhase.Overview
// Guards against redundant re-application of the same phase state.
let lastAppliedKey = ''

const showLayer = (layer: any) => {
  if (layer && !map.hasLayer(layer)) map.addLayer(layer)
}
const hideLayer = (layer: any) => {
  if (layer && map.hasLayer(layer)) map.removeLayer(layer)
}

// ============================================================================
// PHASE FUNCTIONS
//
// Each function is the single source of truth for the map's layer + zoom state
// in its phase. Transitions are explicit (perimeter/HUC clicks, Back navigation,
// initial load); there is no zoom-driven conditional layer management.
// ============================================================================

// Phase 0 — Overview. Zoomed out to defaultViewZoom.
// Layers: HUC choropleth (hucWmsLayer) + a transparent perimeter overlay whose
// clicks advance the map to Phase 1.
const enterPhase0 = () => {
  currentPhase = MapPhase.Overview
  hideLayer(detailedHucLayer)
  clearSegmentLayers(map)
  hideLayer(segWmsLayer)
  hideLayer(simplifiedHucsLayer)
  showLayer(hucWmsLayer)
  showLayer(perimeterLayer)
  map.setView(config.defaultCenter, defaultViewZoom)
}

// Phase 1 — HUC selection. Zoomed in to hucSelectZoom at the given center.
// Layers: HUC-8 choropleth (hucWmsLayer) + invisible simplifiedHucsLayer (hover/click targets)
// + segWmsLayer stream overlay. The perimeter is hidden.
const enterPhase1 = (center: [number, number]) => {
  currentPhase = MapPhase.WmsHuc
  hideLayer(detailedHucLayer)
  clearSegmentLayers(map)
  hideLayer(perimeterLayer)
  showLayer(hucWmsLayer)
  showLayer(simplifiedHucsLayer)
  showLayer(segWmsLayer)
  map.setView(center, hucSelectZoom)
}

// Phase 2 — HUC selected. Zoom is driven by fitBounds() to the selected HUC.
// Layers: detailed HUC boundary + stream segment GeoJSON (fetched by viewport
// bounds on moveend). All overview/WMS layers hidden.
const enterPhase2 = (hucId: string) => {
  currentPhase = MapPhase.HucSelected
  hideLayer(perimeterLayer)
  hideLayer(hucWmsLayer)
  hideLayer(segWmsLayer)
  hideLayer(simplifiedHucsLayer)
  clearSegmentLayers(map)
  loadDetailedHuc(hucId)
}

// Fetches a HUC-8 boundary by id and draws it, then fitBounds() to it.
// The resulting moveend triggers the Phase 2 segment fetch.
const loadDetailedHuc = (hucId: string) => {
  const hucUrl =
    region === 'alaska'
      ? `${config.hucBaseUrl}&cql_filter=ID_2='${hucId}'`
      : `${config.hucBaseUrl}&cql_filter=huc8=${hucId}`
  fetch(hucUrl)
    .then(async r => {
      if (!r.ok)
        throw new Error(`Failed to fetch HUC ${hucId} (status ${r.status})`)
      addDetailedHucLayer(await r.json())
    })
    .catch(err => console.error('Error loading HUC data:', err))
}

const addDetailedHucLayer = (data: any) => {
  hideLayer(detailedHucLayer)
  detailedHucLayer = $L
    .geoJSON(data, {
      style: { weight: 0, fillColor: '#111111', fillOpacity: 0.4 },
    })
    .addTo(map)

  const bounds = detailedHucLayer.getBounds?.()
  if (bounds?.isValid?.()) {
    map.fitBounds(bounds, { padding: [50, 50], maxZoom: segmentSelectZoom })
  }
}

// ============================================================================
// URL <-> MAP SYNC
// ============================================================================

// Applies the map state described by the current URL. Deduplicated so repeated
// calls for the same (phase, huc) are no-ops.
const syncMapFromUrl = () => {
  if (!map) return
  const phase = phaseFromUrl()
  const rawHucId = route.query[paramKeys.huc]
  const hucId = typeof rawHucId === 'string' ? rawHucId : undefined
  const validHucId =
    typeof hucId === 'string' &&
    (region === 'alaska'
      ? /^\d{8}$/.test(hucId) || /^[A-Z0-9]{4}$/.test(hucId)
      : /^\d{8}$/.test(hucId))
  const key = `${phase}:${hucId ?? ''}`
  if (key === lastAppliedKey) return
  lastAppliedKey = key

  if (phase === MapPhase.HucSelected && validHucId) {
    enterPhase2(hucId)
  } else if (phase === MapPhase.WmsHuc) {
    enterPhase1(centerFromUrl())
  } else {
    enterPhase0()
  }
}

// Replaces the current history entry's center for the active phase, without
// changing history depth or phase. Called on pan (moveend).
const updatePositionInUrl = () => {
  if (!map) return
  const c = map.getCenter()
  const query: Record<string, string> = {
    ...safeQuery(),
    [paramKeys.phase]: String(currentPhase),
  }
  if (currentPhase >= MapPhase.WmsHuc) {
    query[paramKeys.lat] = c.lat.toFixed(5)
    query[paramKeys.lng] = c.lng.toFixed(5)
  } else {
    delete query[paramKeys.lat]
    delete query[paramKeys.lng]
  }
  if (currentPhase < MapPhase.HucSelected) delete query[paramKeys.huc]
  router.replace({ query })
}

// React to URL phase/huc changes from Back/Forward navigation (and our own
// forward pushes). Center (lat/lng) changes are intentionally not watched so
// panning does not re-trigger a phase application.
watch(
  () => [route.query[paramKeys.phase], route.query[paramKeys.huc]],
  () => syncMapFromUrl()
)

const hucFeatureHandler = (feature: any, layer: any) => {
  layer.on('mouseover', function (e: any) {
    if (currentPhase !== MapPhase.WmsHuc) return
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
  layer.on('mouseout', function (e: any) {
    if (currentPhase !== MapPhase.WmsHuc) return
    e.target.setStyle({
      color: 'transparent',
      fillColor: 'transparent',
      fillOpacity: 0,
    })
  })
  layer.on('click', function () {
    if (currentPhase !== MapPhase.WmsHuc) return
    const hucId =
      region === 'alaska' ? feature.properties.ID_2 : feature.properties.huc8
    if (!hucId) return
    // Phase 1 -> Phase 2: push a new history entry for the selected HUC.
    router.push({
      query: {
        ...safeQuery(),
        [paramKeys.phase]: String(MapPhase.HucSelected),
        [paramKeys.huc]: String(hucId),
      },
    })
  })
}

const initializeMap = () => {
  const mapOptions: any = {
    scrollWheelZoom: false,
    zoomControl: false,
    zoomSnap: 0.1,
    minZoom: Math.min(config.minZoom, defaultViewZoom),
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
    .setView(config.defaultCenter, defaultViewZoom)

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

  // Create the phase-managed layers detached; the phase functions add/remove them.
  hucWmsLayer = $L.tileLayer.wms(`${$config.public.geoserverUrl}/wms`, {
    transparent: true,
    format: 'image/png',
    layers: config.hucLayer,
    styles: 'hydrology:hydroviz-choropleth',
    zIndex: 10,
    opacity: 0.85,
  })

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
  }

  if (perimeter) {
    perimeterLayer = $L.geoJSON(perimeter, {
      style: {
        opacity: 0,
        fillOpacity: 0,
        interactive: true,
      },
      onEachFeature: function (feature, layer) {
        layer.on('click', function (e: any) {
          // Phase 0 -> Phase 1: advance, centered on the click point.
          router.push({
            query: {
              ...safeQuery(),
              [paramKeys.phase]: String(MapPhase.WmsHuc),
              [paramKeys.lat]: e.latlng.lat.toFixed(5),
              [paramKeys.lng]: e.latlng.lng.toFixed(5),
            },
          })
        })
      },
    })
  }

  // Panning within a phase: persist the new center, and in Phase 2 refresh the
  // segment GeoJSON for the new viewport. (No zoomend handler — zoom is owned
  // entirely by the phase functions.)
  map.on('moveend', function () {
    updatePositionInUrl()
    if (currentPhase === MapPhase.HucSelected) {
      fetchAndAddSegmentsByBounds({
        map,
        $L,
        fitBounds: false,
        mapType: 'main',
        region,
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
    // Apply whatever phase the URL describes (default Phase 0), then ensure the
    // URL reflects it. Both are replaces, so a fresh load adds no history depth.
    syncMapFromUrl()
    updatePositionInUrl()
  })
})
</script>

<template>
  <div :id="config.mapId" style="height: 80vh; min-height: 500px"></div>
</template>

<style lang="scss">
.leaflet-interactive:focus,
.leaflet-interactive:active {
  outline: none;
}
</style>
