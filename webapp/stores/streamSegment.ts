import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useStreamSegmentStore = defineStore('streamSegmentStore', () => {
  const isLoading = ref<boolean>(false)
  const apiSlow = ref<boolean>(false)
  const apiFailed = ref<boolean>(false)

  const segmentId = ref(null)
  const segmentName = ref(null)
  const streamStats = ref(null)
  const streamHydrograph = ref(null)
  const { $config } = useNuxtApp()

  const fetchStreamStats = async (): Promise<void> => {
    let statsRequestUrl = `${$config.public.snapApiUrl}/conus_hydrology/stats/${segmentId.value}`
    let hydrographRequestUrl = `${$config.public.snapApiUrl}/conus_hydrology/modeled_climatology/${segmentId.value}`

    apiSlow.value = false
    apiFailed.value = false

    // BUG: this causes the front end render to fail because
    // it still tries to render the chart (!)
    streamStats.value = null
    streamHydrograph.value = null
    var statsResponse, hydrographResponse

    // Needs error checking, etc.
    isLoading.value = true
    try {
      if ($config.public.staticFixtures) {
        console.log('Using static fixtures for hydroviz API data')
        statsResponse = await import('@/assets/fixtures/stats.json')
        hydrographResponse = await import(
          '@/assets/fixtures/modeled_climatology.json'
        )
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
            statsResponse = await $fetch(statsRequestUrl, {
              signal: controller.signal,
            })
            hydrographResponse = await $fetch(hydrographRequestUrl, {
              signal: controller.signal,
            })
          } finally {
            clearTimeout(timeout)
          }

          clearTimeout(slowTimer)
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
    }

    // Treat the failure of either API endpoint as a total data failure
    // to avoid partial/unpredictable webapp states. In production, it's
    // unlikely that one endpoint will succeed when the other fails, so
    // it's probably not worth trying to handle them separately.
    if (statsResponse.ok && hydrographResponse.ok) {
      streamStats.value = statsResponse
      streamHydrograph.value = hydrographResponse
    }
  }

  return {
    streamStats,
    streamHydrograph,
    fetchStreamStats,
    segmentName,
    segmentId,
    isLoading,
    apiSlow,
    apiFailed,
  }
})
