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
  preload = false,
}: {
  map: any
  $L: any
  data: any
  selectedSegmentId?: string | null
  fitBounds?: boolean
  mapType?: 'main' | 'report'
  mapRegion?: 'conus' | 'alaska'
  preload?: boolean
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

  let opacity = 1
  if (preload) {
    opacity = 0
  }

  orderedSegments.forEach((feature: any) => {
    let isSelected: boolean = false
    if (segmentRegion.value === 'alaska') {
      isSelected = (selectedSegmentId &&
        feature.properties.COMID === selectedSegmentId) as boolean
    } else {
      isSelected = (selectedSegmentId &&
        feature.properties.seg_id_nat === selectedSegmentId) as boolean
    }

    let interactive = !isSelected
    let selectedKey = isSelected ? 'selected' : 'unselected'
    let outletProperty =
      segmentRegion.value === 'alaska' ? 'outlet' : 'h8_outlet'
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
        opacity: opacity,
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
        opacity: opacity,
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
        navigateTo(routePrefix + '/' + segId)
      })
  })

  // Fit bounds to selected segment if one exists
  if (selectedSegmentLayer) {
    if (fitBounds) {
      map.fitBounds(selectedSegmentLayer.getBounds(), { padding: [50, 50] })
    }

    if (!preload) {
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
}

// Builds the WFS request URL for all segments intersecting a lat/lng bounds.
const segmentBboxUrl = (bounds: any, mapRegion: 'conus' | 'alaska') => {
  const { $config } = useNuxtApp()
  const wfsBaseUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&outputFormat=application%2Fjson&srsName=EPSG:4326`
  const segBaseUrl =
    mapRegion === 'alaska'
      ? `${wfsBaseUrl}&typeName=hydrology%3Aarctic_rivers_segments_joined_3338_simplified`
      : `${wfsBaseUrl}&typeName=hydrology%3Aseg_h8_outlet_stats_simplified`

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
  const { $config } = useNuxtApp()
  const streamSegmentStore = useStreamSegmentStore()
  let { segmentId, segmentRegion } = storeToRefs(streamSegmentStore)

  let mapRegion = segmentRegion.value || region

  const wfsBaseUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&outputFormat=application%2Fjson&srsName=EPSG:4326`
  const segBaseUrl =
    mapRegion === 'alaska'
      ? `${wfsBaseUrl}&typeName=hydrology%3Aarctic_rivers_segments_joined_3338_simplified`
      : `${wfsBaseUrl}&typeName=hydrology%3Aseg_h8_outlet_stats_simplified`

  if (segmentId.value) {
    // Fetch only the selected segment first to determine map bounds.
    // The selected segment will be added with an opacity of 0 until fitBounds is called.
    // It will then be removed and added back to the map with full opacity along with all
    // other viewport segments. This is "preload" mode.
    let selectedSegUrl: string
    if (mapRegion === 'alaska') {
      selectedSegUrl = segBaseUrl + `&cql_filter=COMID=${segmentId.value}`
    } else {
      selectedSegUrl = segBaseUrl + `&cql_filter=seg_id_nat=${segmentId.value}`
    }

    return fetch(selectedSegUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(
            `Failed to fetch selected segment: ${response.status} ${response.statusText}`
          )
        }
        return response.json()
      })
      .then(selectedData => {
        // Add and fit bounds to the selected segment
        addSegmentsGeoJson({
          map,
          $L,
          data: selectedData,
          selectedSegmentId: segmentId.value,
          fitBounds,
          mapType: mapType,
          mapRegion: mapRegion,
          preload: true,
        })

        // Map is now fit to bounds of selected segment. Now fetch everything in map viewport.
        // No selected segment, so just fetch segments in current viewport.
        const bounds = map.getBounds()
        const minLon = bounds.getWest()
        const maxLon = bounds.getEast()
        const minLat = bounds.getSouth()
        const maxLat = bounds.getNorth()

        const segUrl =
          segBaseUrl +
          `&cql_filter=BBOX(the_geom,${minLon},${minLat},${maxLon},${maxLat},'EPSG:4326')`

        return fetch(segUrl)
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
            // Add all viewport segments (including selected)
            addSegmentsGeoJson({
              map,
              $L,
              data: data,
              selectedSegmentId: segmentId.value,
              fitBounds: fitBounds,
              mapType: mapType,
              mapRegion: mapRegion,
            })
          })
      })
      .catch(error => {
        console.error('Error fetching segment data:', error)
      })
  }

  // No selected segment, so just fetch segments in current viewport.
  const bounds = map.getBounds()
  const minLon = bounds.getWest()
  const maxLon = bounds.getEast()
  const minLat = bounds.getSouth()
  const maxLat = bounds.getNorth()

  const segUrl =
    segBaseUrl +
    `&cql_filter=BBOX(the_geom,${minLon},${minLat},${maxLon},${maxLat},'EPSG:4326')`

  return fetch(segUrl)
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
      addSegmentsGeoJson({
        map,
        $L,
        data,
        selectedSegmentId: null,
        fitBounds,
        mapType: mapType,
        mapRegion: mapRegion,
      })
    })
    .catch(error => {
      console.error('Error fetching segment data for map bounds:', error)
    })
}
