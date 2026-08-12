<script lang="ts" setup>
const { $config } = useNuxtApp()
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { segmentId, segmentRegion } = storeToRefs(streamSegmentStore)

const hydrologyPath = computed(() => {
  return segmentRegion.value === 'alaska'
    ? '/arctic_hydrology'
    : '/conus_hydrology'
})

const trackCsvDownload = (
  type: 'stats' | 'climatology' | 'wt_stats' | 'wt_climatology'
) => {
  window.trackUmamiEvent('csv-download', {
    type,
    segment: String(segmentId.value),
    region: segmentRegion.value ?? undefined,
  })
}
</script>

<template>
  <span
    >Download complete
    <a
      :href="
        $config.public.snapApiUrl +
        hydrologyPath +
        '/stats/' +
        segmentId +
        '?format=csv'
      "
      @click="trackCsvDownload('stats')"
      >modeled hydrologic statistics<span
        class="tag is-link is-light is-small ml-1"
        >CSV</span
      ></a
    ><template v-if="segmentRegion === 'alaska'"
      >,
      <a
        :href="
          $config.public.snapApiUrl +
          hydrologyPath +
          '/wt_stats/' +
          segmentId +
          '?format=csv'
        "
        @click="trackCsvDownload('wt_stats')"
        >modeled water temperature statistics<span
          class="tag is-link is-light is-small ml-1"
          >CSV</span
        ></a
      >, </template
    ><template v-if="segmentRegion === 'conus'"> or </template>
    <a
      :href="
        $config.public.snapApiUrl +
        hydrologyPath +
        '/modeled_climatology/' +
        segmentId +
        '?format=csv'
      "
      @click="trackCsvDownload('climatology')"
      >modeled daily streamflow climatologies<span
        class="tag is-link is-light is-small ml-1"
        >CSV</span
      ></a
    ><template v-if="segmentRegion === 'alaska'"
      >, or
      <a
        :href="
          $config.public.snapApiUrl +
          hydrologyPath +
          '/wt_modeled_climatology/' +
          segmentId +
          '?format=csv'
        "
        @click="trackCsvDownload('wt_climatology')"
        >modeled water temperature climatologies<span
          class="tag is-link is-light is-small ml-1"
          >CSV</span
        ></a
      ></template
    >
    for analysis in a spreadsheet.
  </span>
</template>

<style scoped>
.tag {
  position: relative;
  top: -2px;
}
</style>
