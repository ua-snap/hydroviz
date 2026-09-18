<script setup lang="ts">
import { watch, toRaw } from 'vue'
import {
  getLayout,
  getConfig,
  initializeChart,
  getDataRange,
  convertTo360,
  getGageIdLine,
  TEMPERATURE_START_DOY,
  TEMPERATURE_END_DOY,
} from '~/utils/chart'
const { $Plotly, $_ } = useNuxtApp()
import type { Data } from 'plotly.js'
import { scenarioFullNames } from '~/types/modelsScenarios'

import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
const { segmentId, gageId, appContext, appEra } =
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

  let gageIdLine = getGageIdLine(gageId.value)
  let titleText = `Modeled water temperature at date of annual maximum, 2034-2065<br>${scenarioFullNames['ssp370']}${gageIdLine}`

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

  let traceLabel = `Projected, ${scenarioFullNames['ssp370']}`

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

  const isAlaskaData = true

  const layout = getLayout(
    'maxTempDates',
    titleText,
    '',
    {},
    {},
    legendConfig,
    isAlaskaData
  )

  // Only label the months inside the displayed May 1 - Sept 30 window.
  const monthStarts = [
    { doy: 1, label: 'Jan' },
    { doy: 32, label: 'Feb' },
    { doy: 60, label: 'Mar' },
    { doy: 91, label: 'Apr' },
    { doy: 121, label: 'May' },
    { doy: 152, label: 'Jun' },
    { doy: 182, label: 'Jul' },
    { doy: 213, label: 'Aug' },
    { doy: 244, label: 'Sep' },
    { doy: 274, label: 'Oct' },
    { doy: 305, label: 'Nov' },
    { doy: 335, label: 'Dec' },
  ].filter(
    ({ doy }) => doy >= TEMPERATURE_START_DOY && doy <= TEMPERATURE_END_DOY
  )

  const firstOfMonthValues = monthStarts.map(({ doy }) => convertTo360(doy))

  // Plotly measures `sector` counterclockwise from due East, while this axis
  // runs clockwise from due North, so a data angle maps to 90 - angle.
  const sectorEnd = 90 - convertTo360(TEMPERATURE_START_DOY) // May 1 edge
  const sectorStart = 90 - convertTo360(TEMPERATURE_END_DOY) // Sept 30 edge
  const sector = [sectorStart, sectorEnd]

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
      ticktext: monthStarts.map(({ label }) => label),
      direction: 'clockwise',
      gridcolor: axisColor,
    },
    radialaxis: {
      // Ride the May 1 edge of the sector. Due north (the full-circle default)
      // now sits outside the sector, which drops the tick labels and leaves the
      // axis line crossing the title.
      angle: sectorEnd,
      // Polar tick angles are relative to the axis, so matching it keeps the
      // labels horizontal, as on the max flow dates chart.
      tickangle: sectorEnd,
      ticksuffix: ' °C',
      tickmode: 'auto',
      nticks: 4,
      gridcolor: axisColor,
      range: [yMin, yMax],
    },
    domain: firstPlotDomain,
    sector: sector,
  }

  let pngName = `max-temperature-dates_${segmentId.value}_2034-2065`
  let config = getConfig(pngName)

  $Plotly.newPlot('max-temperature-dates', traces, layout, config)
}
</script>

<template>
  <div id="max-temperature-dates" class="mb-5"></div>
</template>
