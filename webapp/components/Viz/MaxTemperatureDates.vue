<script setup lang="ts">
import { watch, toRaw } from 'vue'
import {
  getLayout,
  getConfig,
  initializeChart,
  getDataRange,
  convertTo360,
} from '~/utils/chart'
const { $Plotly, $_ } = useNuxtApp()
import type { Data } from 'plotly.js'

import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
const { segmentId, gaugeId, appContext, appEra } =
  storeToRefs(streamSegmentStore)

const props = defineProps(['streamMaxTempDates'])

onMounted(() => {
  initializeChart(
    $Plotly,
    'max-temperature-dates',
    buildChart,
    toRaw(props.streamMaxTempDates)
  )
})

watch([appContext, appEra], () => {
  initializeChart(
    $Plotly,
    'max-temperature-dates',
    buildChart,
    toRaw(props.streamMaxTempDates)
  )
})

const buildChart = () => {
  let historicalTraces: Data[] = []
  let projectedTraces: Data[] = []

  let scenarioColors = {
    historical: '#333333',
    projected: '#32cd32',
  }

  let scenarioSymbols = {
    historical: 'diamond',
    projected: 'circle',
  }

  let gaugeIdLine = gaugeId.value
    ? `<br><span style="font-size: 0.8em;">Gage ID: ${gaugeId.value}</span>`
    : ''
  let titleText = `Modeled water temperature at date of annual maximum, 2034-2065${gaugeIdLine}`

  let historicalTemp = [props.streamMaxTempDates['historical']['temperature']]
  let historicalTempDate = [props.streamMaxTempDates['historical']['date']]

  historicalTempDate.forEach((doy: number, index: number) => {
    historicalTempDate[index] = convertTo360(doy)
  })

  const historicalTraceLabel = 'Historical, 1990-2021'

  let historicalTrace = {
    r: historicalTemp,
    theta: historicalTempDate,
    type: 'scatterpolar',
    mode: 'markers',
    name: historicalTraceLabel,
    marker: {
      size: 9,
      color: scenarioColors['historical'],
      symbol: scenarioSymbols['historical'],
    },
  }

  historicalTraces.push(historicalTrace)

  let projectedTemps =
    props.streamMaxTempDates['projected']['2034-2065']['temperature']
  let projectedDates = $_.cloneDeep(
    props.streamMaxTempDates['projected']['2034-2065']['date']
  )

  projectedDates.forEach((doy: number, index: number) => {
    projectedDates[index] = convertTo360(doy)
  })

  let traceLabel = 'Projected'

  let scenarioColor = scenarioColors['projected']
  let scenarioSymbol = scenarioSymbols['projected']

  let trace = {
    r: projectedTemps,
    theta: projectedDates,
    type: 'scatterpolar',
    mode: 'markers',
    name: traceLabel,
    marker: {
      size: 8,
      color: scenarioColor,
      symbol: scenarioSymbol,
    },
  }

  trace['subplot'] = 'polar'

  projectedTraces.push(trace)

  // Reverse projected traces because the legend gets reversed later.
  // This will ultimately keep the legend order the same as the subplot order.
  projectedTraces.reverse()

  let traces = projectedTraces.concat(historicalTraces)

  let legendConfig = {
    orientation: 'h',
    yanchor: 'top',
    y: -0.15,
    xanchor: 'center',
    x: 0.5,
    traceorder: 'reversed',
  }

  let isTwoLineTitle = gaugeId.value ? true : false
  const isAlaskaData = true

  const layout = getLayout(
    'maxTempDates',
    titleText,
    '',
    {},
    {},
    legendConfig,
    isTwoLineTitle,
    isAlaskaData
  )

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

  let keysToExclude = ['date']
  let { yMin, yMax } = getDataRange(props.streamMaxTempDates, keysToExclude)

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
      ticksuffix: ' °C',
      tickmode: 'auto',
      nticks: 4,
      gridcolor: axisColor,
      range: [yMin, yMax],
    },
    domain: firstPlotDomain,
  }

  let pngName = `max-temperature-dates_${segmentId.value}_2034-2065`
  let config = getConfig(pngName)

  $Plotly.newPlot('max-temperature-dates', traces, layout, config)
}
</script>

<template>
  <div id="max-temperature-dates" class="mb-5"></div>
</template>
