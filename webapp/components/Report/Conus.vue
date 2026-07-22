<script setup lang="ts">
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let {
  streamStats,
  streamHydrograph,
  streamMonthlyFlow,
  streamMaxFlowDates,
  appContext,
} = storeToRefs(streamSegmentStore)
import { scenarioFullNames } from '~/types/modelsScenarios'

onMounted(() => {
  streamSegmentStore.fetchStreamStats()
})

onUnmounted(() => {
  streamSegmentStore.clearStats()
})

const lowFlow = computed(() => {
  return streamStats.value['historical']['1976-2005']['ma99'] < 100
})

const showLowFlowHydrograph = ref(false)
const showIfSure = () => {
  showLowFlowHydrograph.value = true
}
</script>

<template>
  <BackToMap />
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
        </div>
      </div>
    </section>
    <!-- StickyToggle must be outside of section/container wrappers -->
    <div class="sticky-wrapper">
      <StickyToggle />
      <section class="section">
        <div class="container">
          <h4 class="title is-4">Mean monthly flow</h4>
          <div class="content clamp is-size-5 mb-6">
            <p v-if="appContext == 'mid'">
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
            <p v-if="appContext == 'extremes'">
              The charts below show the mean modeled monthly flow rate for the
              historical modeled value (diamond) with two climate scenarios:
              {{ scenarioFullNames.rcp45 }} and {{ scenarioFullNames.rcp85 }}.
              The box plots show the range of values for 13 climate models. Each
              box plot spans from quartile 1 to quartile 3, which is the
              interquartile range (IQR). The second quartile&mdash;the
              median&mdash;is marked by a line inside the box. The whiskers span
              &#177;1.5 times the interquartile range, and outliers are shown as
              colored dots.
            </p>
          </div>
          <VizMonthlyFlow :stream-monthly-flow="streamMonthlyFlow" />
        </div>
      </section>
      <section class="section">
        <div class="container">
          <h4 class="title is-4">Hydrograph</h4>

          <!-- Show if sure -->
          <div
            v-if="lowFlow && !showLowFlowHydrograph"
            class="content clamp is-size-5"
          >
            <p>
              ⚠️ Because this stream segment has relatively low mean annual flow
              (<100 cf/s), a daily hydrograph showing ranges of model outputs
              can look implausible and show more variation in model behavior
              than the flow regime, and is not displayed by default. The monthly
              chart above aggregates these changes and shows a clearer signal of
              possible future change.
              <a @click.prevent="showIfSure">Show hydrograph anyway.</a>
            </p>
          </div>
          <!-- v-if (not v-show) so Plotly mounts into a visible container it can
             measure; charts drawn while display:none fall back to 700px wide -->
          <div v-if="!lowFlow || showLowFlowHydrograph">
            <div class="content clamp is-size-5">
              <p v-if="appContext == 'mid'">
                The chart below is a hydrograph that shows the modeled
                historical mean (white line in center) and range of variation
                (gray band) with the projected middle-of-the-road climate
                scenario&mdash;{{ scenarioFullNames.rcp60 }}. The minimum and
                maximum across 13 climate models are shown (the top and bottom
                lines), and the range of variation for the means are shown as a
                shaded ribbon.
              </p>
              <p v-if="appContext == 'extremes'">
                The charts below are hydrographs that show the modeled
                historical mean (white line in center) and range of variation
                (gray band) for two climate scenarios:
                {{ scenarioFullNames.rcp45 }} and {{ scenarioFullNames.rcp85 }}.
                The minimum and maximum across 13 climate models are shown in
                each chart (top and bottom lines), and the range of variation
                for the means are shown as a shaded ribbon.
              </p>
            </div>
            <VizHydrograph :stream-hydrograph="streamHydrograph" />
          </div>
        </div>
      </section>

      <section class="section">
        <div class="container">
          <h4 class="title is-4">Timing of annual maximum daily flow rate</h4>
          <div class="content clamp is-size-5 mb-6">
            <p v-if="appContext == 'mid'">
              The chart below shows the modeled annual maximum daily flow rate
              and the date of its occurrence for the historical modeled value
              (diamond) and with the projected middle-of-the-road climate
              scenario, {{ scenarioFullNames.rcp60 }}, for 13 climate models.
              This chart can help you see changes in the timing and magnitude of
              annual maximum flow rates.
            </p>
            <p v-if="appContext == 'extremes'">
              The charts below show the modeled annual maximum daily flow rate
              and the date of its occurrence for the historical modeled value
              (diamond) and for two climate scenarios,
              {{ scenarioFullNames.rcp45 }} and {{ scenarioFullNames.rcp85 }},
              for 13 climate models. This chart can help you see changes in the
              timing and magnitude of annual maximum flow rates.
            </p>
          </div>
          <VizMaxFlowDates :stream-max-flow-dates="streamMaxFlowDates" />
        </div>
      </section>

      <section class="section">
        <div class="container">
          <h3 class="title is-3">Complete statistics</h3>

          <div class="is-size-5 mb-6 clamp">
            <p v-if="appContext == 'mid'">
              The projected values in the tables below show the median values
              across the {{ scenarioFullNames.rcp60 }} climate scenario for 13
              climate models. This represents the middle-of-the-road for future
              model projections in the CMIP5 family of datasets.
            </p>
            <p v-if="appContext == 'extremes'">
              The projected values in the tables below show the median values
              across the {{ scenarioFullNames.rcp45 }} and
              {{ scenarioFullNames.rcp85 }} climate scenarios for 13 climate
              models. For each scenario, these values represent the median
              projection within the CMIP5 family of datasets.
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
        </div>
      </section>
    </div>
    <GetAndUse />
  </div>
</template>

<style lang="scss" scoped></style>
