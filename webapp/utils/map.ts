import { useStreamSegmentStore } from '~/stores/streamSegment'

const segmentColors: Record<string, any> = {
  main: {
    selected: {
      outlet: '#ffff00',
      regular: '#ffff00',
      hover: '#ffff00',
    },
    unselected: {
      outlet: '#ff0000',
      regular: '#0000ff',
      hover: '#ffff00',
    },
  },
  report: {
    selected: {
      outlet: '#ff0000',
      regular: '#0000ff',
      hover: '#ffff00',
    },
    unselected: {
      outlet: '#ff7777',
      regular: '#7777ff',
      hover: '#ffff00',
    },
  },
}

// Remove all layers except those containing MultiPolygon features (HUC boundaries).
export const clearSegmentLayers = (map: any) => {
  const { $L } = useNuxtApp()
  const layersToRemove: any[] = []
  map.eachLayer((layer: any) => {
    if (layer instanceof $L.FeatureGroup || layer instanceof $L.GeoJSON) {
      let isPolygonLayer = false
      layer.eachLayer?.((subLayer: any) => {
        if (subLayer.feature?.geometry?.type === 'MultiPolygon') {
          isPolygonLayer = true
        }
      })
      if (!isPolygonLayer) {
        layersToRemove.push(layer)
      }
    }
  })
  layersToRemove.forEach(layer => {
    map.removeLayer(layer)
  })
}

export const getHandleCoord = (feature: any) => {
  const { $L } = useNuxtApp()
  const coords = feature.geometry.coordinates[0]
  const midIdx = Math.floor(coords.length / 2)
  const midCoord = coords[midIdx]
  return $L.latLng(midCoord[1], midCoord[0])
}

export const addSegmentsGeoJson = ({
  map,
  $L,
  data,
  selectedSegmentId = null,
  fitBounds = true,
  mapType = 'main',
  mapRegion = 'conus',
}: {
  map: any
  $L: any
  data: any
  selectedSegmentId?: string | null
  fitBounds?: boolean
  mapType?: 'main' | 'report'
  mapRegion?: 'conus' | 'alaska'
}) => {
  const streamSegmentStore = useStreamSegmentStore()
  let { segmentRegion } = storeToRefs(streamSegmentStore)

  // Add each segment individually so we can add hover effects
  // (color change and tooltip) to each segment individually.
  let selectedSegmentLayer: any = null

  let region = segmentRegion.value || mapRegion
  let idProperty = region === 'alaska' ? 'COMID' : 'seg_id_nat'

  let selectedSegment = data.features.find((feature: any) => {
    return feature.properties[idProperty] === selectedSegmentId
  })

  let otherSegments = data.features.filter((feature: any) => {
    return feature.properties[idProperty] !== selectedSegmentId
  })

  // Only add selected segment if it exists
  let orderedSegments = selectedSegment
    ? [...otherSegments, selectedSegment]
    : otherSegments

  orderedSegments.forEach((feature: any) => {
    let isSelected = (selectedSegmentId &&
      feature.properties[idProperty] === selectedSegmentId) as boolean

    let interactive = !isSelected
    let selectedKey = isSelected ? 'selected' : 'unselected'
    // The WFS layers use different property names for outlet status:
    // 'outlet' for Alaska, 'h8_outlet' for CONUS. Use the resolved region
    // (not segmentRegion, which is null on the main map pages).
    let outletProperty = region === 'alaska' ? 'outlet' : 'h8_outlet'
    let outletKey =
      feature.properties[outletProperty] === 1 ? 'outlet' : 'regular'
    let segmentColor = segmentColors[mapType][selectedKey][outletKey]
    let hoverColor = segmentColors[mapType][selectedKey].hover

    let mapZoom = map.getZoom()
    let lineWeight = 4
    let handleRadius = 6
    if (isSelected) {
      lineWeight = 6
    } else if (mapZoom < 9) {
      lineWeight = 3
      handleRadius = 4
    }

    let line = $L.geoJSON(feature, {
      style: {
        weight: lineWeight,
        color: segmentColor,
        interactive: interactive,
      },
    })

    if (isSelected) {
      selectedSegmentLayer = line
    }

    let segmentParts: any[]
    if (isSelected) {
      // No handle for selected segment on report map.
      segmentParts = [line]
    } else {
      // Add a circle marker as a handle for non-selected segments.
      let latlng = getHandleCoord(feature)
      let handle = $L.circleMarker(latlng, {
        radius: handleRadius,
        fillOpacity: 1,
        color: segmentColor,
        fillColor: segmentColor,
        interactive: interactive,
      })
      segmentParts = [line, handle]
    }

    let combinedSegment = $L
      .featureGroup(segmentParts, {
        color: segmentColor,
        fillColor: segmentColor,
      })
      .addTo(map)

    // Set cursor style: normal for selected, pointer for others
    const container =
      combinedSegment.getContainer?.() || combinedSegment._container
    if (container) {
      container.style.cursor = isSelected ? 'default' : 'pointer'
    }

    combinedSegment
      .on('mouseover', function (e: any) {
        if (mapRegion === 'conus') {
          let segmentName = feature.properties.GNIS_NAME
          if (segmentName !== '') {
            line
              .bindTooltip(segmentName, {
                className: 'is-size-6 px-3',
              })
              .openTooltip()
          }
        }
        if (isSelected) {
          return
        }

        combinedSegment.setStyle({
          color: hoverColor,
          fillColor: hoverColor,
        })
      })
      .on('mouseout', function (e: any) {
        line.closeTooltip()
        combinedSegment.setStyle({
          color: segmentColor,
          fillColor: segmentColor,
        })
      })
      .on('click', function (e: any) {
        const streamSegmentStore = useStreamSegmentStore()
        let { segmentId, isLoading } = storeToRefs(streamSegmentStore)
        segmentId.value = null
        isLoading.value = true
        const routePrefix =
          region === 'alaska' ? '/alaska/stream' : '/conus/stream'
        const segId = feature.properties[idProperty]
        window.trackUmamiEvent('segment-click', {
          id: String(segId),
          region,
          map: mapType,
        })
        navigateTo(routePrefix + '/' + segId)
      })
  })

  // Fit bounds to selected segment if one exists
  if (selectedSegmentLayer) {
    if (fitBounds) {
      map.fitBounds(selectedSegmentLayer.getBounds(), { padding: [50, 50] })
    }

    // Only add marker if one doesn't already exist.
    let markerExists = false
    map.eachLayer((layer: any) => {
      if (layer instanceof $L.Marker) {
        markerExists = true
      }
    })

    if (!markerExists) {
      let latlng = getHandleCoord(selectedSegment)
      $L.marker(latlng).addTo(map)
    }
  }
}

// Builds the WFS request base URL for a region's stream segment layer.
const segmentLayerBaseUrl = (mapRegion: 'conus' | 'alaska') => {
  const { $config } = useNuxtApp()
  const wfsBaseUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&outputFormat=application%2Fjson&srsName=EPSG:4326`
  return mapRegion === 'alaska'
    ? `${wfsBaseUrl}&typeName=hydrology%3Aarctic_rivers_segments_joined_3338_simplified_v2`
    : `${wfsBaseUrl}&typeName=hydrology%3Aseg_h8_outlet_stats_simplified_v2`
}

// Builds the WFS request URL for all segments intersecting a lat/lng bounds.
const segmentBboxUrl = (bounds: any, mapRegion: 'conus' | 'alaska') => {
  const segBaseUrl = segmentLayerBaseUrl(mapRegion)
  const minLon = bounds.getWest()
  const maxLon = bounds.getEast()
  const minLat = bounds.getSouth()
  const maxLat = bounds.getNorth()
  return (
    segBaseUrl +
    `&cql_filter=BBOX(the_geom,${minLon},${minLat},${maxLon},${maxLat},'EPSG:4326')`
  )
}

// Fetches (but does not add) the segment GeoJSON for a given bounds. Lets callers
// load segments for a region before moving the map there, so the swap can happen
// atomically without an intermediate empty/moving frame.
export const fetchSegmentsForBounds = async ({
  bounds,
  region = 'conus',
}: {
  bounds: any
  region?: 'conus' | 'alaska'
}) => {
  const streamSegmentStore = useStreamSegmentStore()
  const { segmentRegion } = storeToRefs(streamSegmentStore)
  const mapRegion = segmentRegion.value || region

  const response = await fetch(segmentBboxUrl(bounds, mapRegion))
  if (!response.ok) {
    throw new Error(
      `Failed to fetch segment data: ${response.status} ${response.statusText}`
    )
  }
  return response.json()
}

// Fetches (but does not add) the GeoJSON for a single stream segment. Lets the
// report map fit itself to the segment before its first view is set, so no
// tiles or segments are ever requested for the wrong place.
export const fetchSegmentById = async ({
  segmentId,
  region = 'conus',
}: {
  segmentId: number | string
  region?: 'conus' | 'alaska'
}) => {
  const streamSegmentStore = useStreamSegmentStore()
  const { segmentRegion } = storeToRefs(streamSegmentStore)
  const mapRegion = segmentRegion.value || region

  const idFilter =
    mapRegion === 'alaska' ? `COMID=${segmentId}` : `seg_id_nat=${segmentId}`

  const response = await fetch(
    segmentLayerBaseUrl(mapRegion) + `&cql_filter=${idFilter}`
  )
  if (!response.ok) {
    throw new Error(
      `Failed to fetch segment ${segmentId}: ${response.status} ${response.statusText}`
    )
  }
  return response.json()
}

export const fetchAndAddSegmentsByBounds = ({
  map,
  $L,
  fitBounds = true,
  mapType = 'main',
  region = 'conus',
}: {
  map: any
  $L: any
  fitBounds?: boolean
  mapType?: 'main' | 'report'
  region?: 'conus' | 'alaska'
}) => {
  const streamSegmentStore = useStreamSegmentStore()
  let { segmentId, segmentRegion } = storeToRefs(streamSegmentStore)

  let mapRegion = segmentRegion.value || region

  return fetch(segmentBboxUrl(map.getBounds(), mapRegion))
    .then(response => {
      if (!response.ok) {
        throw new Error(
          `Failed to fetch segment data: ${response.status} ${response.statusText}`
        )
      }
      return response.json()
    })
    .then(data => {
      clearSegmentLayers(map)
      // The selected segment (set only on report pages; null on the main map)
      // gets its selected styling whenever the viewport includes it.
      addSegmentsGeoJson({
        map,
        $L,
        data,
        selectedSegmentId: segmentId.value,
        fitBounds,
        mapType: mapType,
        mapRegion: mapRegion,
      })
    })
    .catch(error => {
      console.error('Error fetching segment data for map bounds:', error)
    })
}
