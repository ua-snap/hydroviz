<script setup lang="ts">
import { toRaw } from 'vue'
import lowess from '@stdlib/stats-lowess'
import { doyToDateString } from '~/utils/general'
import {
  getLayout,
  getConfig,
  initializeChart,
  getDataRange,
} from '~/utils/chart'
const { $Plotly, $_ } = useNuxtApp()
import type { Data } from 'plotly.js'

const props = defineProps(['streamHydrograph'])

import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { appContext, appEra } = storeToRefs(streamSegmentStore)

onMounted(() => {
  initializeChart(
    $Plotly,
    'hydrograph',
    buildChart,
    toRaw(props.streamHydrograph)
  )
})

watch([appContext, appEra], () => {
  if (appContext.value === 'mid') {
    $Plotly.purge('hydrograph2')
  }
  initializeChart(
    $Plotly,
    'hydrograph',
    buildChart,
    toRaw(props.streamHydrograph)
  )
})

let scenarioLabels = {
  rcp45: 'Stabilizing Emissions (RCP 4.5)',
  rcp60: 'Stabilizing High Emissions (RCP 6.0)',
  rcp85: 'Increasing Emissions (RCP 8.5)',
}

let scenarioColors = {
  historical: { fill: '#bebebe80' },
  rcp45: {
    fill: '#6baed680',
    doy_min_min: '#6baed6',
    doy_mean_mean: '#3182bd',
    doy_max_max: '#08519c',
  },
  rcp60: {
    fill: '#32cd3280',
    doy_min_min: '#32cd32',
    doy_mean_mean: '#28a428',
    doy_max_max: '#1e7a1e',
  },
  rcp85: {
    fill: '#e0666680',
    doy_min_min: '#e06666',
    doy_mean_mean: '#ff4d4d',
    doy_max_max: '#a83232',
  },
}

// Round to significant digits.  Stub.
function roundTo(num, sig = 3) {
  return Number(num.toPrecision(sig))
}

// Shift a DOY-indexed dataset to hydro year (Oct 1 - Sept 30)
function convertDoysToHydroYearDoys(series) {
  let octDec = series.slice(273) // through end of array (366)
  let janSept = series.slice(0, 273)
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
  let traces2: Data[] = []

  let scenarios: string[]
  if (appContext.value === 'mid') {
    scenarios = ['rcp60']
  } else {
    scenarios = ['rcp85', 'rcp45']
  }

  // Create historical trace
  let historicalFlowData = hg['historical']

  let hydroYearHistoricalDataMin = processLowessAndHydroYear(
    historicalFlowData['doy_min']
  )
  let hydroYearHistoricalDataMean = processLowessAndHydroYear(
    historicalFlowData['doy_mean']
  )
  let hydroYearHistoricalDataMax = processLowessAndHydroYear(
    historicalFlowData['doy_max']
  )

  let historicalMinTrace = {
    x: hydroDoys,
    y: hydroYearHistoricalDataMin,
    type: 'scatter',
    mode: 'line',
    line: { color: scenarioColors['historical'].fill, width: 0 },
    name: 'Minimum historical, 1976-2005',
    showlegend: false,
  }

  let historicalMaxTrace = {
    x: hydroDoys,
    y: hydroYearHistoricalDataMax,
    type: 'scatter',
    fill: 'tonexty',
    mode: 'none',
    fillcolor: scenarioColors['historical'].fill,
    name: 'Minimum/maximum historical, 1976-2005',
  }

  let historicalMeanTrace = {
    x: hydroDoys,
    y: hydroYearHistoricalDataMean,
    type: 'scatter',
    mode: 'line',
    line: { color: '#f0f0f0', width: 3 },
    name: 'Mean historical, 1976-2005',
  }

  traces.push(historicalMinTrace)
  traces.push(historicalMaxTrace)
  traces.push(historicalMeanTrace)

  if (appContext.value === 'extremes') {
    traces2.push(historicalMinTrace)
    traces2.push(historicalMaxTrace)
    traces2.push(historicalMeanTrace)
  }

  scenarios.forEach(scenario => {
    let projectedFlowData = hg['projected'][appEra.value][scenario]

    let hydroYearProjectedMeanMax = processLowessAndHydroYear(
      projectedFlowData['doy_mean_max']
    )

    let hydroYearProjectedMeanMin = processLowessAndHydroYear(
      projectedFlowData['doy_mean_min']
    )

    let meanMinTrace = {
      x: hydroDoys,
      y: hydroYearProjectedMeanMin,
      type: 'scatter',
      mode: 'line',
      line: { color: scenarioColors['historical'].fill, width: 0 },
      fillcolor: scenarioColors[scenario].fill,
      showlegend: false,
    }

    let meanMaxTrace = {
      x: hydroDoys,
      y: hydroYearProjectedMeanMax,
      type: 'scatter',
      fill: 'tonexty',
      line: { color: scenarioColors['historical'].fill, width: 0 },
      fillcolor: scenarioColors[scenario].fill,
      name: 'Minimum/maximum of model means',
    }

    if (appContext.value === 'extremes') {
      if (scenario === 'rcp45') {
        traces.push(meanMinTrace)
        traces.push(meanMaxTrace)
      } else {
        traces2.push(meanMinTrace)
        traces2.push(meanMaxTrace)
      }
    } else {
      traces.push(meanMinTrace)
      traces.push(meanMaxTrace)
    }
  })

  let traceConfig = {
    doy_min_min: {
      label: 'Minimum projected',
    },
    doy_mean_mean: {
      label: 'Mean projected',
    },
    doy_max_max: {
      label: 'Maximum projected',
    },
  }

  scenarios.forEach(scenario => {
    let projectedFlowData = hg['projected'][appEra.value][scenario]

    Object.keys(traceConfig).forEach(key => {
      let traceData = projectedFlowData[key]
      let traceName = traceConfig[key].label

      let hydroOrderedSmoothedY = processLowessAndHydroYear(traceData)
      let trace = {
        x: hydroDoys,
        y: hydroOrderedSmoothedY,
        type: 'scatter',
        mode: 'lines',
        line: {
          shape: 'spline',
          color: scenarioColors[scenario][key],
        },
        name: traceName,
      }
      if (appContext.value === 'extremes') {
        if (scenario === 'rcp45') {
          traces.push(trace)
        } else {
          traces2.push(trace)
        }
      } else {
        traces.push(trace)
      }
    })
  })

  // These numbers correspond to the 1st of each month in a 366-day year,
  // oriented by the hydro year.
  let xTickVals = [274, 305, 335, 1, 32, 60, 91, 121, 152, 182, 213, 244]
  let xTickLabels = xTickVals.map((doy: number) => {
    return doyToDateString(doy, true)
  })

  let scenarioLabel: string
  let scenarioLabel2: string

  if (appContext.value === 'mid') {
    scenarioLabel = scenarioLabels['rcp60']
  } else {
    scenarioLabel = scenarioLabels['rcp45']
    scenarioLabel2 = scenarioLabels['rcp85']
  }

  let titleBase = `Modeled flow rate, ${appEra.value}`
  let titleText = `${titleBase}, ${scenarioLabel}`

  let yAxisLabel = 'Flow rate, cf/s'

  let xAxisConfig = {
    type: 'category',
    tickmode: 'array',
    tickvals: xTickVals,
    ticktext: xTickLabels,
  }

  // Min/max need to be logarithmic to work with Plotly.js log chart type.
  let { yMin, yMax } = getDataRange(hg)

  // Log of 0 is undefined.
  if (yMin <= 0) {
    yMin = 0.001
  }

  let yMinLog = Math.log10(yMin)
  let yMaxLog = Math.log10(yMax)

  let yAxisConfig = {
    type: 'log',
    autorange: false,
    range: [yMinLog, yMaxLog],
  }

  let legendConfig = {
    orientation: 'h',
    yanchor: 'top',
    y: -0.2,
    xanchor: 'center',
    x: 0.5,
  }

  let layout = getLayout(
    titleText,
    yAxisLabel,
    xAxisConfig,
    yAxisConfig,
    legendConfig
  )

  const config = getConfig()

  $Plotly.newPlot('hydrograph', traces, layout, config)

  if (appContext.value === 'extremes') {
    let scenarioLabel2 = scenarioLabels['rcp85']
    let titleText2 = `${titleBase}, ${scenarioLabel2}`
    let layout2 = getLayout(
      titleText2,
      yAxisLabel,
      xAxisConfig,
      yAxisConfig,
      legendConfig
    )
    $Plotly.newPlot('hydrograph2', traces2, layout2, config)
  }
}
</script>

<template>
  <div id="hydrograph"></div>
  <div v-if="appContext === 'extremes'" class="mt-6"></div>
  <div id="hydrograph2"></div>
</template>

<style lang="scss" scoped></style>
