<script lang="ts" setup>
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { segmentId, segmentType } = storeToRefs(streamSegmentStore)

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
  throw createError('Stream segment ID not valid')
}

// Set + fetch data.
segmentId.value = segment
segmentType.value = 'alaska'
</script>

<template>
  <section class="section">
    <div class="container">
      <NuxtLink class="content is-size-5" to="/"
        >Go back, pick another place</NuxtLink
      >
    </div>
  </section>
  <Report />
</template>

<style scoped></style>
