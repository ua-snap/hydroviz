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
    >Download
    <a
      :href="
        $config.public.snapApiUrl +
        hydrologyPath +
        '/stats/' +
        segmentId +
        '?format=csv'
      "
      @click="trackCsvDownload('stats')"
      >complete modeled hydrologic statistics</a
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
        >water temperature statistics</a
      ></template
    >
    or
    <a
      :href="
        $config.public.snapApiUrl +
        hydrologyPath +
        '/modeled_climatology/' +
        segmentId +
        '?format=csv'
      "
      @click="trackCsvDownload('climatology')"
      >modeled daily streamflow climatologies</a
    ><template v-if="segmentRegion === 'alaska'"
      >,
      <a
        :href="
          $config.public.snapApiUrl +
          hydrologyPath +
          '/wt_climatology/' +
          segmentId +
          '?format=csv'
        "
        @click="trackCsvDownload('wt_climatology')"
        >water temperature climatologies</a
      ></template
    >
    in CSV format for analysis in a spreadsheet.</span
  >
</template>
