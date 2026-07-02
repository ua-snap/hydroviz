<script setup lang="ts">
import {
  fetchAndAddSegmentsByBounds,
  fetchSegmentsForBounds,
  addSegmentsGeoJson,
  clearSegmentLayers,
} from '~/utils/map'
import { MapPhase, ALL_MAP_PARAMS } from '~/types/map'
import waterLoaderUrl from '@/assets/water-loader.svg'

const { $L, $config } = useNuxtApp()
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
    crs: 'EPSG:3857',
    segLayer: 'hydrology:seg_h8_outlet_stats_simplified_subset',
    hucLayer: 'hydrology:huc8_conus_stats_simplified',
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
// Set while the Phase 2 swap moves the map itself, so the moveend handler does
// not re-fetch segments that loadPhase2Data already added.
let suppressMoveFetch = false

// Drives the loading overlay shown during the Phase 1 -> Phase 2 transition,
// covering both the HUC boundary fetch and the initial segment fetch.
const isLoadingPhase2 = ref(false)

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
  isLoadingPhase2.value = false
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
  isLoadingPhase2.value = false
  hideLayer(detailedHucLayer)
  clearSegmentLayers(map)
  hideLayer(perimeterLayer)
  showLayer(hucWmsLayer)
  showLayer(simplifiedHucsLayer)
  // Clear any stale hover highlight left over from a HUC click that advanced to
  // Phase 2 before its mouseout fired.
  simplifiedHucsLayer?.resetStyle?.()
  showLayer(segWmsLayer)
  map.setView(center, hucSelectZoom)
}

// Phase 2 — HUC selected. Zoom is driven by fitBounds() to the selected HUC.
// Layers: detailed HUC boundary + stream segment GeoJSON. All overview/WMS
// layers hidden. The Phase 1 view is left fully intact while the data loads;
// loadPhase2Data swaps everything in atomically once it's ready.
const enterPhase2 = (hucId: string) => {
  currentPhase = MapPhase.HucSelected
  isLoadingPhase2.value = true
  loadPhase2Data(hucId)
}

const fetchHuc = async (hucId: string) => {
  const hucUrl =
    region === 'alaska'
      ? `${config.hucBaseUrl}&cql_filter=ID_2='${hucId}'`
      : `${config.hucBaseUrl}&cql_filter=huc8=${hucId}`
  const r = await fetch(hucUrl)
  if (!r.ok)
    throw new Error(`Failed to fetch HUC ${hucId} (status ${r.status})`)
  return r.json()
}

// The Phase 2 zoom is pinned to segmentSelectZoom (clamped to the map's max).
// fitBounds would otherwise zoom out to fit large HUCs, packing the stream
// network too densely; this is also the value that caps zoom-in for small HUCs.
const phase2Zoom = () => Math.min(segmentSelectZoom, config.maxZoom)

// Saved center from the URL ([lat, lng]), or null if absent/invalid. A fresh
// HUC click clears these, so a present value means we are restoring a Phase 2
// view (e.g. returning from a segment report after panning).
const urlCenter = (): [number, number] | null => {
  const lat = parseFloat(route.query[paramKeys.lat] as string)
  const lng = parseFloat(route.query[paramKeys.lng] as string)
  return !isNaN(lat) && !isNaN(lng) ? [lat, lng] : null
}

// Computes the lat/lng bounds the viewport WOULD show at a given center/zoom,
// without moving the map — so segments are fetched for the same visible extent
// before the atomic swap happens.
const viewportBoundsAt = (center: any, zoom: number) => {
  const half = map.getSize().divideBy(2)
  const centerPx = map.project(center, zoom)
  const sw = map.unproject(centerPx.add($L.point(-half.x, half.y)), zoom)
  const ne = map.unproject(centerPx.add($L.point(half.x, -half.y)), zoom)
  return $L.latLngBounds(sw, ne)
}

// Loads the HUC boundary and its segments BEFORE touching the visible map, then
// swaps layers and moves the map in a single synchronous block. Because nothing
// above the swap alters the map, the user sees the intact Phase 1 view (under the
// loading overlay) until the fully-rendered Phase 2 view appears in one paint.
const loadPhase2Data = async (hucId: string) => {
  // Capture the saved center synchronously, before any await (or the onMounted
  // updatePositionInUrl) can overwrite it. Present => restore a panned view;
  // absent => fresh HUC click, so center on the HUC below.
  const savedCenter = urlCenter()
  try {
    const hucData = await fetchHuc(hucId)
    const bounds = $L.geoJSON(hucData).getBounds()
    if (!bounds?.isValid?.()) throw new Error('HUC has no valid bounds')

    const center = savedCenter ?? bounds.getCenter()
    const zoom = phase2Zoom()

    const segData = await fetchSegmentsForBounds({
      bounds: viewportBoundsAt(center, zoom),
      region,
    })

    // --- Atomic swap (no awaits below: a single render frame) ---
    hideLayer(perimeterLayer)
    hideLayer(hucWmsLayer)
    hideLayer(segWmsLayer)
    hideLayer(simplifiedHucsLayer)
    hideLayer(detailedHucLayer)
    clearSegmentLayers(map)

    detailedHucLayer = $L
      .geoJSON(hucData, {
        style: { weight: 0, fillColor: '#111111', fillOpacity: 0.2 },
      })
      .addTo(map)

    // Move to the Phase 2 view (saved center if restoring, else the HUC center).
    // Suppress the moveend-driven refetch (consumed in the moveend handler, which
    // also covers the animated case where moveend fires after this call returns)
    // since the segments are added explicitly below.
    suppressMoveFetch = true
    map.setView(center, zoom, { animate: false })

    addSegmentsGeoJson({
      map,
      $L,
      data: segData,
      selectedSegmentId: null,
      fitBounds: false,
      mapType: 'main',
      mapRegion: region,
    })
  } catch (err) {
    console.error('Error loading Phase 2 data:', err)
    // Revert to Phase 1 to try and keep UI consistent
    enterPhase1(centerFromUrl())
  } finally {
    // Done loading, OK
    isLoadingPhase2.value = false
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
    // Phase 1 -> Phase 2: push a new history entry for the selected HUC. Clear
    // the carried-over Phase 1 center so loadPhase2Data centers on the HUC; the
    // map's own moveend then records the Phase 2 center for later restoration.
    const query = {
      ...safeQuery(),
      [paramKeys.phase]: String(MapPhase.HucSelected),
      [paramKeys.huc]: String(hucId),
    }
    delete query[paramKeys.lat]
    delete query[paramKeys.lng]
    router.push({ query })
  })
}

// The view the map should be created at, derived from the URL. On a remount
// (e.g. Back from a segment report) this starts the map at the saved Phase 2
// center/zoom instead of the default extent, so it never flashes the full
// region before loadPhase2Data settles it. Falls back to the region default.
const initialView = (): { center: [number, number]; zoom: number } => {
  const center = urlCenter()
  if (center) {
    if (phaseFromUrl() === MapPhase.HucSelected) {
      return { center, zoom: phase2Zoom() }
    }
    if (phaseFromUrl() === MapPhase.WmsHuc) {
      return { center, zoom: hucSelectZoom }
    }
  }
  return { center: config.defaultCenter, zoom: defaultViewZoom }
}

const initializeMap = () => {
  // Zoom is owned entirely by the phase functions; the user may only pan and
  // click. Disable every user-driven zoom interaction and the zoom control.
  const mapOptions: any = {
    zoomControl: false,
    scrollWheelZoom: false,
    doubleClickZoom: false,
    boxZoom: false,
    touchZoom: false,
    keyboard: false,
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

  const view = initialView()
  map = $L.map(config.mapId, mapOptions).setView(view.center, view.zoom)

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
    // Skip the refetch for the programmatic Phase 2 move (loadPhase2Data adds the
    // segments itself). Consume the flag here so it works whether moveend fires
    // synchronously or after an animated move.
    if (suppressMoveFetch) {
      suppressMoveFetch = false
      return
    }
    // Refresh segments for the new viewport when panning within Phase 2.
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
    let streamSegmentStore = useStreamSegmentStore()
    let { segmentRegion } = storeToRefs(streamSegmentStore)
    segmentRegion.value = null
    initializeMap()
    // Apply whatever phase the URL describes (default Phase 0), then ensure the
    // URL reflects it. Both are replaces, so a fresh load adds no history depth.
    syncMapFromUrl()
    updatePositionInUrl()
  })
})
</script>

<template>
  <div class="map-wrapper" style="height: 80vh; min-height: 500px">
    <div :id="config.mapId" style="height: 100%"></div>
    <div v-if="isLoadingPhase2" class="map-loading-overlay">
      <img :src="waterLoaderUrl" class="map-loading-icon" alt="" />
      <p class="mt-3 has-text-white is-size-3 is-bold">
        Loading stream network&hellip;
      </p>
    </div>
  </div>
</template>

<style lang="scss">
.leaflet-interactive:focus,
.leaflet-interactive:active {
  outline: none;
}

.map-wrapper {
  position: relative;
}

.map-loading-overlay {
  position: absolute;
  inset: 0;
  // Above Leaflet panes (max ~700) and controls (~1000).
  z-index: 1100;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(128, 128, 128, 0.5);
  pointer-events: all;
}

.map-loading-icon {
  width: 6rem;
  height: 6rem;
}
</style>
