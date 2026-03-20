<script setup lang="ts">
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { isLoading, apiSlow, apiFailed } = storeToRefs(streamSegmentStore)
</script>
<template>
  <div v-if="isLoading" class="content is-size-4">
    <p v-if="apiSlow">This is taking longer than usual. Hold tight&hellip;</p>
    <p v-else>Loading data&hellip; this can take a minute or two.</p>
    <progress class="progress" />
  </div>
  <div v-else-if="apiFailed" class="content is-size-4">
    <p>
      ⚠️ Unable to access data for this stream. We are working to resolve this
      issue and apologize for the inconvenience.
    </p>
  </div>
</template>
