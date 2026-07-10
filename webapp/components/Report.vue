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
  segmentRegion,
  appContext,
} = storeToRefs(streamSegmentStore)
import { scenarioFullNames } from '~/types/modelsScenarios'

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
        </div>
      </div>
    </section>
    <!-- StickyToggle must be outside of section/container wrappers -->
    <StickyToggle v-if="segmentRegion == 'conus'" />
    <section class="section">
      <div class="container">
        <div class="content clamp is-size-5 mb-6">
          <p v-if="segmentRegion == 'conus' && appContext == 'mid'">
            The chart below is a hydrograph that shows the modeled historical
            mean (white line in center) and range of variation (gray band) with
            the projected middle-of-the-road climate scenario&mdash;{{
              scenarioFullNames.rcp60
            }}. The minimum and maximum across 13 climate models are shown (the
            top and bottom lines), and the range of variation for the means are
            shown as a shaded ribbon.
          </p>
          <p v-if="segmentRegion == 'conus' && appContext == 'extremes'">
            The charts below are hydrographs that show the modeled historical
            mean (white line in center) and range of variation (gray band) for
            two climate scenarios: {{ scenarioFullNames.rcp45 }} and
            {{ scenarioFullNames.rcp85 }}. The minimum and maximum across 13
            climate models are shown in each chart (top and bottom lines), and
            the range of variation for the means are shown as a shaded ribbon.
          </p>
          <p v-if="segmentRegion == 'alaska'">
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
          <p v-if="segmentRegion == 'conus' && appContext == 'mid'">
            The chart below shows the mean modeled monthly flow rate for the
            historical modeled value (diamond) and with the projected
            middle-of-the-road climate scenario&mdash;{{
              scenarioFullNames.rcp60
            }}. The box plot shows the range of values for 13 climate models.
            Each box plot spans from quartile 1 to quartile 3, which is the
            interquartile range (IQR). The second quartile&mdash;the
            median&mdash;is marked by a line inside the box. The whiskers span
            &#177;1.5 times the interquartile range, and outliers are shown as
            colored dots.
          </p>
          <p v-if="segmentRegion == 'conus' && appContext == 'extremes'">
            The charts below show the mean modeled monthly flow rate for the
            historical modeled value (diamond) with two climate scenarios:
            {{ scenarioFullNames.rcp45 }} and {{ scenarioFullNames.rcp85 }}. The
            box plots show the range of values for 13 climate models. Each box
            plot spans from quartile 1 to quartile 3, which is the interquartile
            range (IQR). The second quartile&mdash;the median&mdash;is marked by
            a line inside the box. The whiskers span &#177;1.5 times the
            interquartile range, and outliers are shown as colored dots.
          </p>
          <p v-if="segmentRegion == 'alaska'">
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
          <p v-if="segmentRegion == 'conus' && appContext == 'mid'">
            The chart below shows the modeled annual maximum daily flow rate and
            the date of its occurrence for the historical modeled value
            (diamond) and with the projected middle-of-the-road climate
            scenario, {{ scenarioFullNames.rcp60 }}, for 13 climate models. This
            chart can help you see changes in the timing and magnitude of annual
            maximum flow rates.
          </p>
          <p v-if="segmentRegion == 'conus' && appContext == 'extremes'">
            The charts below show the modeled annual maximum daily flow rate and
            the date of its occurrence for the historical modeled value
            (diamond) and for two climate scenarios,
            {{ scenarioFullNames.rcp45 }} and {{ scenarioFullNames.rcp85 }}, for
            13 climate models. This chart can help you see changes in the timing
            and magnitude of annual maximum flow rates.
          </p>
          <p v-if="segmentRegion == 'alaska'">
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

    <section class="section" v-if="segmentRegion == 'alaska'">
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
    <section class="section" v-if="segmentRegion == 'alaska'">
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
    <section class="section" v-if="segmentRegion == 'alaska'">
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
          <p v-if="segmentRegion == 'conus' && appContext == 'mid'">
            The projected values in the tables below show the median values
            across the {{ scenarioFullNames.rcp60 }} climate scenario for 13
            climate models. This represents the middle-of-the-road for future
            model projections in the CMIP5 family of datasets.
          </p>
          <p v-if="segmentRegion == 'conus' && appContext == 'extremes'">
            The projected values in the table below show the extreme values
            across two climate scenarios for 13 climate models. The values in
            the &lsquo;Minimum, {{ scenarioFullNames.rcp45 }}&rsquo; column are
            the minimum values across all 13 climate models for the
            {{ scenarioFullNames.rcp45 }} scenario, and the values in the
            &lsquo;Maximum, {{ scenarioFullNames.rcp85 }}&rsquo; column are the
            maximum values across all 13 climate models for the
            {{ scenarioFullNames.rcp85 }} scenario.
          </p>
          <p v-if="segmentRegion == 'alaska'">
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
          v-if="segmentRegion == 'alaska'"
          :wt-stats="streamWtStats"
          category="water_temperature_annual"
          tableTitle="Annual Water Temperature Statistics"
        />
        <StatsTable
          v-if="segmentRegion == 'alaska'"
          :wt-stats="streamWtStats"
          category="water_temperature_minimum_monthly"
          tableTitle="Minimum Monthly Mean Water Temperature"
        />
        <StatsTable
          v-if="segmentRegion == 'alaska'"
          :wt-stats="streamWtStats"
          category="water_temperature_mean_monthly"
          tableTitle="Mean Monthly Water Temperature"
        />
        <StatsTable
          v-if="segmentRegion == 'alaska'"
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
