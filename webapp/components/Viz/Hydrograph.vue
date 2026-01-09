<script setup lang="ts">
// import { lcs, models, scenarios, eras } from '~/types/modelsScenarios'
// import { statVars } from '~/types/statsVars'
import { watch, toRaw } from 'vue'
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { streamHydrograph, segmentName, isLoading } =
  storeToRefs(streamSegmentStore)

// const lcInput = defineModel('lc', { default: 'dynamic' })
// const modelInput = defineModel('model', { default: 'CCSM4' })
// const scenarioInput = defineModel('scenario', { default: 'rcp60' })

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
    console.log(dayMin, dayMax, dayMean)

    min[i] = dayMin
    mean[i] = dayMean / 14
    max[i] = dayMax
  }
  console.log(min, mean, max)
  return { min, mean, max }
}

watch(streamHydrograph, hg => {
  buildHydrographData(toRaw(hg.data.dynamic))
})
</script>

<template>
  <section class="section">
    <div class="container">
      <div v-if="isLoading == true" class="loading content is-size-4">
        <p>Loading data&hellip; this can take a minute or two.</p>
        <progress class="progress" />
      </div>
      <div v-if="!isLoading && streamHydrograph">
        <h3
          class="title is-3 is-flex is-justify-content-center is-align-items-center mt-6 mb-5"
        >
          Hydrograph for {{ segmentName }}
        </h3>
      </div>
    </div>
  </section>
</template>

<style lang="scss" scoped></style>
