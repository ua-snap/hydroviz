<script lang="ts" setup>
const { $L, $config } = useNuxtApp()
import { useStreamSegmentStore } from '~/stores/streamSegment'

const streamSegmentStore = useStreamSegmentStore()
const route = useRoute()

let { hucId } = storeToRefs(streamSegmentStore)

let huc = route.params.huc
if (!/^\d{8}$/.test(huc)) {
  throw createError('HUC ID not valid')
} else {
  hucId.value = parseInt(huc)
}
</script>

<template>
  <h1 class="title is-3">HUC ID {{ huc }}</h1>
  <NuxtLink to="/">Go back, pick another place</NuxtLink>
  <Report />
</template>

<style scoped></style>
