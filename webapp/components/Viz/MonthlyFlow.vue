<script setup lang="ts">
import { watch, toRaw } from 'vue'
import { getLayout, getConfig, initializeChart } from '~/utils/chart'
const { $Plotly, $_ } = useNuxtApp()
import type { Data } from 'plotly.js-dist-min'

const props = defineProps(['streamStats'])

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
    toRaw(props.streamStats.data.static)
  )
})

watch(props.streamStats, newValue => {
  initializeChart(
    $Plotly,
    'monthly-flow',
    buildChart,
    toRaw(newValue.data.static)
  )
})

// Returns an object with keys for each month, and values are arrays of flow
// values across all projected models.
function buildMonthlyFlowData(monthlyFlowData, scenario: Scenario, era: Era) {
  if (!monthlyFlowData || !era) {
    throw 'stream stats data missing or era missing'
  }

  // Initialize each month with an empty array.
  let monthValues: Record<string, number[]> = {}
  Object.keys(monthLabels).forEach(monthKey => {
    monthValues[monthKey] = []
  })

  // Fill each month's array with values across all models.
  Object.keys(monthlyFlowData).forEach(model => {
    if (scenario in monthlyFlowData[model]) {
      Object.keys(monthLabels).forEach(monthKey => {
        monthValues[monthKey]!.push(
          monthlyFlowData[model][scenario][era][monthKey]
        )
      })
    }
  })

  return monthValues
}

// stats is assumed to be non-null, raw, and only dynamic land cover now.
const buildChart = stats => {
  let traces: Data[] = []

  // Remove the historical modeled dataset (Maurer) & build that data for hydrograph
  let historicalMaurer: Record<string, any> = {}
  historicalMaurer['Maurer'] = stats['Maurer']
  delete stats['Maurer']

  // Create historical trace
  let historicalFlowData = buildMonthlyFlowData(
    historicalMaurer,
    'historical',
    '1976-2005'
  )

  // Flatten object of arrays into just one array of historical monthly values.
  let historicalFlowFlattened = $_.map(
    Object.values(historicalFlowData),
    (monthValues: number[]) => {
      return monthValues[0]
    }
  )

  // Historical needs to have been removed.
  let projectedFlowData = buildMonthlyFlowData(stats, 'rcp85', '2046-2075')

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
    y: historicalFlowFlattened,
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
