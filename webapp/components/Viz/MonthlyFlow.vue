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
import { scenarioFullNames } from '~/types/modelsScenarios'

const props = defineProps(['streamMonthlyFlow'])

import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { segmentId, gageId, appContext, appEra } = storeToRefs(streamSegmentStore)

const monthLabels = {
  ma21: 'Oct',
  ma22: 'Nov',
  ma23: 'Dec',
  ma12: 'Jan',
  ma13: 'Feb',
  ma14: 'Mar',
  ma15: 'Apr',
  ma16: 'May',
  ma17: 'Jun',
  ma18: 'Jul',
  ma19: 'Aug',
  ma20: 'Sep',
}

onMounted(() => {
  initializeChart(
    $Plotly,
    'monthly-flow',
    buildChart,
    toRaw(props.streamMonthlyFlow)
  )
})

watch([appContext, appEra], () => {
  initializeChart(
    $Plotly,
    'monthly-flow',
    buildChart,
    toRaw(props.streamMonthlyFlow)
  )
})

// stats is assumed to be non-null, raw, and only dynamic land cover now.
const buildChart = () => {
  let traces: Data[] = []

  const isAlaskaData = !props.streamMonthlyFlow['projected'][appEra.value]

  let scenarios: string[]
  if (appContext.value === 'mid') {
    scenarios = ['rcp60']
  } else {
    scenarios = ['rcp45', 'rcp85']
  }

  let xTickValOffsets: Record<string, number> = {}
  if (appContext.value === 'mid') {
    xTickValOffsets = {
      historical: -0.11,
      rcp60: 0.2,
    }
  } else {
    xTickValOffsets = {
      historical: -0.2,
      rcp45: 0,
      rcp85: 0.25,
    }
  }

  // Create historical trace
  let historicalFlowData = props.streamMonthlyFlow['historical']

  // Convert historical data into an array in the order of monthLabels.
  let historicalFlowDataArray = $_.map(Object.keys(monthLabels), monthKey => {
    return historicalFlowData[monthKey]
  })

  let historicalTrace = {
    x: getOffsetXTickVals(xTickValOffsets, 'historical'),
    y: historicalFlowDataArray,
    type: 'scatter',
    mode: 'markers',
    name: 'Historical, 1976-2005',
    marker: {
      size: 9,
      symbol: 'diamond',
      color: '#333333',
    },
  }

  traces.push(historicalTrace)

  let scenarioColors = {
    rcp45: {
      stroke: '#4293d6',
      fill: '#9ecae1',
    },
    rcp60: {
      stroke: '#4Caf50',
      fill: '#b6e5b6',
    },
    rcp85: {
      stroke: '#e04a4a',
      fill: '#f28b82',
    },
  }

  if (isAlaskaData) {
    let projectedFlowData = props.streamMonthlyFlow['projected']['2034-2065']
    let boxWidth = 0.3
    let showLegend = true

    // Alaska data doesn't have multiple scenarios, but use the same xTickVals
    // as CONUS rcp60 scenario (i.e., one diamond and one box plot per month).
    let xTickVals = getOffsetXTickVals(xTickValOffsets, 'rcp60')

    Object.keys(monthLabels).forEach((monthKey, idx) => {
      let trace = {
        x0: xTickVals[idx],
        y: projectedFlowData[monthKey],
        type: 'box',
        name: 'Projected',
        marker: { color: scenarioColors['rcp60'].stroke, size: 8 },
        line: { color: scenarioColors['rcp60'].stroke, width: 1.5 },
        fillcolor: scenarioColors['rcp60'].fill,
        showlegend: showLegend,
        width: boxWidth, // Add width property to make boxes wider
      }
      traces.push(trace)
      showLegend = false
    })
  } else {
    scenarios.forEach(scenario => {
      let projectedFlowData =
        props.streamMonthlyFlow['projected'][appEra.value][scenario]

      let xTickVals = getOffsetXTickVals(xTickValOffsets, scenario)

      let boxWidth: number
      if (appContext.value === 'extremes') {
        boxWidth = 0.2
      } else {
        boxWidth = 0.3
      }

      let showLegend = true
      Object.keys(monthLabels).forEach((monthKey, idx) => {
        let trace = {
          x0: xTickVals[idx],
          y: projectedFlowData[monthKey],
          type: 'box',
          name: `Projected, ${scenarioFullNames[scenario]}`,
          marker: { color: scenarioColors[scenario].stroke, size: 8 },
          line: { color: scenarioColors[scenario].stroke, width: 1.5 },
          fillcolor: scenarioColors[scenario].fill,
          showlegend: showLegend,
          width: boxWidth, // Add width property to make boxes wider
        }
        traces.push(trace)
        showLegend = false
      })
    })
  }

  let gageIdLine = gageId.value
    ? `<br><span style="font-size: 0.8em;">Gage ID: ${gageId.value}</span>`
    : ''
  const titleText: string = isAlaskaData
    ? `Mean monthly modeled flow rate, 2034-2065${gageIdLine}`
    : `Mean monthly modeled flow rate, ${appEra.value}${gageIdLine}`

  let xAxisSettings = {
    tickvals: $_.range(Object.values(monthLabels).length),
    ticktext: Object.values(monthLabels),
    dtick: 1,
  }

  let { yMin, yMax } = getDataRange(props.streamMonthlyFlow)

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

  let layout = getLayout(
    'monthlyFlow',
    titleText,
    'Mean monthly flow, cf/s',
    xAxisSettings,
    yAxisSettings,
    legendConfig,
    isTwoLineTitle,
    isAlaskaData
  )

  let pngName: string
  if (isAlaskaData) {
    pngName = `monthly-flow_${segmentId.value}_2034-2065`
  } else {
    if (appContext.value === 'mid') {
      pngName = `monthly-flow_${segmentId.value}_rcp60_${appEra.value}`
    } else {
      pngName = `monthly-flow_${segmentId.value}_rcp45-rcp85_${appEra.value}`
    }
  }

  let config = getConfig(pngName)

  $Plotly.newPlot('monthly-flow', traces, layout, config)
}
</script>

<template>
  <div id="monthly-flow"></div>
</template>

<style lang="scss" scoped></style>
