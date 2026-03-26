<script setup lang="ts">
import { watch, toRaw } from 'vue'
import { doyToDateString } from '~/utils/general'
import { getLayout, getConfig, initializeChart } from '~/utils/chart'
const { $Plotly, $_ } = useNuxtApp()
import type { Data } from 'plotly.js'

import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
const { appContext } = storeToRefs(streamSegmentStore)

const props = defineProps(['streamMinMaxFlowDates'])

onMounted(() => {
  initializeChart(
    $Plotly,
    'min-max-flow-dates',
    buildChart,
    toRaw(props.streamMinMaxFlowDates)
  )
})

watch(appContext, () => {
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
  let allFlows = [props.streamMinMaxFlowDates['historical']['max']['flow']]
  allFlows = allFlows.concat(
    props.streamMinMaxFlowDates['projected']['extremes']['max']['flow']
  )
  let upperLimit = $_.max(allFlows)

  let historicalTraces: Data[] = []
  let projectedTraces: Data[] = []
  let stats = ['min', 'max']
  stats.forEach(stat => {
    let historicalFlow = [
      props.streamMinMaxFlowDates['historical'][stat]['flow'],
    ]
    let historicalFlowDate = [
      convertTo360(props.streamMinMaxFlowDates['historical'][stat]['date']),
    ]

    let projectedFlows =
      props.streamMinMaxFlowDates['projected'][appContext.value][stat]['flow']
    let projectedDates = $_.cloneDeep(
      props.streamMinMaxFlowDates['projected'][appContext.value][stat]['date']
    )

    if (appContext.value === 'mid') {
      projectedFlows = [projectedFlows]
      projectedDates = [projectedDates]
    }

    let customdataHistorical: string[][] = []
    historicalFlowDate.forEach((doy: number, index: number) => {
      let dayString = doyToDateString(
        props.streamMinMaxFlowDates['historical'][stat]['date']
      )

      customdataHistorical.push([dayString])
      historicalFlowDate[index] = convertTo360(doy)
    })

    let customdataProjected: string[][] = []
    projectedDates.forEach((doy: number, index: number) => {
      let dayString = doyToDateString(doy)
      customdataProjected.push([dayString])
      projectedDates[index] = convertTo360(doy)
    })

    let historicalTraceLabel: string
    let projectedTraceLabel: string
    let historicalColor: string
    let projectedColor: string
    let historicalHovertextLabel: string
    let projectedHovertextLabel: string
    if (stat === 'min') {
      historicalTraceLabel = 'Minimum flow date, historical, 1976-2005'
      projectedTraceLabel = 'Minimum flow date, modeled, 2046-2075'
      historicalColor = '#aaaaaa'
      projectedColor = '#6baed6'
      historicalHovertextLabel = 'Min historical flow'
      projectedHovertextLabel = 'Min projected flow'
    } else {
      historicalTraceLabel = 'Maximum flow date, historical, 1976-2005'
      projectedTraceLabel = 'Maximum flow date, modeled, 2046-2075'
      historicalColor = '#666666'
      projectedColor = '#3182bd'
      historicalHovertextLabel = 'Max historical flow'
      projectedHovertextLabel = 'Max projected flow'
    }

    historicalTraces.push({
      r: historicalFlow,
      theta: historicalFlowDate,
      type: 'scatterpolar',
      mode: 'markers',
      name: historicalTraceLabel,
      marker: {
        size: 8,
        color: historicalColor,
      },
      customdata: customdataHistorical,
      hovertemplate: `%{customdata[0]}, 1976-2005<br />${historicalHovertextLabel}: %{r:,} cf/s<extra></extra>`,
    })
    projectedTraces.push({
      r: projectedFlows,
      theta: projectedDates,
      type: 'scatterpolar',
      mode: 'markers',
      name: projectedTraceLabel,
      marker: {
        size: 8,
        color: projectedColor,
        symbol: 'square',
      },
      customdata: customdataProjected,
      hovertemplate: `%{customdata[0]}, 2046-2075<br />${projectedHovertextLabel}: %{r:,} cf/s<extra></extra>`,
    })
  })

  let traces = historicalTraces.concat(projectedTraces)
  const titleText = 'Minimum and maximum flow dates, cf/s'

  const layout = getLayout(titleText, '')

  let firstOfMonthValues = [
    1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335,
  ]

  firstOfMonthValues = firstOfMonthValues.map((doy: number) => {
    return convertTo360(doy)
  })

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
    },
    radialaxis: {
      range: [0, upperLimit],
      angle: 90,
      tickangle: 90,
    },
  }

  const config = getConfig('min-max-flow-dates')

  $Plotly.newPlot('min-max-flow-dates', traces, layout, config)
}
</script>

<template>
  <div id="min-max-flow-dates"></div>
</template>
