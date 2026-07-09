import { defineStore } from 'pinia'
import { ref, shallowRef } from 'vue'

export const useStreamSegmentStore = defineStore('streamSegmentStore', () => {
  const isLoading = ref<boolean>(false)
  const apiSlow = ref<boolean>(false)
  const apiFailed = ref<boolean>(false)

  const segmentId = ref(null)
  const segmentUsgsGageId = ref(null)
  const segmentHuc8Id = ref(null)
  const segmentIsHuc8Outlet = ref(null)
  const segmentRegion = ref(null)
  const segmentName = ref(null)
  const gageId = ref(null)
  const streamSummary = shallowRef(null)
  const streamHydrograph = shallowRef(null)
  const streamMonthlyFlow = shallowRef(null)
  const streamMaxFlowDates = shallowRef(null)
  const streamStats = shallowRef(null)
  const streamMonthlyTemperature = shallowRef(null)
  const streamWtHydrograph = shallowRef(null)
  const streamWtStats = shallowRef(null)
  const streamMaxTempDates = shallowRef(null)
  const appContext = ref<AppContext>('mid')
  const appEra = ref<Era>('2046-2075')
  const { $config } = useNuxtApp()

  const fetchStreamStats = async (): Promise<void> => {
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
            '@/assets/fixtures/conus_output_example.json'
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
      gageId.value = dataResponse['gage_id']
      streamSummary.value = dataResponse['summary']
      streamHydrograph.value = dataResponse['hydrograph']
      streamMonthlyFlow.value = dataResponse['monthly_flow']
      streamMaxFlowDates.value = dataResponse['max_flow_dates']
      streamStats.value = dataResponse['stats']
      streamWtHydrograph.value = dataResponse['wt_hydrograph']
      streamWtStats.value = dataResponse['wt_stats']
      streamMonthlyTemperature.value = dataResponse['monthly_temperature']
      streamMaxTempDates.value = dataResponse['max_temp_dates']
      segmentUsgsGageId.value = dataResponse['gage_id']
      segmentHuc8Id.value = dataResponse['huc8']
      segmentIsHuc8Outlet.value =
        dataResponse['h8_outlet'] || dataResponse['huc8_outlet'] // different key depending on AK vs. CONUS
    } catch {
      console.error('API response does not contain expected data.')
    }
  }

  // Full reset of app data and loading state
  const clearStats = (): void => {
    segmentId.value = null
    segmentUsgsGageId.value = null
    segmentHuc8Id.value = null
    segmentIsHuc8Outlet.value = null
    segmentName.value = null
    gageId.value = null
    streamSummary.value = null
    streamHydrograph.value = null
    streamMonthlyFlow.value = null
    streamMaxFlowDates.value = null
    streamStats.value = null
    streamWtHydrograph.value = null
    streamMonthlyTemperature.value = null
    streamMaxTempDates.value = null
    streamWtStats.value = null
    apiSlow.value = false
    apiFailed.value = false
  }

  return {
    segmentId,
    segmentUsgsGageId,
    segmentHuc8Id,
    segmentIsHuc8Outlet,
    segmentRegion: segmentRegion,
    segmentName,
    gageId,
    streamSummary,
    streamHydrograph,
    streamMonthlyTemperature,
    streamWtHydrograph,
    streamWtStats,
    streamMaxTempDates,
    streamMonthlyFlow,
    streamMaxFlowDates,
    streamStats,
    fetchStreamStats,
    clearStats,
    isLoading,
    apiSlow,
    apiFailed,
    appContext,
    appEra,
  }
})
