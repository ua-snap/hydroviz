<script lang="ts" setup>
const { $L, $config } = useNuxtApp()
import { useStreamSegmentStore } from '~/stores/streamSegment'

const streamSegmentStore = useStreamSegmentStore()
const route = useRoute()

let { hucId, segmentRegion } = storeToRefs(streamSegmentStore)

let huc = route.params.huc
if (!/^\d{8}$/.test(huc) && !/^[A-Z0-9]{4}$/.test(huc)) {
  throw createError('HUC ID not valid')
} else {
  hucId.value = huc
  segmentRegion.value = 'alaska'
}
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
