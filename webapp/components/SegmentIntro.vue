<script setup lang="ts">
import { computed } from 'vue'
import { huc8s } from '~/assets/conus_huc8'

import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { segmentUsgsGaugeId, segmentHuc8Id, streamSummary, segmentIsHuc8Outlet } =
  storeToRefs(streamSegmentStore)

const lowFlow = computed(() => {
  return streamSummary.value.ma99_hist.value <= 5
})

const USGS_STREAM_GAUGE_URL_BASE =
  'https://waterdata.usgs.gov/monitoring-location/'
</script>
<template>
  <div class="content clamp is-size-5">
    <p>
      This stream segment is
      <span v-if="segmentIsHuc8Outlet">an outflow segment for</span
      ><span v-else>located in</span> the
      <NuxtLink
        :to="{ path: `/${streamSegmentStore.segmentRegion}/huc/${segmentHuc8Id}` }"
        >{{ huc8s[segmentHuc8Id] }} watershed</NuxtLink
      >
      (HUC-8 {{ segmentHuc8Id }}).
    </p>
    <p v-if="segmentUsgsGaugeId">
      This stream segment has a corresponding USGS stream gage,
      {{ segmentUsgsGaugeId }}.
      <a rel="external" :href="USGS_STREAM_GAUGE_URL_BASE + segmentUsgsGaugeId"
        >Go to the web page for that gage</a
      >.
    </p>
    <p v-if="lowFlow">
      <strong>This stream segment has a low mean annual flow.</strong>
      Headwaters and other small or intermittent streams have high statistical
      variability. Charts and visualizations may look strange for this stream
      segment.
    </p>
    <p>
      All data in this report can be downloaded in CSV and other formats
      <NuxtLink to="#get-and-use">at the bottom of this page</NuxtLink>.
    </p>
  </div>
</template>

<style lang="scss" scoped></style>
