<script setup lang="ts">
import { watch, toRaw } from 'vue'
import { doyToDateString } from '~/utils/general'
import { getLayout, getConfig, initializeChart } from '~/utils/chart'
const { $Plotly, $_ } = useNuxtApp()
import type { Data } from 'plotly.js'

import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
const { appContext, appEra } = storeToRefs(streamSegmentStore)

const props = defineProps(['streamMinMaxFlowDates'])

onMounted(() => {
  initializeChart(
    $Plotly,
    'min-max-flow-dates',
    buildChart,
    toRaw(props.streamMinMaxFlowDates)
  )
})

watch([appContext, appEra], () => {
  initializeChart(
    $Plotly,
    'min-max-flow-dates',
    buildChart,
    toRaw(props.streamMinMaxFlowDates)
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

  let scenarioLabels = {
    rcp45: 'RCP 4.5',
    rcp60: 'RCP 6.0',
    rcp85: 'RCP 8.5',
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
    let stats = ['max']
    stats.forEach(stat => {
      let historicalFlow = [
        props.streamMinMaxFlowDates['historical'][stat]['flow'],
      ]
      let historicalFlowDate = [
        props.streamMinMaxFlowDates['historical'][stat]['date'],
      ]

      let customdataHistorical: string[][] = []
      historicalFlowDate.forEach((doy: number, index: number) => {
        let dayString = doyToDateString(doy)

        customdataHistorical.push([dayString])
        historicalFlowDate[index] = convertTo360(doy)
      })

      let historicalTraceLabel: string
      let projectedTraceLabel: string
      let historicalColor: string
      let projectedColor: string
      let historicalHovertextLabel: string
      let projectedHovertextLabel: string

      if (stat == 'min') {
        historicalTraceLabel = 'Minimum flow date, historical, 1976-2005'
        projectedTraceLabel = 'Minimum flow date, modeled, ' + appEra.value
        historicalHovertextLabel = 'Min historical flow'
        projectedHovertextLabel = 'Min projected flow'
        historicalColor = '#888888'
        projectedColor = '#6baed6'
      } else {
        historicalTraceLabel = 'Maximum flow date, historical, 1976-2005'
        projectedTraceLabel = 'Maximum flow date, modeled, ' + appEra.value
        historicalHovertextLabel = 'Max historical flow'
        projectedHovertextLabel = 'Max projected flow'
        historicalColor = '#333333'
        projectedColor = '#3182bd'
      }

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
        props.streamMinMaxFlowDates['projected'][appEra.value][scenario][stat][
          'flow'
        ]
      let projectedDates = $_.cloneDeep(
        props.streamMinMaxFlowDates['projected'][appEra.value][scenario][stat][
          'date'
        ]
      )

      let customdataProjected: string[][] = []
      projectedDates.forEach((doy: number, index: number) => {
        let dayString = doyToDateString(doy)
        customdataProjected.push([dayString])
        projectedDates[index] = convertTo360(doy)
      })

      let traceLabel = projectedTraceLabel + `, ${scenarioLabels[scenario]}`

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
  })

  let traces = historicalTraces.concat(projectedTraces)
  const titleText = 'Flow rate at date of annual maximum daily flow'

  const layout = getLayout(titleText, '')

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
      x: [0, 0.45],
      y: [0, 1],
    }
  }

  let axisColor = 'rgba(0,0,0,0.08)'

  layout['polar'] = {
    title: {
      text: 'Minimum flow date',
      font: { size: 14 },
    },
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
    },
    domain: firstPlotDomain,
  }

  if (appContext.value === 'extremes') {
    // Ensure polar2 axis settings are applied to the "polar2" subplot
    layout['polar2'] = {
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
      },
      domain: { x: [0.55, 1], y: [0, 1] }, // Make sure domain is set here, not below
    }
  }

  // Add an annotation (title) below each subplot
  if (appContext.value === 'extremes') {
    layout['annotations'] = [
      {
        text: plotLabels['rcp45'],
        x: 0.062,
        y: -0.15,
        showarrow: false,
        font: { size: 14 },
      },
      {
        text: plotLabels['rcp85'],
        x: 0.946,
        y: -0.15,
        showarrow: false,
        font: { size: 14 },
      },
    ]
  } else {
    layout['annotations'] = [
      {
        text: plotLabels['rcp60'],
        x: 0.505,
        y: -0.15,
        showarrow: false,
        font: { size: 14 },
      },
    ]
  }

  const config = getConfig('min-max-flow-dates')

  $Plotly.newPlot('min-max-flow-dates', traces, layout, config)
}
</script>

<template>
  <div id="min-max-flow-dates"></div>
</template>
