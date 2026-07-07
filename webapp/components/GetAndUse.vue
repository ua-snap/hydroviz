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
      <div class="content is-size-5">
        <h3 class="title is-3">Get &amp; use this data</h3>
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
        <div v-if="segmentRegion == 'conus'">
          <h4 class="title is-4">Academic citations</h4>

          <blockquote>
            LaFontaine, J.H., and Riley, J.W., 2023, Model Input and Output for
            Hydrologic Simulations for the Conterminous United States for
            Historical and Future Conditions Using the National Hydrologic Model
            Infrastructure (NHM) and the Coupled Model Intercomparison Project
            Phase 5 (CMIP5), 1950–2100: U.S. Geological Survey data release,
            <a href="https://doi.org/10.5066/P9EBKREQ"
              >https://doi.org/10.5066/P9EBKREQ</a
            >.
          </blockquote>

          <blockquote>
            Regan, R.S., Markstrom, S.L., Hay, L.E., Viger, R.J., Norton, P.A.,
            Driscoll, J.M., LaFontaine, J.H., 2018, Description of the National
            Hydrologic Model for use with the Precipitation–Runoff Modeling
            System (PRMS): U.S. Geological Survey Techniques and Methods, book
            6, chap B9, 38 p.,
            <a href="https://doi.org/10.3133/tm6B9"
              >https://doi.org/10.3133/tm6B9</a
            >.
          </blockquote>

          <blockquote>
            LaFontaine, J.H., Hay, L.E., and Riley, J.R., 2023, Application of
            the National Hydrologic Model Infrastructure with the
            Precipitation–Runoff Modeling System (NHM-PRMS), 1950–2010, Maurer
            Calibration: U.S. Geological Survey data release,
            <a href="https://doi.org/10.5066/P9CVHLMB"
              >https://doi.org/10.5066/P9CVHLMB</a
            >.
          </blockquote>

          <blockquote>
            U.S. Geological Survey, 2025, U.S. Geological Survey National Water
            Information System database, at
            <a href="https://doi.org/10.5066/F7P55KJN"
              >https://doi.org/10.5066/F7P55KJN</a
            >. Data download directly accessible at
            <a href="https://api.waterdata.usgs.gov/ogcapi/v0/collections/daily"
              >https://api.waterdata.usgs.gov/ogcapi/v0/collections/daily</a
            >.
          </blockquote>
        </div>
      </div>
    </div>
  </section>
</template>
