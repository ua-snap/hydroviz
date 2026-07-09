<script lang="ts" setup>
const { $config } = useNuxtApp()
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { segmentId, segmentRegion } = storeToRefs(streamSegmentStore)

const hydrologyPath = computed(() => {
  return segmentRegion.value === 'alaska'
    ? '/arctic_hydrology'
    : '/conus_hydrology'
})

const trackCsvDownload = (type: 'stats' | 'climatology') => {
  window.trackUmamiEvent('csv-download', {
    type,
    segment: String(segmentId.value),
    region: segmentRegion.value ?? undefined,
  })
}
</script>

<template>
  <span
    >Download
    <a
      :href="
        $config.public.snapApiUrl +
        hydrologyPath +
        '/stats/' +
        segmentId +
        '?format=csv'
      "
      @click="trackCsvDownload('stats')"
      >complete modeled hydrologic statistics</a
    >
    or
    <a
      :href="
        $config.public.snapApiUrl +
        hydrologyPath +
        '/modeled_climatology/' +
        segmentId +
        '?format=csv'
      "
      @click="trackCsvDownload('climatology')"
      >modeled daily streamflow climatologies</a
    >
    in CSV format for analysis in a spreadsheet.</span
  >
</template>
