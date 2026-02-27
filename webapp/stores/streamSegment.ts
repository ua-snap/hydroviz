import { defineStore } from 'pinia'
import { ref, shallowRef } from 'vue'

export const useStreamSegmentStore = defineStore('streamSegmentStore', () => {
  const isLoading = ref<boolean>(false)
  const segmentId = ref(null)
  const hucId = ref(null)
  const streamStats = shallowRef(null)
  const streamHydrograph = shallowRef(null)
  const { $config } = useNuxtApp()

  // If we have a hucId but not a segmentId, set segmentId to HUC outlet.
  const fetchHucStats = async (): Promise<void> => {
    isLoading.value = true
    const hucBaseUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Aseg_h8_outlet_stats_simplified&outputFormat=application%2Fjson&srsName=EPSG:4326&cql_filter=huc8=`
    let hucUrl = hucBaseUrl + hucId.value
    try {
      const response = await fetch(hucUrl)
      const data = await response.json()

      const features = Array.isArray(data?.features) ? data.features : []
      if (features.length === 0) {
        console.error('No features returned for HUC:', hucId.value)
        return
      }

      // Find the first feature in the response where properties.h8_outlet is 1.
      // TODO: What do we do if there is more than 1 outlet stream segment?
      const outletFeature = features.find(
        (feature: any) => feature?.properties?.h8_outlet === 1
      )

      if (!outletFeature || !outletFeature.properties) {
        console.error('No outlet feature found for HUC:', hucId.value)
        return
      }

      segmentId.value = outletFeature.properties.seg_id_nat

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
    streamStats.value = null
    streamHydrograph.value = null
    var statsResponse, hydrographResponse

    let statsRequestUrl = `${$config.public.snapApiUrl}/conus_hydrology/stats/${segmentId.value}`
    let hydrographRequestUrl = `${$config.public.snapApiUrl}/conus_hydrology/modeled_climatology/${segmentId.value}`

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

  const clearStats = (): void => {
    streamStats.value = null
    streamHydrograph.value = null
    segmentId.value = null
    hucId.value = null
  }

  return {
    streamStats,
    streamHydrograph,
    fetchStreamStats,
    fetchHucStats,
    clearStats,
    segmentId,
    hucId,
    isLoading,
  }
})
