import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useStreamSegmentStore = defineStore('streamSegmentStore', () => {
  const segmentId = ref(null)
  const segmentName = ref(null)
  const streamStats = ref(null)
  const { $config } = useNuxtApp()

  const fetchStreamStats = async (): Promise<void> => {
    let requestUrl = `${$config.public.snapApiUrl}/conus_hydrology/${segmentId.value}`

    // Needs error checking, etc.
    const res = await $fetch(requestUrl)
    streamStats.value = res[segmentId.value]['stats']
  }

  return {
    streamStats: streamStats,
    fetchStreamStats,
    segmentName,
    segmentId,
  }
})
