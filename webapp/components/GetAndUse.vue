<script setup lang="ts">
const { $config } = useNuxtApp()
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { segmentId } = storeToRefs(streamSegmentStore)
const props = defineProps({
  streamId: {
    type: Number,
    required: true,
  },
})
</script>

<template>
  <section class="section">
    <div class="container">
      <div class="content is-size-5">
        <h3 class="title is-3">Get &amp; use this data</h3>
        <ul>
          <li><CsvDownload /></li>
          <li>
            <a :href="$config.public.snapApiUrl + '/conus_hydrology'"
              >Access this data programmatically</a
            >
            with downloads ready for R and Python analysis.
          </li>
          <li>
            <a
              href="https://www.sciencebase.gov/catalog/item/6373bd3bd34ed907bf6c6e25"
              >Access the source datasets</a
            >
            used in this application, including references to academic papers
            about the dataset.
          </li>
          <li>
            Read a
            <a href="https://pubs.usgs.gov/publication/tm6B9"
              >description of the National Hydrologic Model for use with the
              Precipitation-Runoff Modeling System</a
            >
            (PRMS)
          </li>
        </ul>
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
          Hydrologic Model for use with the Precipitation–Runoff Modeling System
          (PRMS): U.S. Geological Survey Techniques and Methods, book 6, chap
          B9, 38 p.,
          <a href="https://doi.org/10.3133/tm6B9"
            >https://doi.org/10.3133/tm6B9</a
          >.
        </blockquote>

        <blockquote>
          LaFontaine, J.H., Hay, L.E., and Riley, J.R., 2023, Application of the
          National Hydrologic Model Infrastructure with the Precipitation–Runoff
          Modeling System (NHM-PRMS), 1950–2010, Maurer Calibration: U.S.
          Geological Survey data release,
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
  </section>
</template>
