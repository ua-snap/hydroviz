<script lang="ts" setup>
const { $L, $config } = useNuxtApp()
import { useStreamSegmentStore } from '~/stores/streamSegment'

const streamSegmentStore = useStreamSegmentStore()
const route = useRoute()

let { hucId, segmentRegion } = storeToRefs(streamSegmentStore)

let huc = route.params.huc
if (!/^\d{8}$/.test(huc)) {
  throw createError('HUC ID not valid')
} else {
  hucId.value = parseInt(huc)
  segmentRegion.value = 'conus'
}
</script>

<template>
  <Report />
</template>

<style scoped></style>
