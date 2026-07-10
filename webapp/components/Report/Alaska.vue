<script setup lang="ts">
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let {
  streamStats,
  streamHydrograph,
  streamMonthlyFlow,
  streamMaxFlowDates,
  streamWtStats,
  streamWtHydrograph,
  streamMonthlyTemperature,
  streamMaxTempDates,
  segmentId,
  segmentName,
} = storeToRefs(streamSegmentStore)

const router = useRouter()

// Returns to the map, restoring its zoom/center/phase via browser history when
// this report was reached from the map. On a direct visit (shared link) there
// is no in-app history to go back to, so fall back to the home page.
const goBackToMap = () => {
  if (window.history.state?.back) {
    router.back()
  } else {
    navigateTo('/')
  }
}

onMounted(() => {
  streamSegmentStore.fetchStreamStats()
})

onUnmounted(() => {
  streamSegmentStore.clearStats()
})
</script>

<template>
  <section class="section pb-0">
    <div class="container">
      <a class="content is-size-5" href="/" @click.prevent="goBackToMap"
        >&larr; Go back, choose another segment</a
      >
    </div>
  </section>
  <Loading />
  <div v-if="streamStats">
    <section class="section">
      <div class="container">
        <h3 class="title is-3">
          Statistics for {{ segmentName }}
          <span class="segmentId">ID{{ segmentId }}</span>
        </h3>
        <SegmentIntro />
        <ReportMap class="my-6" />
        <DataSentences />
      </div>

      <div class="container">
        <div class="content clamp is-size-5 mt-6">
          <p>
            <strong>This web tool shows summarized information</strong> to
            convey trends shown in the data.
            <CsvDownload />
          </p>
          <p>
            All data on this page show a
            <strong>higher emissions</strong> scenario with four runs of one
            climate model, the Community Earth System Model 2 (CESM2). The
            scenario selected is &ldquo;Regional Rivalry&rdquo;, or SSP3-7.0,
            which projects one of the higher-emissions futures modeled for this
            century: greenhouse gas output and radiative forcing climb steadily
            to about 7 watts per square meter by 2100, driven by continued heavy
            fossil fuel use and weak global climate cooperation, placing it
            between the &ldquo;medium&rdquo; and &ldquo;worst-case&rdquo;
            pathways.
          </p>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <VizHydrograph :stream-hydrograph="streamHydrograph" />
      </div>
    </section>
    <section class="section">
      <div class="container">
        <VizMonthlyFlow :stream-monthly-flow="streamMonthlyFlow" />
      </div>
    </section>
    <section class="section">
      <div class="container">
        <VizMaxFlowDates :stream-max-flow-dates="streamMaxFlowDates" />
      </div>
    </section>

    <section class="section">
      <div class="container">
        <VizTemperatureHydrograph :stream-wt-hydrograph="streamWtHydrograph" />
      </div>
    </section>
    <section class="section">
      <div class="container">
        <VizMonthlyTemperature
          :stream-monthly-temperature="streamMonthlyTemperature"
        />
      </div>
    </section>
    <section class="section">
      <div class="container">
        <VizMaxTemperatureDates :stream-max-temp-dates="streamMaxTempDates" />
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h4 class="title is-4">Complete statistics</h4>

        <StatsTable
          :stream-stats="streamStats"
          category="magnitude"
          tableTitle="Magnitude Statistics"
        />
        <StatsTable
          :stream-stats="streamStats"
          category="frequency"
          tableTitle="Frequency Statistics"
        />
        <StatsTable
          :stream-stats="streamStats"
          category="duration"
          tableTitle="Duration Statistics"
        />
        <StatsTable
          :stream-stats="streamStats"
          category="timing"
          tableTitle="Timing Statistics"
        />
        <StatsTable
          :stream-stats="streamStats"
          category="rate_of_change"
          tableTitle="Rate of Change Statistics"
        />
        <StatsTable
          :wt-stats="streamWtStats"
          category="water_temperature_annual"
          tableTitle="Annual Water Temperature Statistics"
        />
        <StatsTable
          :wt-stats="streamWtStats"
          category="water_temperature_minimum_monthly"
          tableTitle="Minimum Monthly Mean Water Temperature"
        />
        <StatsTable
          :wt-stats="streamWtStats"
          category="water_temperature_mean_monthly"
          tableTitle="Mean Monthly Water Temperature"
        />
        <StatsTable
          :wt-stats="streamWtStats"
          category="water_temperature_maximum_monthly"
          tableTitle="Maximum Monthly Mean Water Temperature"
        />
      </div>
    </section>
    <GetAndUse />
  </div>
</template>

<style lang="scss" scoped></style>
