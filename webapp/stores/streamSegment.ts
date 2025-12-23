import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useStreamSegmentStore = defineStore('streamSegmentStore', () => {
  const isLoading = ref<boolean>(false)
  const segmentId = ref(null)
  const segmentName = ref(null)
  const streamStats = ref(null)
  const { $config } = useNuxtApp()

  const fetchStreamStats = async (): Promise<void> => {
    let requestUrl = `${$config.public.snapApiUrl}/conus_hydrology/${segmentId.value}`
    streamStats.value = null

    // Needs error checking, etc.
    isLoading.value = true
    try {
      const res = await $fetch(requestUrl)
      streamStats.value = res[segmentId.value]['stats']
    } finally {
      isLoading.value = false
    }
  }

  return {
    streamStats: streamStats,
    fetchStreamStats,
    segmentName,
    segmentId,
    isLoading,
  }
})
