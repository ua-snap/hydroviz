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
      >modeled daily streamflow climatologies</a
    >
    in CSV format for analysis in a spreadsheet.</span
  >
</template>
