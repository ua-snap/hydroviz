<script setup lang="ts">
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { streamStats, streamHydrograph } = storeToRefs(streamSegmentStore)
</script>

<template>
  <section class="section">
    <div class="container">
      <Loading />
    </div>
  </section>

  <div v-if="streamStats">
    <section class="section">
      <div class="container">
        <h3 class="title is-3">
          Statistics for {{ streamStats.name }}
          <span class="segmentId">ID{{ streamStats.id }}</span>
        </h3>
        <div class="content is-size-5">
          Introduction to the report goes here. We can pull some summarized info
          about the specific stream segment in order to highlight aspects of
          uncertainty and some succinct characterization of net change over
          time.
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <DataSentences />
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h4 class="title is-4">Hydrograph</h4>
        <VizHydrograph :stream-hydrograph="streamHydrograph" />
      </div>
    </section>
    <section class="section">
      <div class="container">
        <h4 class="title is-4">Magnitude statistics</h4>
        <VizMonthlyFlow :stream-stats="streamStats" />
        <StatsTable :stream-stats="streamStats" category="magnitude" />
      </div>
    </section>
    <section class="section">
      <div class="container">
        <h4 class="title is-4">Frequency statistics</h4>
        <StatsTable :stream-stats="streamStats" category="frequency" />
      </div>
    </section>
    <section class="section">
      <div class="container">
        <h4 class="title is-4">Duration statistics</h4>
        <StatsTable :stream-stats="streamStats" category="duration" />
      </div>
    </section>
    <section class="section">
      <div class="container">
        <h4 class="title is-4">Timing statistics</h4>
        <StatsTable :stream-stats="streamStats" category="timing" />
      </div>
    </section>
    <section class="section">
      <div class="container">
        <h4 class="title is-4">Rate of change statistics</h4>
        <StatsTable :stream-stats="streamStats" category="rate_of_change" />
      </div>
    </section>
  </div>
</template>

<style lang="scss" scoped></style>
