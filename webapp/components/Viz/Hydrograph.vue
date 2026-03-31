<script setup lang="ts">
import { toRaw } from 'vue'
import lowess from '@stdlib/stats-lowess'
import { doyToDateString } from '~/utils/general'
import { getLayout, getConfig, initializeChart } from '~/utils/chart'
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
  initializeChart(
    $Plotly,
    'hydrograph',
    buildChart,
    toRaw(props.streamHydrograph)
  )
})

let scenarioLabels = {
  rcp45: 'RCP 4.5',
  rcp60: 'RCP 6.0',
  rcp85: 'RCP 8.5',
}

let plotLabels = {
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
    fill: '#32cd3280', // softer green with transparency
    doy_min_min: '#32cd32', // same as fill, solid
    doy_mean_mean: '#28a428', // slightly darker than fill
    doy_max_max: '#1e7a1e', // even darker green
  },
  rcp85: {
    fill: '#e0666680', // lighter red with transparency
    doy_min_min: '#ff9999', // even lighter red
    doy_mean_mean: '#ff4d4d', // lighter strong red
    doy_max_max: '#a83232', // lighter dark red
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

  // Plotly.js subplot axes
  let axes = [
    {
      x: 'x',
      y: 'y',
    },
    {
      x: 'x2',
      y: 'y2',
    },
  ]

  let historicalMinTrace = {
    x: hydroDoys,
    y: hydroYearHistoricalDataMin,
    type: 'scatter',
    mode: 'line',
    line: { color: scenarioColors['historical'].fill, width: 0 },
    name: 'Historical minimum (modeled), 1976-2005',
    showlegend: false,
  }

  let historicalMaxTrace = {
    x: hydroDoys,
    y: hydroYearHistoricalDataMax,
    type: 'scatter',
    fill: 'tonexty',
    mode: 'none',
    fillcolor: scenarioColors['historical'].fill,
    name: 'Max/min historical flow (modeled), 1976-2005',
  }

  let historicalMeanTrace = {
    x: hydroDoys,
    y: hydroYearHistoricalDataMean,
    type: 'scatter',
    mode: 'line',
    line: { color: '#f0f0f0', width: 3 },
    name: 'Mean historical flow (modeled), 1976-2005',
  }

  if (appContext.value === 'extremes') {
    let showLegend = true
    axes.forEach(axis => {
      let historicalMinTraceCopy = $_.cloneDeep(historicalMinTrace)
      let historicalMaxTraceCopy = $_.cloneDeep(historicalMaxTrace)
      historicalMinTraceCopy['xaxis'] = axis.x
      historicalMinTraceCopy['yaxis'] = axis.y
      historicalMaxTraceCopy['xaxis'] = axis.x
      historicalMaxTraceCopy['yaxis'] = axis.y
      historicalMaxTraceCopy['showlegend'] = showLegend
      traces.push(historicalMinTraceCopy)
      traces.push(historicalMaxTraceCopy)
      showLegend = false
    })
  } else {
    traces.push(historicalMinTrace)
    traces.push(historicalMaxTrace)
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
      name:
        'Min/max mean modeled future flow, ' +
        appEra.value +
        ', ' +
        scenarioLabels[scenario],
    }

    if (appContext.value === 'extremes' && scenario === 'rcp85') {
      meanMinTrace['xaxis'] = 'x2'
      meanMinTrace['yaxis'] = 'y2'
      meanMaxTrace['xaxis'] = 'x2'
      meanMaxTrace['yaxis'] = 'y2'
    }

    traces.push(meanMinTrace)
    traces.push(meanMaxTrace)
  })

  if (appContext.value === 'extremes') {
    let showLegend = true
    axes.forEach(axis => {
      let historicalMeanTraceCopy = $_.cloneDeep(historicalMeanTrace)
      historicalMeanTraceCopy['xaxis'] = axis.x
      historicalMeanTraceCopy['yaxis'] = axis.y
      historicalMeanTraceCopy['showlegend'] = showLegend
      traces.push(historicalMeanTraceCopy)
      showLegend = false
    })
  } else {
    traces.push(historicalMeanTrace)
  }

  let traceConfig = {
    doy_min_min: {
      label: 'Minimum modeled future flow',
    },
    doy_mean_mean: {
      label: 'Mean modeled future flow',
    },
    doy_max_max: {
      label: 'Maximum modeled future flow',
    },
  }

  scenarios.forEach(scenario => {
    let projectedFlowData = hg['projected'][appEra.value][scenario]

    Object.keys(traceConfig).forEach(key => {
      let traceData = projectedFlowData[key]
      let traceName =
        traceConfig[key].label +
        ', ' +
        appEra.value +
        ', ' +
        scenarioLabels[scenario]

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
      if (appContext.value === 'extremes' && scenario === 'rcp85') {
        trace['xaxis'] = 'x2'
        trace['yaxis'] = 'y2'
      }
      traces.push(trace)
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

  let layout = getLayout(
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
    },
    {
      traceorder: 'reversed',
    }
  )

  // Add a tiny bit of margin to the left of the plot
  layout['margin']['l'] = 110

  if (appContext.value === 'extremes') {
    layout['xaxis2'] = $_.cloneDeep(layout['xaxis'])
    layout['yaxis2'] = $_.cloneDeep(layout['yaxis'])
    layout['height'] = 830
    layout['grid'] = {
      rows: 2,
      columns: 1,
      pattern: 'independent',
      ygap: 0.18,
    }
  }

  // Add annotations along the y-axis for each subplot, rotated vertically
  if (appContext.value === 'extremes') {
    layout['annotations'] = [
      {
        text: plotLabels['rcp45'],
        x: -0.12,
        y: 0.778,
        showarrow: false,
        font: { size: 14 },
        textangle: -90,
        xref: 'paper',
        yref: 'paper',
        xanchor: 'center',
        yanchor: 'middle',
      },
      {
        text: plotLabels['rcp85'],
        x: -0.12,
        y: 0.228,
        showarrow: false,
        font: { size: 14 },
        textangle: -90,
        xref: 'paper',
        yref: 'paper',
        xanchor: 'center',
        yanchor: 'middle',
      },
    ]
  } else {
    layout['annotations'] = [
      {
        text: plotLabels['rcp60'],
        x: -0.12,
        y: 0.505,
        showarrow: false,
        font: { size: 14 },
        textangle: -90,
        xref: 'paper',
        yref: 'paper',
        xanchor: 'center',
        yanchor: 'middle',
      },
    ]
  }

  const config = getConfig()

  $Plotly.newPlot('hydrograph', traces, layout, config)
}
</script>

<template>
  <div id="hydrograph"></div>
</template>

<style lang="scss" scoped></style>
