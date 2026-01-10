<script setup lang="ts">
// import { lcs, models, scenarios, eras } from '~/types/modelsScenarios'
// import { statVars } from '~/types/statsVars'
import { watch, toRaw } from 'vue'
import lowess from '@stdlib/stats-lowess'
import { useStreamSegmentStore } from '~/stores/streamSegment'
import { getLayout, getConfig } from '~/utils/chart'
const { $Plotly, $_ } = useNuxtApp()
import type { Data } from 'plotly.js-dist-min'

const streamSegmentStore = useStreamSegmentStore()
let { streamHydrograph, segmentName, isLoading } =
  storeToRefs(streamSegmentStore)

// const lcInput = defineModel('lc', { default: 'dynamic' })
// const modelInput = defineModel('model', { default: 'CCSM4' })
// const scenarioInput = defineModel('scenario', { default: 'rcp60' })

// Round to significant digits.  Stub.
function roundTo(num, sig = 3) {
  return Number(num.toPrecision(sig))
}

// We want a data structure that we can feed into Plotly.
// Three traces:
// - min (floor) across all models
// - mean computed across all models
// - max (ceiling) across all models
// incoming hydrograph data should be an object whose keys are models,
// see the API documentation for structure details deeper than that.
function buildHydrographData(hydrographData, scenario: Scenario, era: Era) {
  // TODO: keep this or what?
  if (!hydrographData || !era) {
    throw 'hydrograph data missing or era missing'
  }

  var mean = [],
    min = [],
    max = []

  var dayMin, dayMax, dayMean

  // old school for loop!
  for (let i = 0; i <= 365; i++) {
    // If true, initialize the day min/max/mean for this iteration
    let unset = true
    Object.keys(hydrographData).forEach(model => {
      console.log('Model: ', model, 'Scenario', scenario, 'Era:', era)
      console.log('hydrographData[model]', hydrographData[model])
      if (unset) {
        dayMin = hydrographData[model][scenario][era][i]['doy_min']
        dayMax = hydrographData[model][scenario][era][i]['doy_max']
        dayMean = hydrographData[model][scenario][era][i]['doy_mean']

        unset = false
        return // continue loop
      } else {
        if (hydrographData[model][scenario][era][i]['doy_min'] < dayMin) {
          dayMin = hydrographData[model][scenario][era][i]['doy_min']
        }
        if (hydrographData[model][scenario][era][i]['doy_max'] > dayMax) {
          dayMax = hydrographData[model][scenario][era][i]['doy_max']
        }
        dayMean += hydrographData[model][scenario][era][i]['doy_mean']
      }
    })

    min[i] = roundTo(dayMin)
    mean[i] = roundTo(dayMean / 14)
    max[i] = roundTo(dayMax)
  }

  return [min, mean, max]
}

const doyToDateString = (doy: number) => {
  const year = 2025 // Can be any year, but not a leap year.
  const date = new Date(year, 0) // January 1st of the given year
  date.setDate(doy) // Add DOY as days offset
  const options: Intl.DateTimeFormatOptions = { month: 'short', day: 'numeric' }
  return date.toLocaleDateString('en-US', options)
}

// Shift a DOY-indexed dataset to hydro year (Oct 1 - Sept 30)
function convertDoysToHydroYearDoys(series) {
  let octDec = series.slice(273) // through end of array (366)
  let janSept = series.slice(0, 273)
  let joined = octDec.concat(janSept)
  return octDec.concat(janSept)
}

const hydroDoys = convertDoysToHydroYearDoys($_.range(1, 366 + 1))

// hg is assumed to be non-null, raw, and only dynamic land cover now.
const buildChart = hg => {
  let traces: Data[] = []

  // Remove the historical modeled dataset (Maurer) & build that data for hydrograph
  let historicalMaurer = {}
  historicalMaurer['Maurer'] = hg['Maurer']
  delete hg['Maurer']

  console.log(historicalMaurer)
  let historicalFlowData = buildHydrographData(
    historicalMaurer,
    'historical',
    '1976-2005'
  )

  // There's a gotcha here: two scenarios (ACCESS1-0, BNU-ESM) don't have RCP 2.6 or 6.0.
  // Historical needs to have been removed.
  let projectedFlowData = buildHydrographData(hg, 'rcp45', '2046-2075')

  let traceConfig = [
    {
      label: 'Minimum flow',
      doy: hydroDoys,
    },
    {
      label: 'Mean flow',
      doy: hydroDoys,
    },
    {
      label: 'Maximum flow',
      doy: hydroDoys,
    },
  ]

  projectedFlowData.forEach((traceData, index) => {
    // BIG TODO: the Loess isn't fitting right still.
    // Need to trick it so there's not discontinuity between day 366/1.

    let hydroYearTraceData = convertDoysToHydroYearDoys(traceData)
    let smoothed = lowess(hydroDoys, hydroYearTraceData, {
      f: 0.05,
    })
    let hydroOrderedSmoothedY = convertDoysToHydroYearDoys(smoothed.y)
    hydroOrderedSmoothedY = hydroOrderedSmoothedY.map((cfm: number) => {
      return roundTo(cfm)
    })
    traces.push({
      x: hydroDoys,
      y: hydroOrderedSmoothedY,
      mode: 'lines',
      line: { shape: 'spline', smoothing: 1.3 },
      name: traceConfig[index].label,
    })
  })

  const yAxisLabel = 'Daily flow rate (cfm)'

  // These numbers correspond to the 1st of each month in a 366-day year.
  let xTickVals = [274, 305, 335, 1, 32, 59, 90, 121, 152, 182, 213, 244]
  let xTickLabels = xTickVals.map((doy: number) => {
    return doyToDateString(doy)
  })

  const chartTitle = 'Hydrograph'

  const titleText: string =
    'Minimum, mean and maximum flow rate across 13 models'

  const layout = getLayout(titleText, yAxisLabel, {
    tickangle: 45,
  })

  layout.xaxis = {
    type: 'category',
    tickmode: 'array',
    tickvals: xTickVals,
    ticktext: xTickLabels,
  }

  layout.yaxis = {
    type: 'log',
    autorange: true,
  }

  const config = getConfig(chartTitle)

  $Plotly.newPlot('hydrograph', traces, layout, config)
}

watch(streamHydrograph, hg => {
  // Is briefly null when switching places
  if (hg.data) {
    buildChart(toRaw(hg.data.dynamic))
  }
})
</script>

<template>
  <section class="section">
    <div class="container">
      <div v-if="isLoading == true" class="loading content is-size-4">
        <p>Loading data&hellip; this can take a minute or two.</p>
        <progress class="progress" />
      </div>
      <div v-show="!isLoading && streamHydrograph">
        <h3 class="title is-3">Hydrograph for {{ segmentName }}</h3>
        <div id="hydrograph"></div>
      </div>
    </div>
  </section>
</template>

<style lang="scss" scoped></style>
