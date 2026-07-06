<script lang="ts" setup>
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { segmentId } = storeToRefs(streamSegmentStore)

const route = useRoute()
let segment = parseInt(route.params.segment)

// Sanity test input, numeric + integer + no bigger than total number of segments=56460
if (!segment || !Number.isInteger(segment) || segment > 56460 || segment < 0) {
  throw createError({
    statusCode: 404,
    message: 'Stream segment ID not valid',
    fatal: true,
  })
}

// Set + fetch data.
segmentId.value = segment
</script>

<template>
  <Report />
</template>

<style scoped></style>
