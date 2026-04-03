<script setup lang="ts">
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { isLoading, apiSlow, apiFailed } = storeToRefs(streamSegmentStore)
</script>
<template>
  <div v-if="isLoading" class="content is-size-4">
    <section class="section">
      <div class="container">
        <p v-if="apiSlow">
          This is taking longer than usual. Still trying&hellip;
        </p>
        <p v-else>
          Loading data&hellip; this usually takes about 10-15 seconds.
        </p>
        <progress class="progress" />
      </div>
    </section>
  </div>
  <div v-else-if="apiFailed" class="content is-size-4">
    <p>
      ⚠️ We&rsquo;re experiencing technical difficulties connecting to our
      servers and can&rsquo;t load any data at the moment. Hang tight and try
      again soon, or email us at
      <a href="mailto:uaf-snap-data-tools@alaska.edu"
        >uaf-snap-data-tools@alaska.edu</a
      >.
    </p>
  </div>
</template>
