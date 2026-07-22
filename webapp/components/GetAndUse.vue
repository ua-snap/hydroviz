<script setup lang="ts">
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { segmentId, segmentRegion } = storeToRefs(streamSegmentStore)

const { $config } = useNuxtApp()

const hydrologyPath = computed(() =>
  segmentRegion.value === 'alaska' ? '/arctic_hydrology' : '/conus_hydrology'
)

const hydrologyUrl = computed(
  () => `${$config.public.snapApiUrl}${hydrologyPath.value}`
)

const trackApiClick = () => {
  window.trackUmamiEvent('api-link-click', {
    segment: String(segmentId.value),
    region: segmentRegion.value ?? undefined,
  })
}

// Track when the user has scrolled far enough to bring this section (the last
// one on the report page) into view. Fires at most once per report.
const sectionEl = ref<HTMLElement | null>(null)
let observer: IntersectionObserver | null = null

onMounted(() => {
  if (!sectionEl.value || !('IntersectionObserver' in window)) return
  observer = new IntersectionObserver(
    entries => {
      if (entries.some(entry => entry.isIntersecting)) {
        window.trackUmamiEvent('get-and-use-reached', {
          segment: String(segmentId.value),
          region: segmentRegion.value ?? undefined,
        })
        observer?.disconnect()
        observer = null
      }
    },
    // A tall section may never reach high visibility ratios, so fire once a
    // small fraction of it is on screen.
    { threshold: 0.1 }
  )
  observer.observe(sectionEl.value)
})

onUnmounted(() => {
  observer?.disconnect()
  observer = null
})
</script>

<template>
  <section class="section" id="get-and-use" ref="sectionEl">
    <div class="container">
      <h3 class="title is-3">Get &amp; use this data</h3>
      <div class="content is-size-5 clamp">
        <ul>
          <li><CsvDownload /></li>
          <li>
            <a :href="hydrologyUrl" @click="trackApiClick"
              >Access this data programmatically</a
            >
            with downloads ready for R and Python analysis.
          </li>
          <li v-if="segmentRegion == 'conus'">
            <a
              href="https://www.sciencebase.gov/catalog/item/6373bd3bd34ed907bf6c6e25"
              >Access the source datasets</a
            >
            used in this application, including references to academic papers
            about the dataset.
          </li>
          <li v-if="segmentRegion == 'conus'">
            Read a
            <a href="https://pubs.usgs.gov/publication/tm6B9"
              >description of the National Hydrologic Model for use with the
              Precipitation-Runoff Modeling System</a
            >
            (PRMS)
          </li>
        </ul>
        <CitationsConus v-if="segmentRegion == 'conus'" />
        <CitationsAlaska v-if="segmentRegion == 'alaska'" />
      </div>
    </div>
  </section>
</template>
