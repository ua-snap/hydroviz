<script setup lang="ts">
import { watch, toRaw } from 'vue'
import { getLayout, getConfig, initializeChart } from '~/utils/chart'
const { $Plotly, $_ } = useNuxtApp()
import type { Data } from 'plotly.js'

const props = defineProps(['streamMonthlyFlow'])

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

// stats is assumed to be non-null, raw, and only dynamic land cover now.
const buildChart = () => {
  let traces: Data[] = []

  // Create historical trace
  let historicalFlowData = props.streamMonthlyFlow['historical']

  // Convert historical data into an array in the order of monthLabels.
  let historicalFlowDataArray = $_.map(Object.keys(monthLabels), monthKey => {
    return historicalFlowData[monthKey]
  })

  // Historical needs to have been removed.
  let projectedFlowData = props.streamMonthlyFlow['projected']

  // Each box plot needs to be its own trace (due to Plotly.js limitations),
  // and a new legend entry is added for each trace. To clean this up, show
  // the legend for just the first box plot trace, hide the rest, and override
  // the name of the first legend entry to make it more general & apply to all
  // of the box plots. Also, make sure all box plots have the same color.
  let showLegend = true
  Object.keys(monthLabels).forEach(monthKey => {
    traces.push({
      x: Array(projectedFlowData[monthKey].length).fill(monthLabels[monthKey]),
      y: projectedFlowData[monthKey],
      type: 'box',
      name: 'Projected (Modeled), 2046-2075',
      marker: { color: '#3182bd' },
      line: { color: '#3182bd', width: 1.5 },
      fillcolor: '#6baed6',
      showlegend: showLegend,
    })
    showLegend = false
  })

  let monthMarkers = Object.values(monthLabels)
  traces.push({
    x: monthMarkers,
    y: historicalFlowDataArray,
    type: 'scatter',
    mode: 'markers',
    name: 'Historical (Modeled), 1976-2005',
    marker: {
      size: 8,
      color: '#666666',
    },
  })

  const titleText: string = 'Mean monthly modeled flow rate, RCP 8.5'

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
