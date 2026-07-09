<script setup lang="ts">
import { watch, toRaw } from 'vue'
import {
  getLayout,
  getConfig,
  initializeChart,
  getDataRange,
  getOffsetXTickVals,
} from '~/utils/chart'
const { $Plotly, $_ } = useNuxtApp()
import type { Data } from 'plotly.js'

const props = defineProps(['streamMonthlyTemperature'])

import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { segmentId, gageId, appContext, appEra } = storeToRefs(streamSegmentStore)

const monthKeys = [
  'oct',
  'nov',
  'dec',
  'jan',
  'feb',
  'mar',
  'apr',
  'may',
  'jun',
  'jul',
  'aug',
  'sep',
]

const monthLabels = {
  oct: 'Oct',
  nov: 'Nov',
  dec: 'Dec',
  jan: 'Jan',
  feb: 'Feb',
  mar: 'Mar',
  apr: 'Apr',
  may: 'May',
  jun: 'Jun',
  jul: 'Jul',
  aug: 'Aug',
  sep: 'Sep',
}

onMounted(() => {
  initializeChart(
    $Plotly,
    'monthly-temperature',
    buildChart,
    toRaw(props.streamMonthlyTemperature)
  )
})

watch([appContext, appEra], () => {
  initializeChart(
    $Plotly,
    'monthly-temperature',
    buildChart,
    toRaw(props.streamMonthlyTemperature)
  )
})

// stats is assumed to be non-null, raw, and only dynamic land cover now.
const buildChart = () => {
  let traces: Data[] = []

  // Create historical trace
  let historicalTempData = props.streamMonthlyTemperature['historical']

  // Convert historical data into an array in the order of monthKeys.
  let historicalTempDataArray = $_.map(monthKeys, monthKey => {
    return historicalTempData[`wt_mean_${monthKey}`]
  })

  let xTickValOffsets = {
    historical: -0.11,
    projected: 0.2,
  }

  let historicalTrace = {
    x: getOffsetXTickVals(xTickValOffsets, 'historical'),
    y: historicalTempDataArray,
    type: 'scatter',
    mode: 'markers',
    name: 'Historical, 1990-2021',
    marker: {
      size: 9,
      symbol: 'diamond',
      color: '#333333',
    },
  }

  traces.push(historicalTrace)

  // Monthly temperature API doesn't split by scenario - all 6 models combined
  let projectedTempData =
    props.streamMonthlyTemperature['projected']['2034-2065']
  let boxWidth = 0.3
  let showLegend = true

  // Use the same xTickVals as CONUS rcp60 scenario
  let xTickVals = getOffsetXTickVals(xTickValOffsets, 'projected')

  monthKeys.forEach((monthKey, idx) => {
    let tempValues = projectedTempData[`wt_mean_${monthKey}`]

    let trace = {
      x0: xTickVals[idx],
      y: tempValues,
      type: 'box',
      name: 'Projected',
      marker: { color: '#4Caf50', size: 8 },
      line: { color: '#4Caf50', width: 1.5 },
      fillcolor: '#b6e5b6',
      showlegend: showLegend,
      width: boxWidth,
    }
    traces.push(trace)
    showLegend = false
  })

  let gageIdLine = gageId.value
    ? `<br><span style="font-size: 0.8em;">Gage ID: ${gageId.value}</span>`
    : ''
  const titleText = `Mean monthly modeled water temperature, 2034-2065${gageIdLine}`

  let xAxisSettings = {
    tickvals: $_.range(Object.values(monthLabels).length),
    ticktext: Object.values(monthLabels),
    dtick: 1,
  }

  let { yMin, yMax } = getDataRange(props.streamMonthlyTemperature)

  let yAxisSettings = {
    range: [yMin, yMax],
    autorange: false,
  }

  let legendConfig = {
    orientation: 'h',
    yanchor: 'top',
    y: -0.2,
    xanchor: 'center',
    x: 0.5,
  }

  let isTwoLineTitle = gageId.value ? true : false
  const isAlaskaData = true

  let layout = getLayout(
    'monthlyTemperature',
    titleText,
    'Mean monthly temperature, °C',
    xAxisSettings,
    yAxisSettings,
    legendConfig,
    isTwoLineTitle,
    isAlaskaData
  )

  const pngName = `monthly-temperature_${segmentId.value}_2034-2065`
  const config = getConfig(pngName)

  $Plotly.newPlot('monthly-temperature', traces, layout, config)
}
</script>

<template>
  <div id="monthly-temperature"></div>
</template>

<style lang="scss" scoped></style>
