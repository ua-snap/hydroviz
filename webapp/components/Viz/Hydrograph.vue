<script setup lang="ts">
// import { lcs, models, scenarios, eras } from '~/types/modelsScenarios'
// import { statVars } from '~/types/statsVars'
import { watch, toRaw } from 'vue'
import { useStreamSegmentStore } from '~/stores/streamSegment'
import { getLayout, getConfig } from '~/utils/chart'
const { $Plotly, $_ } = useNuxtApp()
import type { Data } from 'plotly.js-dist-min'

const streamSegmentStore = useStreamSegmentStore()
let { streamHydrograph, segmentName, isLoading } =
  storeToRefs(streamSegmentStore)

// const lcInput = defineModel('lc', { default: 'dynamic' })
// const modelInput = defineModel('model', { default: 'CCSM4' })
// const scenarioInput = defineModel('scenario', { default: 'rcp60' })

// Round to significant digits.  Stub.
function roundTo(num, sig = 3) {
  return Number(num.toPrecision(sig))
}

// We want a data structure that we can feed into Plotly.
// Three traces:
// - min (floor) across all models
// - mean computed across all models
// - max (ceiling) across all models
// incoming hydrograph data should be an object whose keys are models,
// see the API documentation for structure details deeper than that.
function buildHydrographData(hydrographData) {
  // console.log(hydrographData)
  if (!hydrographData) {
    alert('not set')
    return
  }

  var mean = [],
    min = [],
    max = []

  var dayMin, dayMax, dayMean

  // old school for loop!
  for (let i = 0; i <= 365; i++) {
    // If true, initialize the day min/max/mean for this iteration
    let unset = true
    Object.keys(hydrographData).forEach(model => {
      if (unset) {
        dayMin = hydrographData[model]['historical']['1976-2005'][i]['doy_min']
        dayMax = hydrographData[model]['historical']['1976-2005'][i]['doy_max']
        dayMean =
          hydrographData[model]['historical']['1976-2005'][i]['doy_mean']

        unset = false
        return // continue
      } else {
        if (
          hydrographData[model]['historical']['1976-2005'][i]['doy_min'] <
          dayMin
        ) {
          dayMin =
            hydrographData[model]['historical']['1976-2005'][i]['doy_min']
        }
        if (
          hydrographData[model]['historical']['1976-2005'][i]['doy_max'] >
          dayMax
        ) {
          dayMax =
            hydrographData[model]['historical']['1976-2005'][i]['doy_max']
        }
        dayMean +=
          hydrographData[model]['historical']['1976-2005'][i]['doy_mean']
      }
    })

    min[i] = roundTo(dayMin)
    mean[i] = roundTo(dayMean / 14)
    max[i] = roundTo(dayMax)

    console.log(min[i], mean[i], max[i])
  }

  return [min, mean, max]
}

const doyToDateString = (doy: number) => {
  const year = 2025 // Can be any year, but not a leap year.
  const date = new Date(year, 0) // January 1st of the given year
  date.setDate(doy) // Add DOY as days offset
  const options: Intl.DateTimeFormatOptions = { month: 'short', day: 'numeric' }
  return date.toLocaleDateString('en-US', options)
}

const doys = $_.range(1, 365 + 1)
const dataLabels = doys.map((doy: number) => {
  return doyToDateString(doy)
})

// hg is assumed to be non-null, raw, and only dynamic land cover now.
const buildChart = hg => {
  let traces: Data[] = []
  let flowData = buildHydrographData(hg)

  let doys = $_.range(1, 365 + 1)

  let traceConfig = [
    {
      label: 'Minimum flow',
      doy: doys,
    },
    {
      label: 'Mean flow',
      doy: doys,
    },
    {
      label: 'Maximum flow',
      doy: doys,
    },
  ]

  flowData.forEach((traceData, index) => {
    traces.push({
      x: doys,
      y: traceData,
      mode: 'lines',
      line: { shape: 'spline', smoothing: 2 },
      name: traceConfig[index].label,
    })
  })

  const yAxisLabel = 'Daily flow rate (cfm)'

  // These numbers correspond to the 1st of each month in a 366-day year.
  let xTickVals = [1, 32, 59, 90, 121, 152, 182, 213, 244, 274, 305, 335]
  let xTickLabels = xTickVals.map((doy: number) => {
    return doyToDateString(doy)
  })

  const chartTitle = 'Hydrograph'

  const titleText: string =
    'Minimum, mean and maximum flow rate across 13 models'

  const layout = getLayout(titleText, yAxisLabel, {
    tickangle: 45,
  })

  layout.xaxis = {
    tickmode: 'array',
    tickvals: xTickVals,
    ticktext: xTickLabels,
  }

  layout.yaxis = {
    type: 'log',
    autorange: true,
  }

  const config = getConfig(chartTitle)

  $Plotly.newPlot('hydrograph', traces, layout, config)
}

watch(streamHydrograph, hg => {
  // Is briefly null when switching places
  if (hg.data) {
    buildChart(toRaw(hg.data.dynamic))
  }
})
</script>

<template>
  <section class="section">
    <div class="container">
      <div v-if="isLoading == true" class="loading content is-size-4">
        <p>Loading data&hellip; this can take a minute or two.</p>
        <progress class="progress" />
      </div>
      <div v-show="!isLoading && streamHydrograph">
        <h3
          class="title is-3 is-flex is-justify-content-center is-align-items-center mt-6 mb-5"
        >
          Hydrograph for {{ segmentName }}
        </h3>
        <div id="hydrograph"></div>
      </div>
    </div>
  </section>
</template>

<style lang="scss" scoped></style>
