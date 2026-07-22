<script setup lang="ts">
import { computed } from 'vue'
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { segmentId, segmentName } = storeToRefs(streamSegmentStore)
</script>

<template>
  <div class="mb-4">
    <div v-if="segmentName">
      <h3 class="title is-3">Statistics for {{ segmentName }}</h3>
      <h4 class="subtitle is-4">Segment ID #{{ segmentId }}</h4>
    </div>
    <div v-else>
      <h3 class="title is-3">
        Statistics for Stream Segment ID #{{ segmentId }}
      </h3>
    </div>
  </div>
</template>
