<script lang="ts" setup>
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { segmentId, segmentRegion, appContext } = storeToRefs(streamSegmentStore)

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

// Alaska reports don't offer the middle-of-the-road/future-extremes toggle,
// so clear any "extremes" context carried over from a CONUS report.
appContext.value = 'mid'
</script>

<template>
  <ReportAlaska />
</template>

<style scoped></style>
