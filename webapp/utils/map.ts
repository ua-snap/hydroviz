export const getHandleCoord = (feature: any) => {
  const { $L } = useNuxtApp()
  const coords = feature.geometry.coordinates[0]
  const midIdx = Math.floor(coords.length / 2)
  const midCoord = coords[midIdx]
  return $L.latLng(midCoord[1], midCoord[0])
}

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

export const addSegmentsGeoJson = ({
  map,
  $L,
  data,
  layers,
  selectedSegmentId = null,
  fitBounds = true,
  mapType = 'main',
}: {
  map: any
  $L: any
  data: any
  layers?: any[]
  selectedSegmentId?: string | null
  fitBounds: boolean
  mapType?: 'main' | 'report'
}) => {
  // Add each segment individually so we can add hover effects
  // (color change and tooltip) to each segment individually.
  let selectedSegmentLayer: any = null

  let selectedSegment = data.features.find((feature: any) => {
    return feature.properties.seg_id_nat === selectedSegmentId
  })

  let otherSegments = data.features.filter((feature: any) => {
    return feature.properties.seg_id_nat !== selectedSegmentId
  })

  // Only add selected segment if it exists
  let orderedSegments = selectedSegment
    ? [...otherSegments, selectedSegment]
    : otherSegments

  orderedSegments.forEach((feature: any) => {
    const isSelected =
      selectedSegmentId && feature.properties.seg_id_nat === selectedSegmentId

    let interactive = !isSelected

    let selectedKey = isSelected ? 'selected' : 'unselected'
    let outletKey = feature.properties.h8_outlet === 1 ? 'outlet' : 'regular'
    let segmentColor = segmentColors[mapType][selectedKey][outletKey]
    let hoverColor = segmentColors[mapType][selectedKey].hover

    let line = $L.geoJSON(feature, {
      style: {
        weight: isSelected ? 5 : 3,
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
        radius: 4,
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
        let segmentName = feature.properties.GNIS_NAME
        if (segmentName !== '') {
          line
            .bindTooltip(segmentName, {
              className: 'is-size-6 px-3',
            })
            .openTooltip()
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
        let { hucId, segmentId, isLoading } = storeToRefs(streamSegmentStore)
        segmentId.value = feature.properties.seg_id_nat
        hucId.value = null
        segmentId.value = null
        isLoading.value = true
        navigateTo('/conus/' + feature.properties.seg_id_nat)
      })
    if (layers) {
      layers.push(combinedSegment)
    }
  })

  // Fit bounds to selected segment if one exists
  if (selectedSegmentLayer) {
    if (fitBounds) {
      map.fitBounds(selectedSegmentLayer.getBounds(), { padding: [50, 50] })
    }

    let latlng = getHandleCoord(selectedSegment)
    $L.marker(latlng).addTo(map)
  }
}

export const fetchAndAddSegmentsByBounds = ({
  map,
  $L,
  segBaseUrl,
  layers,
  selectedSegmentId = null,
  fitBounds = true,
  mapType = 'main',
}: {
  map: any
  $L: any
  segBaseUrl: string
  layers?: any[]
  selectedSegmentId?: string | null | undefined
  fitBounds?: boolean
  mapType?: 'main' | 'report'
}) => {
  if (selectedSegmentId) {
    // Fetch only the selected segment first to determine map bounds.
    const selectedSegUrl = segBaseUrl + `seg_id_nat=${selectedSegmentId}`
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
          layers,
          selectedSegmentId,
          fitBounds,
          mapType: mapType,
        })

        // Map is now fit to bounds of selected segment. Now fetch everything in map viewport.
        const bounds = map.getBounds()
        const minLon = bounds.getWest()
        const maxLon = bounds.getEast()
        const minLat = bounds.getSouth()
        const maxLat = bounds.getNorth()
        const segUrl =
          segBaseUrl +
          `INTERSECTS(the_geom,ENVELOPE(${minLon},${maxLon},${minLat},${maxLat}))`

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
            // Filter out the selected segment since we already added it
            addSegmentsGeoJson({
              map,
              $L,
              data: data,
              layers,
              selectedSegmentId: selectedSegmentId,
              fitBounds: fitBounds,
              mapType: mapType,
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
    `INTERSECTS(the_geom,ENVELOPE(${minLon},${maxLon},${minLat},${maxLat}))`

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
      addSegmentsGeoJson({
        map,
        $L,
        data,
        layers,
        selectedSegmentId,
        fitBounds,
        mapType: mapType,
      })
    })
    .catch(error => {
      console.error('Error fetching segment data for map bounds:', error)
    })
}
