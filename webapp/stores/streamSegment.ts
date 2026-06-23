import { defineStore } from 'pinia'
import { ref, shallowRef } from 'vue'

export const useStreamSegmentStore = defineStore('streamSegmentStore', () => {
  const isLoading = ref<boolean>(false)
  const apiSlow = ref<boolean>(false)
  const apiFailed = ref<boolean>(false)

  const segmentId = ref(null)
  const segmentRegion = ref(null)
  const segmentName = ref(null)
  const hucId = ref(null)
  const streamSummary = shallowRef(null)
  const streamHydrograph = shallowRef(null)
  const streamMonthlyFlow = shallowRef(null)
  const streamMaxFlowDates = shallowRef(null)
  const streamStats = shallowRef(null)
  const appContext = ref<AppContext>('mid')
  const appEra = ref<Era>('2046-2075')
  const { $config } = useNuxtApp()

  // If we have a hucId but not a segmentId, set segmentId to HUC outlet.
  const fetchHucStats = async (): Promise<void> => {
    isLoading.value = true
    const hucBaseUrl =
      segmentRegion.value === 'alaska'
        ? `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Aarctic_rivers_segments_joined_3338_simplified&outputFormat=application%2Fjson&srsName=EPSG:4326`
        : `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Aseg_h8_outlet_stats_simplified_subset&outputFormat=application%2Fjson&srsName=EPSG:4326`
    const hucFilter =
      segmentRegion.value === 'alaska'
        ? `&cql_filter=ID_2='${hucId.value}'`
        : `&cql_filter=huc8=${hucId.value}`
    let hucUrl = `${hucBaseUrl}${hucFilter}`

    try {
      const response = await fetch(hucUrl)
      const data = await response.json()

      apiFailed.value = false

      const features = Array.isArray(data?.features) ? data.features : []
      if (features.length === 0) {
        console.error('No features returned for HUC:', hucId.value)
        return
      }

      // Find the first feature in the response where properties.h8_outlet is 1.
      // TODO: What do we do if there is more than 1 outlet stream segment?
      let outletFeature = null
      let outletPropertyName =
        segmentRegion.value === 'alaska' ? 'outlet' : 'h8_outlet'
      outletFeature = features.find(
        (feature: any) => feature?.properties?.[outletPropertyName] === 1
      )

      if (!outletFeature || !outletFeature.properties) {
        console.error('No outlet feature found for HUC:', hucId.value)
        return
      }

      segmentId.value =
        segmentRegion.value === 'alaska'
          ? outletFeature.properties.COMID
          : outletFeature.properties.seg_id_nat

      if (segmentId.value != null) {
        await fetchStreamStats()
      }
    } catch (error) {
      console.error('Error fetching HUC data:', error)
    } finally {
      isLoading.value = false
    }
  }

  const fetchStreamStats = async (): Promise<void> => {
    // BUG: this causes the front end render to fail because
    // it still tries to render the chart (!)
    segmentName.value = null
    streamSummary.value = null
    streamHydrograph.value = null
    streamMonthlyFlow.value = null
    streamMaxFlowDates.value = null
    streamStats.value = null
    var dataResponse

    let dataUrl: string
    if (segmentRegion.value === 'alaska') {
      dataUrl = `${$config.public.snapApiUrl}/arctic_hydrology/hydroviz/${segmentId.value}`
    } else {
      dataUrl = `${$config.public.snapApiUrl}/conus_hydrology/hydroviz/${segmentId.value}`
    }

    // Needs error checking, etc.
    isLoading.value = true
    try {
      if ($config.public.staticFixtures) {
        console.log('Using static fixtures for hydroviz API data')
        if (segmentRegion.value === 'alaska') {
          dataResponse = await import(
            '@/assets/fixtures/alaska_output_example.json'
          )
        } else {
          dataResponse = await import(
            // TEMP FOR TESTING
            // '@/assets/fixtures/conus_output_example.json'
            '@/assets/fixtures/test-roundSigFig-fixture-DELETE.json'
          )
        }
      } else {
        try {
          // Used to track mildly slow data API responses that don't abort.
          const slowTimer = setTimeout(() => {
            apiSlow.value = true
          }, 10000)

          // Used to track very slow API responses that do abort.
          const controller = new AbortController()
          const timeout = setTimeout(() => {
            controller.abort()
          }, 60000)

          try {
            dataResponse = await $fetch(dataUrl, {
              signal: controller.signal,
            })
          } finally {
            clearTimeout(timeout)
            clearTimeout(slowTimer)
          }
        } catch (error: any) {
          // If API is unreachable, returns error, or times out.
          if (
            !error?.statusCode ||
            (error?.statusCode >= 400 && error?.statusCode < 600)
          ) {
            apiFailed.value = true
          }
        }
      }
    } finally {
      isLoading.value = false
      apiSlow.value = false
    }

    try {
      segmentName.value = dataResponse['name']
      streamSummary.value = dataResponse['summary']
      streamHydrograph.value = dataResponse['hydrograph']
      streamMonthlyFlow.value = dataResponse['monthly_flow']
      streamMaxFlowDates.value = dataResponse['max_flow_dates']
      streamStats.value = dataResponse['stats']
    } catch {
      console.error('API response does not contain expected data.')
    }
  }

  const clearStats = (): void => {
    segmentId.value = null
    segmentRegion.value = null
    segmentName.value = null
    streamSummary.value = null
    streamHydrograph.value = null
    streamMonthlyFlow.value = null
    streamMaxFlowDates.value = null
    streamStats.value = null
    hucId.value = null
  }

  return {
    segmentId,
    segmentRegion: segmentRegion,
    segmentName,
    streamSummary,
    streamHydrograph,
    streamMonthlyFlow,
    streamMaxFlowDates,
    streamStats,
    fetchStreamStats,
    fetchHucStats,
    clearStats,
    hucId,
    isLoading,
    apiSlow,
    apiFailed,
    appContext,
    appEra,
  }
})
