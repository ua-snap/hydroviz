<script setup lang="ts">
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { appContext, appEra } = storeToRefs(streamSegmentStore)
</script>

<template>
  <div class="container block content is-size-5">
    <p>
      This tool lets you explore this dataset in two modes: the
      <strong>middle of the road</strong> shows the averages for a
      middle-of-the-road climate future, and
      <strong>future extremes</strong> show the size of variation between the
      minimums and maximums for lower and higher emissions scenarios.
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
    <p>
      Show
      <span class="control is-size-5">
        <label class="radio">
          <input
            type="radio"
            name="scenario"
            value="mid"
            v-model="appContext"
          />
          <span>middle of the road</span>
        </label>
        or
        <label class="radio">
          <input
            type="radio"
            name="scenario"
            value="extremes"
            v-model="appContext"
          />
          <span>future extremes</span>
        </label>
      </span>
      in charts and graphs below.
    </p>
    <p style="margin-top: -1rem">
      Show projected data for
      <span class="control is-size-5">
        <label class="radio">
          <input type="radio" name="era" value="2016-2045" v-model="appEra" />
          <span>early-century</span> (2016&ndash;2045),</label
        >
        <label class="radio">
          <input type="radio" name="era" value="2046-2075" v-model="appEra" />
          <span>mid-century</span> (2046&ndash;2075)</label
        >
        or
        <label class="radio">
          <input type="radio" name="era" value="2071-2100" v-model="appEra" />
          <span>late-century</span> (2071&ndash;2100).</label
        >
      </span>
    </p>
  </div>
</template>

<style lang="scss" scoped>
.sticky-toggle {
  position: sticky;
  top: 0;
  background: white;
  z-index: 10000;
  border-bottom: 1px solid #eee;
}

label.radio {
  display: inline-block;
  margin-left: 0.5rem;
  margin-right: 0.5rem;
  span {
    font-weight: 500;
    display: inline-block;
    margin-left: 0.4rem;
    border-bottom: 2px solid #ccc;
  }
}
</style>
