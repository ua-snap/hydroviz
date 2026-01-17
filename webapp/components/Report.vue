<script setup lang="ts">
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { streamStats, segmentName } = storeToRefs(streamSegmentStore)
</script>

<template>
  <section class="section report">
    <div class="container">
      <Loading />
      <div v-if="streamStats">
        <h3 class="title is-3">Statistics for {{ segmentName }}</h3>
        <VizHydrograph />
        <StatsTable />
      </div>
    </div>
  </section>
</template>

<style lang="scss" scoped></style>
