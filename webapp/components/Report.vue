<script setup lang="ts">
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let {
  streamStats,
  streamHydrograph,
  streamMonthlyFlow,
  streamMinMaxFlowDates,
  hucId,
  segmentId,
  segmentName,
  appContext,
} = storeToRefs(streamSegmentStore)

onMounted(() => {
  // Prefer HUC mode when both hucId and segmentId are set so behavior matches ReportMap
  if (hucId.value !== null) {
    streamSegmentStore.fetchHucStats()
  } else if (segmentId.value !== null) {
    streamSegmentStore.fetchStreamStats()
  }
})
onUnmounted(() => {
  streamSegmentStore.clearStats()
})
</script>

<template>
  <section class="section">
    <div class="container">
      <Loading />
    </div>
  </section>

  <div v-if="streamStats">
    <section class="section">
      <div class="container">
        <h3 class="title is-3">
          Statistics for {{ segmentName }}
          <span class="segmentId">ID{{ segmentId }}</span>
        </h3>
        <ReportMap class="my-6" />
        <div class="content is-size-5">
          Introduction to the report goes here. We can pull some summarized info
          about the specific stream segment in order to highlight aspects of
          uncertainty and some succinct characterization of net change over
          time.
        </div>
        <DataSentences />
      </div>
    </section>
    <StickyToggle />
    <section class="section">
      <div class="container">
        <h4 class="title is-4">Hydrograph</h4>
        <VizHydrograph :stream-hydrograph="streamHydrograph" />
      </div>
    </section>
    <section class="section">
      <div class="container">
        <h4 class="title is-4">Magnitude</h4>
        <VizMonthlyFlow :stream-monthly-flow="streamMonthlyFlow" />
        <div class="mt-6 block content is-size-5">
          <p v-if="appContext == 'mid'">
            The projected values in the table below show the median values
            across the Stabilizing High (RCP 6.0) climate scenario for 13 climate
            models. This represents the middle-of-the-road for future model
            projections in the CMIP5 family of datasets.
          </p>
          <p v-if="appContext == 'extremes'">
            The projected values in the table below show the extreme values
            across two climate scenarios for 13 climate models. The values in
            the &lsquo;Minimum, Stabilizing (RCP 4.5)&rsquo; column are the
            minimum values across all 13 climate models, and the values in
            the &lsquo;Maximum, Increasing Emissions (RCP 8.5)&rsquo; column are
            the maximum values across all 13 climate models.
          </p>
        </div>
        <StatsTable
          :stream-stats="streamStats"
          category="magnitude"
          tableTitle="Magnitude Statistics"
        />
      </div>
    </section>
    <section class="section">
      <div class="container">
        <h4 class="title is-4">Frequency</h4>
        <StatsTable
          :stream-stats="streamStats"
          category="frequency"
          tableTitle="Frequency Statistics"
        />
      </div>
    </section>
    <section class="section">
      <div class="container">
        <h4 class="title is-4">Duration</h4>
        <StatsTable
          :stream-stats="streamStats"
          category="duration"
          tableTitle="Duration Statistics"
        />
      </div>
    </section>
    <section class="section">
      <div class="container">
        <h4 class="title is-4">Timing</h4>
        <VizMinMaxFlowDates
          :stream-min-max-flow-dates="streamMinMaxFlowDates"
        />
        <StatsTable
          :stream-stats="streamStats"
          category="timing"
          tableTitle="Timing Statistics"
        />
      </div>
    </section>
    <section class="section">
      <div class="container">
        <h4 class="title is-4">Rate of change statistics</h4>
        <!-- <StatsTable :stream-stats="streamStats" category="rate_of_change" /> -->
      </div>
    </section>
  </div>
</template>

<style lang="scss" scoped></style>
