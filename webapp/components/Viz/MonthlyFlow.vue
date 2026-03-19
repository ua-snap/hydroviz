<script setup lang="ts">
import { watch, toRaw } from 'vue'
import { getLayout, getConfig, initializeChart } from '~/utils/chart'
const { $Plotly, $_ } = useNuxtApp()
import type { Data } from 'plotly.js'

const props = defineProps(['streamMonthlyFlow'])

import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { appContext } = storeToRefs(streamSegmentStore)

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

watch(props.streamMonthlyFlow, newValue => {
  initializeChart($Plotly, 'monthly-flow', buildChart, toRaw(newValue))
})

watch(appContext, () => {
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

  // Create historical trace
  let historicalFlowData = props.streamMonthlyFlow['historical']

  // Convert historical data into an array in the order of monthLabels.
  let historicalFlowDataArray = $_.map(Object.keys(monthLabels), monthKey => {
    return historicalFlowData[monthKey]
  })

  let projectedFlowData
  if (appContext.value === 'mid') {
    projectedFlowData = []
    Object.keys(monthLabels).forEach(monthKey => {
      projectedFlowData.push(
        props.streamMonthlyFlow['projected'][appContext.value][monthKey]
      )
    })
  } else {
    projectedFlowData = props.streamMonthlyFlow['projected'][appContext.value]
  }

  // For "extremes" mode, show a boxplot populated by all values across all models
  // and scenarios for each month. For "mid" mode, show a single point of the mean
  // of all models at RCP 6.0 for each month.
  if (appContext.value === 'extremes') {
    // Each box plot needs to be its own trace (due to Plotly.js limitations),
    // and a new legend entry is added for each trace. To clean this up, show
    // the legend for just the first box plot trace, hide the rest, and override
    // the name of the first legend entry to make it more general & apply to all
    // of the box plots. Also, make sure all box plots have the same color.
    let showLegend = true
    Object.keys(monthLabels).forEach(monthKey => {
      traces.push({
        x: Array(projectedFlowData[monthKey].length).fill(
          monthLabels[monthKey]
        ),
        y: projectedFlowData[monthKey],
        type: 'box',
        name: 'Projected (Modeled), 2046-2075',
        marker: { color: '#3182bd', size: 8 },
        line: { color: '#3182bd', width: 1.5 },
        fillcolor: '#6baed6',
        showlegend: showLegend,
      })
      showLegend = false
    })
  } else {
    traces.push({
      x: Object.values(monthLabels),
      y: projectedFlowData,
      type: 'scatter',
      mode: 'markers',
      name: 'Projected (Modeled), 2046-2075',
      marker: { color: '#3182bd', size: 8 },
    })
  }

  let monthMarkers = Object.values(monthLabels)
  traces.push({
    x: monthMarkers,
    y: historicalFlowDataArray,
    type: 'scatter',
    mode: 'markers',
    name: 'Historical (Modeled), 1976-2005',
    marker: {
      size: 8,
      symbol: 'square',
      color: '#666666',
    },
  })

  const titleText: string = 'Mean monthly modeled flow rate'

  const layout = getLayout(titleText, 'Mean monthly flow, cf/s', {
    type: 'category',
    tickmode: 'array',
  })

  const config = getConfig()

  $Plotly.newPlot('monthly-flow', traces, layout, config)
}
</script>

<template>
  <div id="monthly-flow"></div>
</template>

<style lang="scss" scoped></style>
