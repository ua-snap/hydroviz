<script setup lang="ts">
import { toRaw } from 'vue'
import { doyToDateString } from '~/utils/general'
import {
  getLayout,
  getConfig,
  initializeChart,
  getDataRange,
  convertDoysToHydroYearDoys,
  processLowessAndHydroYear,
  getGageIdLine,
} from '~/utils/chart'
const { $Plotly, $_ } = useNuxtApp()
import type { Data } from 'plotly.js'
import { scenarioFullNames } from '~/types/modelsScenarios'

const props = defineProps(['streamHydrograph'])

import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { segmentId, gageId, appContext, appEra } = storeToRefs(streamSegmentStore)

const doys = $_.range(1, 366 + 1)
const hydroDoys = convertDoysToHydroYearDoys(doys)

let isAlaskaData = false

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

function postprocessValues(traceData) {
  let smoothedData = processLowessAndHydroYear(traceData, doys)
  let clampedData = clampTinyValues(smoothedData)
  return clampedData
}

// Clamp any value below 1 to 1 to avoid issues with logarithmic y-axis.
function clampTinyValues(traceData) {
  let clampValue = 1
  return traceData.map((val: number) => {
    if (val < clampValue) {
      return clampValue
    } else {
      return val
    }
  })
}

function processProjectedAlaskaData(hg, traces: Data[]) {
  let projectedFlowData = hg['projected']['2034-2065']

  let hydroYearProjectedMeanMax = postprocessValues(
    projectedFlowData['doy_mean_max']
  )

  let hydroYearProjectedMeanMin = postprocessValues(
    projectedFlowData['doy_mean_min']
  )

  let meanMinTrace = {
    x: hydroDoys,
    y: hydroYearProjectedMeanMin,
    type: 'scatter',
    mode: 'line',
    line: { color: scenarioColors['historical'].fill, width: 0 },
    fillcolor: scenarioColors['rcp60'].fill,
    showlegend: false,
  }

  let meanMaxTrace = {
    x: hydroDoys,
    y: hydroYearProjectedMeanMax,
    type: 'scatter',
    fill: 'tonexty',
    line: { color: scenarioColors['historical'].fill, width: 0 },
    fillcolor: scenarioColors['rcp60'].fill,
    name: 'Minimum/maximum of model means',
  }

  traces.push(meanMinTrace)
  traces.push(meanMaxTrace)

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

  Object.keys(traceConfig).forEach(key => {
    let traceData = projectedFlowData[key]
    let traceName = traceConfig[key].label

    let hydroOrderedSmoothedY = postprocessValues(traceData)
    let trace = {
      x: hydroDoys,
      y: hydroOrderedSmoothedY,
      type: 'scatter',
      mode: 'lines',
      line: {
        shape: 'spline',
        color: scenarioColors['rcp60'][key],
      },
      name: traceName,
    }
    traces.push(trace)
  })
}

function processProjectedConusData(
  hg,
  scenarios: string[],
  traces: Data[],
  traces2: Data[]
) {
  const isExtremesContext = appContext.value === 'extremes'

  scenarios.forEach(scenario => {
    let projectedFlowData = hg['projected'][appEra.value][scenario]

    let hydroYearProjectedMeanMax = postprocessValues(
      projectedFlowData['doy_mean_max']
    )

    let hydroYearProjectedMeanMin = postprocessValues(
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

    if (isExtremesContext) {
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

      let hydroOrderedSmoothedY = postprocessValues(traceData)
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
      if (isExtremesContext) {
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
}

// hg is assumed to be non-null, raw, and only dynamic land cover now.
const buildChart = hg => {
  let traces: Data[] = []
  let traces2: Data[] = []

  // Check if this is Alaska data (no projected scenarios)
  isAlaskaData = !hg['projected'][appEra.value]

  let scenarios: string[] = []
  if (!isAlaskaData) {
    if (appContext.value === 'mid') {
      scenarios = ['rcp60']
    } else {
      scenarios = ['rcp85', 'rcp45']
    }
  }

  // Create historical trace
  let historicalFlowData = hg['historical']

  let hydroYearHistoricalDataMin = postprocessValues(
    historicalFlowData['doy_min']
  )
  let hydroYearHistoricalDataMean = postprocessValues(
    historicalFlowData['doy_mean']
  )
  let hydroYearHistoricalDataMax = postprocessValues(
    historicalFlowData['doy_max']
  )

  let historicalYearRange = isAlaskaData ? '1990-2021' : '1976-2005'

  let historicalMinTrace = {
    x: hydroDoys,
    y: hydroYearHistoricalDataMin,
    type: 'scatter',
    mode: 'line',
    line: { color: scenarioColors['historical'].fill, width: 0 },
    name: `Minimum historical, ${historicalYearRange}`,
    showlegend: false,
  }

  let historicalMaxTrace = {
    x: hydroDoys,
    y: hydroYearHistoricalDataMax,
    type: 'scatter',
    fill: 'tonexty',
    mode: 'none',
    fillcolor: scenarioColors['historical'].fill,
    name: `Minimum/maximum historical, ${historicalYearRange}`,
  }

  let historicalMeanTrace = {
    x: hydroDoys,
    y: hydroYearHistoricalDataMean,
    type: 'scatter',
    mode: 'line',
    line: { color: '#f0f0f0', width: 2 },
    name: `Mean historical, ${historicalYearRange}`,
  }

  // First put the two historical traces at the bottom of the stack...
  traces.push(historicalMinTrace)
  traces.push(historicalMaxTrace)

  if (appContext.value === 'extremes' && !isAlaskaData) {
    traces2.push(historicalMinTrace)
    traces2.push(historicalMaxTrace)
  }

  // Only add projected data for CONUS (non-Alaska) data
  if (isAlaskaData) {
    processProjectedAlaskaData(hg, traces)
  } else {
    processProjectedConusData(hg, scenarios, traces, traces2)
  }

  // Now put the historical mean on top because it makes the key comparison
  // easier to see (how do the projections relate to the historical calibration mean?)
  traces.push(historicalMeanTrace)
  if (appContext.value === 'extremes' && !isAlaskaData) {
    traces2.push(historicalMeanTrace)
  }

  // These numbers correspond to the 1st of each month in a 366-day year,
  // oriented by the hydro year.
  let xTickVals = [274, 305, 335, 1, 32, 60, 91, 121, 152, 182, 213, 244]
  let xTickLabels = xTickVals.map((doy: number) => {
    return doyToDateString(doy, true)
  })

  let scenarioLabel: string
  let scenarioLabel2: string
  let titleText: string
  let titleBase: string = ''
  let gageIdLine = getGageIdLine(gageId.value)

  if (isAlaskaData) {
    scenarioLabel = scenarioFullNames['ssp370']
    titleText = `Modeled flow rate, 2034-2065, ${scenarioLabel}${gageIdLine}`
  } else {
    if (appContext.value === 'mid') {
      scenarioLabel = scenarioFullNames['rcp60']
    } else {
      scenarioLabel = scenarioFullNames['rcp45']
      scenarioLabel2 = scenarioFullNames['rcp85']
    }

    titleBase = `Modeled flow rate, ${appEra.value}`
    titleText = `${titleBase}, ${scenarioLabel}${gageIdLine}`
  }

  let yAxisLabel = 'Flow rate, cf/s'

  let xAxisConfig = {
    type: 'category',
    tickmode: 'array',
    tickvals: xTickVals,
    ticktext: xTickLabels,
  }

  // Min/max need to be logarithmic to work with Plotly.js log chart type.
  let { yMin, yMax } = getDataRange(hg)

  // Set minimum possible y-axis range to 1.
  // All values below 1 have been clamped to 1 already.
  if (yMin < 1) {
    yMin = 1
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

  let isTwoLineTitle = gageId.value ? true : false

  let layout = getLayout(
    'hydrograph',
    titleText,
    yAxisLabel,
    xAxisConfig,
    yAxisConfig,
    legendConfig,
    isTwoLineTitle,
    isAlaskaData
  )

  if (isAlaskaData) {
    let pngName = `hydrograph_${segmentId.value}_2034-2065`
    let config = getConfig(pngName)
    $Plotly.newPlot('hydrograph', traces, layout, config)
  } else {
    if (appContext.value === 'mid') {
      let pngName = `hydrograph_${segmentId.value}_rcp60_${appEra.value}`
      let config = getConfig(pngName)
      $Plotly.newPlot('hydrograph', traces, layout, config)
    } else {
      let pngName = `hydrograph_${segmentId.value}_rcp45_${appEra.value}`
      let config = getConfig(pngName)
      $Plotly.newPlot('hydrograph', traces, layout, config)

      let scenarioLabel2 = scenarioFullNames['rcp85']
      let titleText2 = `${titleBase}, ${scenarioLabel2}${gageIdLine}`
      let layout2 = getLayout(
        'hydrograph',
        titleText2,
        yAxisLabel,
        xAxisConfig,
        yAxisConfig,
        legendConfig,
        isTwoLineTitle,
        isAlaskaData
      )
      let pngName2 = `hydrograph_${segmentId.value}_rcp85_${appEra.value}`
      let config2 = getConfig(pngName2)
      $Plotly.newPlot('hydrograph2', traces2, layout2, config2)
    }
  }
}
</script>

<template>
  <div id="hydrograph"></div>
  <div v-if="appContext === 'extremes' && !isAlaskaData" class="mt-6"></div>
  <div v-if="!isAlaskaData" id="hydrograph2"></div>
</template>
