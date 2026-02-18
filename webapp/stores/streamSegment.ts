import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useStreamSegmentStore = defineStore('streamSegmentStore', () => {
  const isLoading = ref<boolean>(false)
  const segmentId = ref(null)
  const streamStats = ref(null)
  const streamHydrograph = ref(null)
  const { $config } = useNuxtApp()

  const fetchStreamStats = async (): Promise<void> => {
    let statsRequestUrl = `${$config.public.snapApiUrl}/conus_hydrology/stats/${segmentId.value}`
    let hydrographRequestUrl = `${$config.public.snapApiUrl}/conus_hydrology/modeled_climatology/${segmentId.value}`

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
        statsResponse = await $fetch(statsRequestUrl)
        hydrographResponse = await $fetch(hydrographRequestUrl)
      }
    } finally {
      isLoading.value = false
    }
    streamStats.value = statsResponse
    streamHydrograph.value = hydrographResponse
  }

  const clearStreamStats = async (): Promise<void> => {
    streamStats.value = ref(null)
    streamHydrograph.value = ref(null)
  }

  return {
    streamStats,
    streamHydrograph,
    fetchStreamStats,
    clearStreamStats,
    segmentId,
    isLoading,
  }
})
