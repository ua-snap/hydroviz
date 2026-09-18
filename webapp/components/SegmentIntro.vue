<script setup lang="ts">
import { computed } from 'vue'
import { huc8s } from '~/assets/huc8names'

import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { segmentUsgsGageId, segmentHuc8Id, segmentIsHuc8Outlet, segmentRegion } =
  storeToRefs(streamSegmentStore)

const USGS_STREAM_GAGE_URL_BASE =
  'https://waterdata.usgs.gov/monitoring-location/'
</script>
<template>
  <div class="content clamp is-size-5">
    <aside v-if="segmentRegion === 'alaska'" class="region-note">
      <h4 class="region-note-title">Alaska &amp; Northwestern Canada data</h4>
      <p>
        The streamflow and river-temperature projections presented here were
        developed by the NSF-funded
        <a
          href="https://www.colorado.edu/research/arctic-rivers/"
          rel="external"
          >Arctic Rivers Project</a
        >, which combined a high-resolution (4-km) regional climate model with
        river-routing and river-temperature models to simulate historical and
        potential midcentury river conditions across Alaska and northwestern
        Canada. The modeling and data products were developed through a
        collaborative process designed to improve their relevance and usability
        for communities and decision makers.
      </p>
      <dl class="region-note-refs">
        <dt>Learn more</dt>
        <dd>
          Newman et al. (2026),
          <cite>Bulletin of the American Meteorological Society</cite>,
          <a href="https://doi.org/10.1175/BAMS-D-24-0131.1" rel="external"
            >DOI: 10.1175/BAMS-D-24-0131.1</a
          >
        </dd>
        <dt>Data</dt>
        <dd>
          Blaskey et al. (2024),
          <cite
            >Alaskan river discharge, temperature, and climate data for a
            climate reference (1990&ndash;2021) and at mid-century
            (2034&ndash;2065)</cite
          >, NSF Arctic Data Center,
          <a href="https://doi.org/10.18739/A25M62870" rel="external"
            >DOI: 10.18739/A25M62870</a
          >
        </dd>
      </dl>
    </aside>
    <p>
      This stream segment is
      <span v-if="segmentIsHuc8Outlet">an outflow segment for</span
      ><span v-else>located in</span> the
      <span>{{ huc8s[segmentHuc8Id] }} watershed</span>
      (HUC-8 {{ segmentHuc8Id }}).
    </p>
    <p v-if="segmentUsgsGageId">
      This stream segment has a corresponding USGS stream gage,
      {{ segmentUsgsGageId }}.
      <a rel="external" :href="USGS_STREAM_GAGE_URL_BASE + segmentUsgsGageId"
        >Go to the web page for that gage</a
      >.
    </p>
    <p>
      This tool integrates some of the best available datasets at a broad
      spatial scale, but understanding model uncertainty and the characteristics
      of the data in the context of your area of study is
      important&mdash;<NuxtLink to="/how-to">read more.</NuxtLink>
    </p>

    <p>
      All data in this report can be downloaded in CSV and other formats
      <NuxtLink to="#get-and-use">at the bottom of this page</NuxtLink>.
    </p>
  </div>
</template>

<style lang="scss" scoped>
// Supplementary provenance note. It inherits the surrounding
// .content.is-size-5 sizing, measure and text color; the rule and the eyebrow
// heading set it apart, not smaller or lighter type.
.region-note {
  margin-bottom: 2rem;
  padding: 0.75rem 0 0.75rem 1.25rem;
  border-left: 4px solid var(--bulma-grey-light);

  p {
    margin-bottom: 0.75rem;
  }
}

.region-note-title {
  font-size: 1.2rem !important;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--bulma-text-strong);
  margin-bottom: 0.5rem !important;
}

.region-note-refs {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.25rem 0.75rem;
  margin: 0;

  dt {
    font-weight: 600;
    white-space: nowrap;
  }

  dd {
    margin: 0;
  }

  cite {
    font-style: italic;
  }
}

// Stack the label above its citation where a two-column grid would crowd.
@media screen and (max-width: 48rem) {
  .region-note-refs {
    grid-template-columns: 1fr;
    gap: 0.15rem;

    dd {
      margin-bottom: 0.75rem;
    }
  }
}
</style>
