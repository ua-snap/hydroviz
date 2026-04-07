<script lang="ts" setup>
import { computed } from 'vue'
const { $config } = useNuxtApp()
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { segmentId } = storeToRefs(streamSegmentStore)
const props = defineProps({
  streamId: {
    type: Number,
    required: true,
  },
})
</script>

<template>
  <span
    >Download
    <a
      :href="
        $config.public.snapApiUrl +
        '/conus_hydrology/stats/' +
        segmentId +
        '?format=csv'
      "
      >complete modeled hydrologic statistics</a
    >
    or
    <a
      :href="
        $config.public.snapApiUrl +
        '/conus_hydrology/modeled_climatology/' +
        segmentId +
        '?format=csv'
      "
      >modeled daily streamflow climatologies</a
    >
    in CSV format for analysis in a spreadsheet.</span
  >
</template>
