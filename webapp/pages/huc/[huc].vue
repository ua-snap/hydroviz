<script lang="ts" setup>
const { $L, $config } = useNuxtApp()
import { useStreamSegmentStore } from '~/stores/streamSegment'

const streamSegmentStore = useStreamSegmentStore()
let { hucId } = storeToRefs(streamSegmentStore)

const route = useRoute()
let huc = parseInt(route.params.huc)
hucId.value = huc
</script>

<template>
  <h1 class="title is-3">HUC ID {{ huc }}</h1>
  <NuxtLink to="/">Go back, pick another place</NuxtLink>
  <Report />
</template>

<style scoped></style>
