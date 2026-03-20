<script setup lang="ts">
import { toRaw } from 'vue'
import lowess from '@stdlib/stats-lowess'
import { getLayout, getConfig, initializeChart } from '~/utils/chart'
const { $Plotly, $_ } = useNuxtApp()
import type { Data } from 'plotly.js'

const props = defineProps(['streamHydrograph'])

onMounted(() => {
  initializeChart(
    $Plotly,
    'hydrograph',
    buildChart,
    toRaw(props.streamHydrograph)
  )
})

watch(props.streamHydrograph, newValue => {
  initializeChart($Plotly, 'hydrograph', buildChart, toRaw(newValue))
})

// Round to significant digits.  Stub.
function roundTo(num, sig = 3) {
  return Number(num.toPrecision(sig))
}

const doyToDateString = (doy: number) => {
  const year = 2025 // Can be any year, but not a leap year.
  const date = new Date(year, 0) // January 1st of the given year
  date.setDate(doy) // Add DOY as days offset
  const options: Intl.DateTimeFormatOptions = { month: 'short', day: 'numeric' }
  return date.toLocaleDateString('en-US', options)
}

// Shift a DOY-indexed dataset to hydro year (Oct 1 - Sept 30)
function convertDoysToHydroYearDoys(series) {
  let octDec = series.slice(273) // through end of array (366)
  let janSept = series.slice(0, 273)
  let joined = octDec.concat(janSept)
  return octDec.concat(janSept)
}
const doys = $_.range(1, 366 + 1)
const hydroDoys = convertDoysToHydroYearDoys(doys)

// Converts & LOWESS smooths a timeseries of Y values
// Need to trick it so there's not discontinuity between day 366/1.
function processLowessAndHydroYear(traceData) {
  let hydroYearTraceData = convertDoysToHydroYearDoys(traceData)

  // Bit tricky: we index the day-of-year as 1...366 for the x-axis
  // for the purpose of the lowess calculation, but the y-values represent
  // the hydro-year shifted values.  This gives us the correct, smooth
  // chart form.
  let smoothed = lowess(doys, hydroYearTraceData, {
    f: 0.05,
    sorted: true,
  })
  let hydroOrderedSmoothedY = smoothed.y.map((cfm: number) => {
    return roundTo(cfm)
  })
  return hydroOrderedSmoothedY
}

// hg is assumed to be non-null, raw, and only dynamic land cover now.
const buildChart = hg => {
  let traces: Data[] = []

  // Create historical trace
  let historicalFlowData = hg['historical']

  let hydroYearHistoricalDataMin = processLowessAndHydroYear(
    historicalFlowData['doy_min']
  )
  let hydroYearHistoricalDataMean = processLowessAndHydroYear(
    historicalFlowData['doy_mean']
  )
  let hydroYearHistoricalDataMax = processLowessAndHydroYear(
    historicalFlowData['doy_max']
  )

  traces.push({
    x: hydroDoys,
    y: hydroYearHistoricalDataMin,
    type: 'scatter',
    mode: 'line',
    line: { color: '#aaaaaa', width: 0 },
    name: 'Historical Minimum (Modeled), 1976-2005',
  })

  traces.push({
    x: hydroDoys,
    y: hydroYearHistoricalDataMax,
    type: 'scatter',
    fill: 'tonexty',
    mode: 'none',
    fillcolor: 'rgba(190,190,190,0.5)',
    name: 'Historical Maximum (Modeled), 1976-2005',
  })

  traces.push({
    x: hydroDoys,
    y: hydroYearHistoricalDataMean,
    type: 'scatter',
    mode: 'line',
    line: { color: '#FFFFFF', width: 3 },
    name: 'Historical Mean (Modeled), 1976-2005',
  })

  // There's a gotcha here: two scenarios (ACCESS1-0, BNU-ESM) don't have RCP 2.6 or 6.0.
  // Historical needs to have been removed.
  let projectedFlowData = hg['projected']

  let traceConfig = {
    doy_min: {
      label: 'Minimum modeled future flow',
      color: '#6baed6',
    },
    doy_mean: {
      label: 'Mean modeled future flow',
      color: '#3182bd',
    },
    doy_max: {
      label: 'Maximum modeled future flow',
      color: '#08519c',
    },
  }

  Object.keys(traceConfig).forEach(key => {
    let traceData = projectedFlowData[key]
    let hydroOrderedSmoothedY = processLowessAndHydroYear(traceData)
    traces.push({
      x: hydroDoys,
      y: hydroOrderedSmoothedY,
      type: 'scatter',
      mode: 'lines',
      line: { shape: 'spline', color: traceConfig[key].color },
      name: traceConfig[key].label,
    })
  })

  // These numbers correspond to the 1st of each month in a 366-day year,
  // oriented by the hydro year.
  let xTickVals = [274, 305, 335, 1, 32, 60, 91, 121, 152, 182, 213, 244]
  let xTickLabels = xTickVals.map((doy: number) => {
    return doyToDateString(doy)
  })

  const titleText: string =
    'Minimum, mean and maximum modeled projected flow rate'

  const layout = getLayout(
    titleText,
    'Flow rate, cf/s',
    {
      type: 'category',
      tickmode: 'array',
      tickvals: xTickVals,
      ticktext: xTickLabels,
    },
    {
      type: 'log',
      autorange: true,
    }
  )
  const config = getConfig()

  $Plotly.newPlot('hydrograph', traces, layout, config)
}
</script>

<template>
  <div id="hydrograph"></div>
</template>

<style lang="scss" scoped></style>
