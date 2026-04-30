<script setup lang="ts">
import { watch, toRaw } from 'vue'
import { doyToDateString } from '~/utils/general'
import {
  getLayout,
  getConfig,
  initializeChart,
  getDataRange,
} from '~/utils/chart'
const { $Plotly, $_ } = useNuxtApp()
import type { Data } from 'plotly.js'

import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
const { appContext, appEra } = storeToRefs(streamSegmentStore)

const props = defineProps(['streamMaxFlowDates'])

onMounted(() => {
  initializeChart(
    $Plotly,
    'max-flow-dates',
    buildChart,
    toRaw(props.streamMaxFlowDates)
  )
})

watch([appContext, appEra], () => {
  initializeChart(
    $Plotly,
    'max-flow-dates',
    buildChart,
    toRaw(props.streamMaxFlowDates)
  )
})

// Values exceeding 360 cannot be plotted on a Plotly.js polarscatter chart.
// So, slightly squeeze 366 calendar to a 360 degree representation.
const convertTo360 = (doy: number) => {
  return ((doy - 1) / 366) * 360
}

const buildChart = () => {
  let historicalTraces: Data[] = []
  let projectedTraces: Data[] = []

  let scenarios: string[]
  if (appContext.value === 'mid') {
    scenarios = ['rcp60']
  } else {
    scenarios = ['rcp45', 'rcp85']
  }

  let scenarioColors = {
    historical: '#333333',
    rcp45: '#6baed6',
    rcp60: '#32cd32',
    rcp85: '#e06666',
  }

  let scenarioSymbols = {
    historical: 'diamond',
    rcp45: 'square',
    rcp60: 'circle',
    rcp85: 'cross',
  }

  let plotLabels = {
    rcp45: 'Stabilizing Emissions (RCP 4.5)',
    rcp60: 'Stabilizing High Emissions (RCP 6.0)',
    rcp85: 'Increasing Emissions (RCP 8.5)',
  }

  scenarios.forEach(scenario => {
    let historicalFlow = [props.streamMaxFlowDates['historical']['flow']]
    let historicalFlowDate = [props.streamMaxFlowDates['historical']['date']]

    let customdataHistorical: string[][] = []
    historicalFlowDate.forEach((doy: number, index: number) => {
      let dayString = doyToDateString(doy)

      customdataHistorical.push([dayString])
      historicalFlowDate[index] = convertTo360(doy)
    })

    const historicalTraceLabel = 'Historical, 1976-2005'
    const projectedTraceLabel = 'Projected'
    const historicalHovertextLabel = 'Max historical flow'
    const projectedHovertextLabel = 'Max projected flow'

    let showLegend = false
    if (
      (appContext.value === 'extremes' && scenario === 'rcp45') ||
      appContext.value === 'mid'
    ) {
      showLegend = true
    }

    let historicalTrace = {
      r: historicalFlow,
      theta: historicalFlowDate,
      type: 'scatterpolar',
      mode: 'markers',
      name: historicalTraceLabel,
      marker: {
        size: 9,
        color: scenarioColors['historical'],
        symbol: scenarioSymbols['historical'],
      },
      customdata: customdataHistorical,
      hovertemplate: `%{customdata[0]}, 1976-2005<br />${historicalHovertextLabel}: %{r:,} cf/s<extra></extra>`,
      showlegend: showLegend,
    }
    if (appContext.value === 'extremes' && scenario === 'rcp45') {
      historicalTrace['subplot'] = 'polar2'
    }
    historicalTraces.push(historicalTrace)

    let projectedFlows =
      props.streamMaxFlowDates['projected'][appEra.value][scenario]['flow']
    let projectedDates = $_.cloneDeep(
      props.streamMaxFlowDates['projected'][appEra.value][scenario]['date']
    )

    let customdataProjected: string[][] = []
    projectedDates.forEach((doy: number, index: number) => {
      let dayString = doyToDateString(doy)
      customdataProjected.push([dayString])
      projectedDates[index] = convertTo360(doy)
    })

    let traceLabel = projectedTraceLabel + `, ${plotLabels[scenario]}`

    let trace = {
      r: projectedFlows,
      theta: projectedDates,
      type: 'scatterpolar',
      mode: 'markers',
      name: traceLabel,
      marker: {
        size: 8,
        color: scenarioColors[scenario],
        symbol: scenarioSymbols[scenario],
      },
      customdata: customdataProjected,
      hovertemplate: `%{customdata[0]}, 2046-2075<br />${projectedHovertextLabel}: %{r:,} cf/s<extra></extra>`,
    }

    if (appContext.value === 'mid') {
      trace['subplot'] = 'polar'
    } else {
      if (scenario === 'rcp45') {
        trace['subplot'] = 'polar'
      } else if (scenario === 'rcp85') {
        trace['subplot'] = 'polar2'
      }
    }

    projectedTraces.push(trace)
  })

  // Reverse projected traces because the legend gets reversed later.
  // This will ultimately keep the legend order the same as the subplot order.
  projectedTraces.reverse()

  let traces = projectedTraces.concat(historicalTraces)
  const titleText = `Modeled flow rate at date of annual maximum daily flow, ${appEra.value}`

  let legendConfig = {
    orientation: 'h',
    yanchor: 'top',
    y: -0.15,
    xanchor: 'center',
    x: 0.5,
    traceorder: 'reversed',
  }

  const layout = getLayout(titleText, '', {}, {}, legendConfig)

  let firstOfMonthValues = [
    1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335,
  ]

  firstOfMonthValues = firstOfMonthValues.map((doy: number) => {
    return convertTo360(doy)
  })

  let firstPlotDomain = {}
  if (appContext.value === 'mid') {
    firstPlotDomain = {
      x: [0, 1],
      y: [0, 1],
    }
  } else {
    firstPlotDomain = {
      x: [0, 0.58],
      y: [0, 1],
    }
  }

  let axisColor = 'rgba(0,0,0,0.08)'

  let keysToExclude = ['date', 'min']
  let { yMin, yMax } = getDataRange(props.streamMinMaxFlowDates, keysToExclude)

  layout['polar'] = {
    angularaxis: {
      tickmode: 'array',
      tickvals: firstOfMonthValues,
      ticktext: [
        'Jan',
        'Feb',
        'Mar',
        'Apr',
        'May',
        'Jun',
        'Jul',
        'Aug',
        'Sep',
        'Oct',
        'Nov',
        'Dec',
      ],
      direction: 'clockwise',
      gridcolor: axisColor,
    },
    radialaxis: {
      angle: 90,
      tickangle: 90,
      ticksuffix: ' cf/s',
      tickmode: 'auto',
      nticks: 4,
      gridcolor: axisColor,
      range: [yMin, yMax],
    },
    domain: firstPlotDomain,
  }

  if (appContext.value === 'extremes') {
    layout['polar2'] = $_.cloneDeep(layout['polar'])
    layout['polar2']['domain'] = { x: [0.42, 1], y: [0, 1] }
  }

  layout['margin'] = { t: 100 }
  layout['height'] = 500

  const config = getConfig('max-flow-dates')

  $Plotly.newPlot('max-flow-dates', traces, layout, config)
}
</script>

<template>
  <div id="max-flow-dates" class="mb-5"></div>
</template>
