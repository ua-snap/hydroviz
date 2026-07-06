<script lang="ts" setup>
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { segmentId, segmentRegion } = storeToRefs(streamSegmentStore)

const route = useRoute()
let segment = parseInt(route.params.segment)

// The min/max values found for the COMID property in the shapefile.
let minId = 81000004
let maxId = 82001714

if (
  !segment ||
  !Number.isInteger(segment) ||
  segment > maxId ||
  segment < minId
) {
  throw createError({
    statusCode: 404,
    message: 'Stream segment ID not valid',
    fatal: true,
  })
}

// Set + fetch data.
segmentId.value = segment
segmentRegion.value = 'alaska'
</script>

<template>
  <Report />
</template>

<style scoped></style>
