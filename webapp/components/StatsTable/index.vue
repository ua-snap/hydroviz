<script setup lang="ts">
const props = defineProps(['streamStats', 'category', 'tableTitle'])
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { segmentRegion } = storeToRefs(streamSegmentStore)
let region = segmentRegion.value === 'alaska' ? 'alaska' : 'conus'
</script>

<template>
  <StatsTableAlaska
    v-if="region === 'alaska'"
    :stream-stats="streamStats"
    :category="category"
    :table-title="tableTitle"
  />
  <StatsTableConus
    v-else
    :stream-stats="streamStats"
    :category="category"
    :table-title="tableTitle"
  />
</template>
