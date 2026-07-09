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
} from '~/utils/chart'
const { $Plotly, $_ } = useNuxtApp()
import type { Data } from 'plotly.js'
import { scenarioFullNames } from '~/types/modelsScenarios'

const props = defineProps(['streamWtHydrograph'])

import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { segmentId, gaugeId, appContext, appEra } = storeToRefs(streamSegmentStore)

const doys = $_.range(1, 366 + 1)
const hydroDoys = convertDoysToHydroYearDoys(doys)

onMounted(() => {
  initializeChart(
    $Plotly,
    'temperature-hydrograph',
    buildChart,
    toRaw(props.streamWtHydrograph)
  )
})

watch([appContext, appEra], () => {
  initializeChart(
    $Plotly,
    'temperature-hydrograph',
    buildChart,
    toRaw(props.streamWtHydrograph)
  )
})

let scenarioColors = {
  historical: { fill: '#bebebe80' },
  projected: {
    fill: '#32cd3280',
    doy_min_min: '#32cd32',
    doy_mean_mean: '#28a428',
    doy_max_max: '#1e7a1e',
  },
}

function processProjectedAlaskaData(hg, traces: Data[]) {
  let projectedTempData = hg['projected']['2034-2065']

  let hydroYearProjectedMeanMax = processLowessAndHydroYear(
    projectedTempData['doy_mean_max'],
    doys
  )

  let hydroYearProjectedMeanMin = processLowessAndHydroYear(
    projectedTempData['doy_mean_min'],
    doys
  )

  let meanMinTrace = {
    x: hydroDoys,
    y: hydroYearProjectedMeanMin,
    type: 'scatter',
    mode: 'line',
    line: { color: scenarioColors['historical'].fill, width: 0 },
    fillcolor: scenarioColors['projected'].fill,
    showlegend: false,
  }

  let meanMaxTrace = {
    x: hydroDoys,
    y: hydroYearProjectedMeanMax,
    type: 'scatter',
    fill: 'tonexty',
    line: { color: scenarioColors['historical'].fill, width: 0 },
    fillcolor: scenarioColors['projected'].fill,
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
    let traceData = projectedTempData[key]
    let traceName = traceConfig[key].label

    let hydroOrderedSmoothedY = processLowessAndHydroYear(traceData, doys)
    let trace = {
      x: hydroDoys,
      y: hydroOrderedSmoothedY,
      type: 'scatter',
      mode: 'lines',
      line: {
        shape: 'spline',
        color: scenarioColors['projected'][key],
      },
      name: traceName,
    }
    traces.push(trace)
  })
}

// hg is assumed to be non-null, raw, and only dynamic land cover now.
const buildChart = hg => {
  let traces: Data[] = []

  // Create historical trace
  let historicalTempData = hg['historical']

  let hydroYearHistoricalDataMin = processLowessAndHydroYear(
    historicalTempData['doy_min'],
    doys
  )
  let hydroYearHistoricalDataMean = processLowessAndHydroYear(
    historicalTempData['doy_mean'],
    doys
  )
  let hydroYearHistoricalDataMax = processLowessAndHydroYear(
    historicalTempData['doy_max'],
    doys
  )

  let historicalMinTrace = {
    x: hydroDoys,
    y: hydroYearHistoricalDataMin,
    type: 'scatter',
    mode: 'line',
    line: { color: scenarioColors['historical'].fill, width: 0 },
    name: 'Minimum historical, 1990-2021',
    showlegend: false,
  }

  let historicalMaxTrace = {
    x: hydroDoys,
    y: hydroYearHistoricalDataMax,
    type: 'scatter',
    fill: 'tonexty',
    mode: 'none',
    fillcolor: scenarioColors['historical'].fill,
    name: 'Minimum/maximum historical, 1990-2021',
  }

  let historicalMeanTrace = {
    x: hydroDoys,
    y: hydroYearHistoricalDataMean,
    type: 'scatter',
    mode: 'line',
    line: { color: '#f0f0f0', width: 3 },
    name: 'Mean historical, 1990-2021',
  }

  traces.push(historicalMinTrace)
  traces.push(historicalMaxTrace)
  traces.push(historicalMeanTrace)

  processProjectedAlaskaData(hg, traces)

  // These numbers correspond to the 1st of each month in a 366-day year,
  // oriented by the hydro year.
  let xTickVals = [274, 305, 335, 1, 32, 60, 91, 121, 152, 182, 213, 244]
  let xTickLabels = xTickVals.map((doy: number) => {
    return doyToDateString(doy, true)
  })

  let gaugeIdLine = gaugeId.value
    ? `<br><span style="font-size: 0.8em;">Gage ID: ${gaugeId.value}</span>`
    : ''
  let scenarioName = scenarioFullNames['ssp370']
  let titleText = `Modeled water temperature, 2034-2065, ${scenarioName}${gaugeIdLine}`
  let yAxisLabel = 'Water temperature, °C'

  let xAxisConfig = {
    type: 'category',
    tickmode: 'array',
    tickvals: xTickVals,
    ticktext: xTickLabels,
  }

  // Min/max need to be logarithmic to work with Plotly.js log chart type.
  let { yMin, yMax } = getDataRange(hg)

  let yAxisConfig = {
    autorange: false,
    range: [yMin, yMax],
  }

  let legendConfig = {
    orientation: 'h',
    yanchor: 'top',
    y: -0.2,
    xanchor: 'center',
    x: 0.5,
  }

  let isTwoLineTitle = gaugeId.value ? true : false
  const isAlaskaData = true

  let layout = getLayout(
    'temperatureHydrograph',
    titleText,
    yAxisLabel,
    xAxisConfig,
    yAxisConfig,
    legendConfig,
    isTwoLineTitle,
    isAlaskaData
  )

  const pngName = `temperature-hydrograph_${segmentId.value}_2034-2065`
  const config = getConfig(pngName)

  $Plotly.newPlot('temperature-hydrograph', traces, layout, config)
}
</script>

<template>
  <div id="temperature-hydrograph"></div>
</template>

<style lang="scss" scoped></style>
