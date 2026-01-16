<script setup lang="ts">
// import { lcs, models, scenarios, eras } from '~/types/modelsScenarios'
// import { statVars } from '~/types/statsVars'
import { watch } from 'vue'
import lowess from '@stdlib/stats-lowess'
import { useStreamSegmentStore } from '~/stores/streamSegment'
import { getLayout, getConfig } from '~/utils/chart'
const { $Plotly, $_ } = useNuxtApp()
import type { Data } from 'plotly.js-dist-min'

var plotlyChart // will have the Plotly object if value
const streamSegmentStore = useStreamSegmentStore()
let { streamHydrograph, segmentName } = storeToRefs(streamSegmentStore)

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
    mean[i] = roundTo(dayMean / Object.keys(hydrographData).length)
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
const doys = $_.range(1, 366 + 1)
const hydroDoys = convertDoysToHydroYearDoys(doys)

// Converts & LOWESS smooths a timeseries of Y values
// Need to trick it so there's not discontinuity between day 366/1.
function processLowessAndHydroYear(traceData) {
  let hydroYearTraceData = convertDoysToHydroYearDoys(traceData)

  // Bit tricky: we index the day-of-year as 1...366 for the x-axis
  // for the purpose of the lowess calculation, but the y-values represent
  // the hydro-year shifted values.  This gives us the correct, smooth
  // chart form.
  let smoothed = lowess(doys, hydroYearTraceData, {
    f: 0.05,
    sorted: true,
  })
  let hydroOrderedSmoothedY = smoothed.y.map((cfm: number) => {
    return roundTo(cfm)
  })
  return hydroOrderedSmoothedY
}

// hg is assumed to be non-null, raw, and only dynamic land cover now.
const buildChart = hg => {
  let traces: Data[] = []

  // Remove the historical modeled dataset (Maurer) & build that data for hydrograph
  let historicalMaurer = {}
  historicalMaurer['Maurer'] = hg['Maurer']
  delete hg['Maurer']

  // Create historical trace
  let historicalFlowData = buildHydrographData(
    historicalMaurer,
    'historical',
    '1976-2005'
  )

  let hydroYearHistoricalDataMin = processLowessAndHydroYear(
    historicalFlowData[0]
  )
  let hydroYearHistoricalDataMean = processLowessAndHydroYear(
    historicalFlowData[1]
  )
  let hydroYearHistoricalDataMax = processLowessAndHydroYear(
    historicalFlowData[2]
  )

  traces.push({
    x: hydroDoys,
    y: hydroYearHistoricalDataMin,
    type: 'scatter',
    mode: 'line',
    line: { color: '#aaaaaa', width: 0 },
    name: 'Historical Minimum (Modeled), 1975-2005',
  })

  traces.push({
    x: hydroDoys,
    y: hydroYearHistoricalDataMax,
    type: 'scatter',
    fill: 'tonexty',
    mode: 'none',
    fillcolor: 'rgba(190,190,190,0.5)',
    name: 'Historical Maximum (Modeled), 1975-2005',
  })

  traces.push({
    x: hydroDoys,
    y: hydroYearHistoricalDataMean,
    type: 'scatter',
    mode: 'line',
    line: { color: '#FFFFFF', width: 3 },
    name: 'Historical Mean (Modeled), 1975-2005',
  })

  // There's a gotcha here: two scenarios (ACCESS1-0, BNU-ESM) don't have RCP 2.6 or 6.0.
  // Historical needs to have been removed.
  let projectedFlowData = buildHydrographData(hg, 'rcp85', '2046-2075')

  let traceConfig = [
    {
      label: 'Minimum modeled future flow',
      color: '#6baed6',
    },
    {
      label: 'Mean modeled future flow',
      color: '#3182bd',
    },
    {
      label: 'Maximum modeled future flow',
      color: '#08519c',
    },
  ]

  projectedFlowData.forEach((traceData, index) => {
    let hydroOrderedSmoothedY = processLowessAndHydroYear(traceData)
    traces.push({
      x: hydroDoys,
      y: hydroOrderedSmoothedY,
      type: 'scatter',
      mode: 'lines',
      line: { shape: 'spline', color: traceConfig[index].color },
      name: traceConfig[index].label,
    })
  })

  // These numbers correspond to the 1st of each month in a 366-day year,
  // oriented by the hydro year.
  let xTickVals = [274, 305, 335, 1, 32, 60, 91, 121, 152, 182, 213, 244]
  let xTickLabels = xTickVals.map((doy: number) => {
    return doyToDateString(doy)
  })

  const titleText: string =
    'Minimum, mean and maximum modeled projected flow rate'

  const layout = getLayout(
    titleText,
    'Flow rate, cf/s',
    {
      type: 'category',
      tickmode: 'array',
      tickvals: xTickVals,
      ticktext: xTickLabels,
    },
    {
      type: 'log',
      autorange: true,
    }
  )
  const config = getConfig()

  $Plotly.newPlot('hydrograph', traces, layout, config)
}

watch(streamHydrograph, newValue => {
  // We cannot access $Plotly directly from utils/charts.ts, so we need to
  // pass it as a function parameter here.
  initializeChart($Plotly, 'hydrograph', buildChart, newValue)
})
</script>

<template>
  <section class="section">
    <div class="container">
      <div v-show="streamHydrograph" class="content">
        <h3 class="title is-3">Hydrograph for {{ segmentName }}</h3>
        <ClientOnly>
          <div id="hydrograph"></div>
        </ClientOnly>
      </div>
    </div>
  </section>
</template>

<style lang="scss" scoped></style>
