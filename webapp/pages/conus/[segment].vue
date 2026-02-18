<script lang="ts" setup>
import { onUnmounted } from 'vue'
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { segmentId } = storeToRefs(streamSegmentStore)

const route = useRoute()
let segment = parseInt(route.params.segment)

// Sanity test input, numeric + integer + no bigger than total number of segments=56460
if (!segment || !Number.isInteger(segment) || segment > 56460 || segment < 0) {
  throw createError('Stream segment ID not valid')
}

// Set + fetch data.
segmentId.value = segment
streamSegmentStore.fetchStreamStats()

onUnmounted(() => {
  streamSegmentStore.clearStreamStats()
})
</script>

<template>
  <h1 class="title is-3">Stream Segment ID {{ segment }}</h1>
  <NuxtLink to="/">Go back, pick another place</NuxtLink>
  <Report />
</template>

<style scoped></style>
