<script setup lang="ts">
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { appContext } = storeToRefs(streamSegmentStore)
</script>

<template>
  <div class="container block content is-size-5">
    <p>
      This tool lets you explore this dataset in two modes: the
      <strong>middle of the road</strong> shows the average across 13 climate
      model futures, and <strong>future extremes</strong> show the size of
      variation between the minimums and maximums for lower and higher emissions
      scenarios.
      <NuxtLink to="/about/data"
        >Read more about how these are defined</NuxtLink
      >
      and learn how to apply them in your work.
    </p>
    <p>
      The full dataset for this stream location may be downloaded as a CSV file,
      below, for further analysis.
    </p>
  </div>
  <div class="sticky-toggle block content is-size-5 py-3 container">
    Show
    <span class="control is-size-5">
      <label class="radio">
        <input type="radio" name="scenario" value="mid" v-model="appContext" />
        middle of the road
      </label>
      or
      <label class="radio">
        <input
          type="radio"
          name="scenario"
          value="extremes"
          v-model="appContext"
        />
        future extremes
      </label>
    </span>
    in charts and graphs below.
    <span>Value: {{ appContext }}</span>
  </div>
</template>

<style lang="scss">
.sticky-toggle {
  position: sticky;
  top: 0;
  background: white;
  z-index: 10000;
  border-bottom: 1px solid #eee;
}
</style>
