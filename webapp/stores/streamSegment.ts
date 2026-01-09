import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useStreamSegmentStore = defineStore('streamSegmentStore', () => {
  const isLoading = ref<boolean>(false)
  const segmentId = ref(null)
  const segmentName = ref(null)
  const streamStats = ref(null)
  const streamHydrograph = ref(null)
  const { $config } = useNuxtApp()

  const fetchStreamStats = async (): Promise<void> => {
    let statsRequestUrl = `${$config.public.snapApiUrl}/conus_hydrology/stats/${segmentId.value}`
    let hydrographRequestUrl = `${$config.public.snapApiUrl}/conus_hydrology/hydrograph/${segmentId.value}`

    streamStats.value = null
    streamHydrograph.value = null

    // Needs error checking, etc.
    isLoading.value = true
    try {
      const statsResponse = await $fetch(statsRequestUrl)
      streamStats.value = statsResponse

      const hydrographResponse = await $fetch(hydrographRequestUrl)
      streamHydrograph.value = hydrographResponse
    } finally {
      isLoading.value = false
    }
  }

  return {
    streamStats: streamStats,
    streamHydrograph: streamHydrograph,
    fetchStreamStats,
    segmentName,
    segmentId,
    isLoading,
  }
})
