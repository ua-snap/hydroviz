<script setup lang="ts">
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { isLoading } = storeToRefs(streamSegmentStore)
</script>
<template>
  <div v-if="isLoading" class="content is-size-4">
    <p>Loading data&hellip; this can take a minute or two.</p>
    <progress class="progress" />
  </div>
</template>
