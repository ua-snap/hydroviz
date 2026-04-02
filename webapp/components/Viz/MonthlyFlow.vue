<script setup lang="ts">
import { watch, toRaw } from 'vue'
import { getLayout, getConfig, initializeChart } from '~/utils/chart'
const { $Plotly, $_ } = useNuxtApp()
import type { Data } from 'plotly.js'

const props = defineProps(['streamMonthlyFlow'])

import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { appContext, appEra } = storeToRefs(streamSegmentStore)

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

let xTickValOffsets: Record<string, number> = {}

const getOffsetXTickVals = (scenario: string) => {
  let xTickVals = $_.range(Object.values(monthLabels).length)
  let offset = xTickValOffsets[scenario]
  let offsetXTickVals = xTickVals.map(tickVal => {
    return tickVal + offset
  })
  return offsetXTickVals
}

// stats is assumed to be non-null, raw, and only dynamic land cover now.
const buildChart = () => {
  let traces: Data[] = []

  let scenarios: string[]
  if (appContext.value === 'mid') {
    scenarios = ['rcp60']
  } else {
    scenarios = ['rcp45', 'rcp85']
  }

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
    x: getOffsetXTickVals('historical'),
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

  let scenarioLabels = {
    rcp45: 'Stabilizing Emissions (RCP 4.5)',
    rcp60: 'Stabilizing High Emissions (RCP 6.0)',
    rcp85: 'Increasing Emissions (RCP 8.5)',
  }

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

  scenarios.forEach(scenario => {
    let projectedFlowData =
      props.streamMonthlyFlow['projected'][appEra.value][scenario]

    let xTickVals = getOffsetXTickVals(scenario)

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
        name: `Projected, ${scenarioLabels[scenario]}`,
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

  const titleText: string = `Mean monthly modeled flow rate, ${appEra.value}`

  let xAxisSettings = {
    tickvals: $_.range(Object.values(monthLabels).length),
    ticktext: Object.values(monthLabels),
    dtick: 1,
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
    'Mean monthly flow, cf/s',
    xAxisSettings,
    {},
    legendConfig
  )

  const config = getConfig()

  $Plotly.newPlot('monthly-flow', traces, layout, config)
}
</script>

<template>
  <div id="monthly-flow"></div>
</template>

<style lang="scss" scoped></style>
