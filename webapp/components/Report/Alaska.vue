<script setup lang="ts">
import { useStreamSegmentStore } from '~/stores/streamSegment'
import { scenarioFullNames } from '~/types/modelsScenarios'
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
        <SegmentTitle />
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
        <div class="content clamp is-size-5 mb-6">
          <p>
            The chart below is a hydrograph that shows the modeled historical
            mean (white line in center) and range of variation (gray band) with
            the projected scenario&mdash;{{ scenarioFullNames.ssp370 }}. The
            minimum and maximum across four climate model runs are shown (the
            top and bottom lines), and the range of variation for the means are
            shown as a shaded ribbon.
          </p>
        </div>
        <VizHydrograph :stream-hydrograph="streamHydrograph" />
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="content clamp is-size-5 mb-6">
          <p>
            The chart below shows the mean modeled monthly flow rate for the
            historical modeled value (diamond) and with the projected
            scenario&mdash;{{ scenarioFullNames.ssp370 }}. The box plot shows
            the range of values for four climate model runs. Each box plot spans
            from quartile 1 to quartile 3, which is the interquartile range
            (IQR). The second quartile&mdash;the median&mdash;is marked by a
            line inside the box. The whiskers span &#177;1.5 times the
            interquartile range, and outliers are shown as colored dots.
          </p>
        </div>
        <VizMonthlyFlow :stream-monthly-flow="streamMonthlyFlow" />
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="content clamp is-size-5 mb-6">
          <p>
            The chart below shows the modeled annual maximum daily flow rate and
            the date of its occurrence for the historical modeled value
            (diamond) and with the projected scenario,
            {{ scenarioFullNames.ssp370 }}, for four climate model runs. This
            chart can help you see changes in the timing and magnitude of annual
            maximum flow rates.
          </p>
        </div>
        <VizMaxFlowDates :stream-max-flow-dates="streamMaxFlowDates" />
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="content clamp is-size-5 mb-6">
          <p>
            The chart below is a temperature hydrograph that shows the modeled
            historical mean (white line in center) and range of variation (gray
            band) with the projected scenario&mdash;{{
              scenarioFullNames.ssp370
            }}. The minimum and maximum across four climate model runs are shown
            (the top and bottom lines), and the range of variation for the means
            are shown as a shaded ribbon.
          </p>
        </div>
        <VizTemperatureHydrograph :stream-wt-hydrograph="streamWtHydrograph" />
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="content clamp is-size-5 mb-6">
          <p>
            The chart below shows the mean modeled monthly temperature for the
            historical modeled value (diamond) and with the projected
            scenario&mdash;{{ scenarioFullNames.ssp370 }}. The box plot shows
            the range of values for four climate model runs. Each box plot spans
            from quartile 1 to quartile 3, which is the interquartile range
            (IQR). The second quartile&mdash;the median&mdash;is marked by a
            line inside the box. The whiskers span &#177;1.5 times the
            interquartile range, and outliers are shown as colored dots.
          </p>
        </div>
        <VizMonthlyTemperature
          :stream-monthly-temperature="streamMonthlyTemperature"
        />
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="content clamp is-size-5 mb-6">
          <p>
            The chart below shows the modeled annual maximum temperature and the
            date of its occurrence for the historical modeled value (diamond)
            and with the projected scenario,
            {{ scenarioFullNames.ssp370 }}, for four climate model runs. This
            chart can help you see changes in the timing and magnitude of annual
            maximum temperatures.
          </p>
        </div>
        <VizMaxTemperatureDates :stream-max-temp-dates="streamMaxTempDates" />
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h4 class="title is-4">Complete statistics</h4>

        <div class="is-size-5 mb-6">
          <p>
            The projected values in the tables below show the median values
            across the {{ scenarioFullNames.ssp370 }} climate scenario for four
            climate model runs.
          </p>
        </div>
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
