<script setup lang="ts">
import { computed } from 'vue'
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { streamStats, segmentName } = storeToRefs(streamSegmentStore)

function adjectiveForPercent(value) {
  if (value < -50) {
    return 'dramatically decrease'
  } else if (value >= -50 && value < -30) {
    return 'substantially decrease'
  } else if (value >= -30 && value < -10) {
    return 'moderately decrease'
  } else if (value >= -10 && value < 0) {
    return 'slightly decrease or stay the same'
  } else if (value >= 0 && value < 20) {
    return 'slightly increase or stay the same'
  } else if (value >= 20 && value < 60) {
    return 'moderately increase'
  } else if (value >= 60 && value < 100) {
    return 'substantially increase'
  } else if (value >= 100) {
    return 'dramatically increase'
  }
}

// Returns 's' or '' depending on value
function ifPlural(value) {
  value = Math.abs(value)
  if (value == 1) {
    return ''
  }
  return 's'
}

// Type = 'event' or 'day'
function blurbFromEventCountOrDuration(count, type) {
  let blurb = ''
  if (count < 0) {
    blurb +=
      'decrease by ' +
      Math.abs(count) +
      ' ' +
      type +
      ifPlural(count) +
      ' per year'
  } else if (count == 0) {
    blurb += 'stay about the same (' + count + ' ' + type + 's per year)'
  } else if (count > 0) {
    blurb +=
      'increase by ' +
      Math.abs(count) +
      ' ' +
      type +
      ifPlural(count) +
      ' per year'
  }
  return blurb
}

// Whether we think there is strong model disagreement for a min/max range
const isMeanAnnualFlowHighlyVariable = computed(() => {
  return (
    Math.abs(
      streamStats.value.summary.ma99_delta.range_high -
        streamStats.value.summary.ma99_delta.range_low
    ) > 50
  )
})

const isMax1DayFlowHighlyVariable = computed(() => {
  return (
    Math.abs(
      streamStats.value.summary.dh1_delta.range_high -
        streamStats.value.summary.dh1_delta.range_low
    ) > 50 ||
    Math.abs(
      streamStats.value.summary.dl1_delta.range_high -
        streamStats.value.summary.dl1_delta.range_low
    ) > 50
  )
})

const lowFlow = computed(() => {
  return streamStats.value.summary.ma99_hist.value <= 5
})

function orMoreIf100Percent(amount) {
  if (amount >= 100) {
    return 'or more'
  }
  return ''
}
</script>

<template>
  <div class="content is-size-5">
    <p v-if="lowFlow">
      <strong>Note: this stream segment has a low mean annual flow.</strong>
      Headwaters and other small or intermittent streams have high statistical
      variability.
    </p>
    <ul>
      <li>
        Historically, this stream has a mean annual flow of about
        {{ streamStats.summary.ma99_hist.value }} cfs. The mean annual flow is
        projected to
        {{ adjectiveForPercent(streamStats.summary.ma99_delta.value) }} ({{
          streamStats.summary.ma99_delta.value
        }}% {{ orMoreIf100Percent(streamStats.summary.ma99_delta.value) }}) by
        mid-century.
        <span v-if="isMeanAnnualFlowHighlyVariable">&#x26A0;&#xFE0F;</span>
      </li>
      <li>
        The maximum 1-day flow is projected to
        {{ adjectiveForPercent(streamStats.summary.dh1_delta.value) }} ({{
          streamStats.summary.dh1_delta.value
        }}% {{ orMoreIf100Percent(streamStats.summary.dh1_delta.value) }}) and
        the minimum 1-day flow is projected to
        {{ adjectiveForPercent(streamStats.summary.dl1_delta.value) }} ({{
          streamStats.summary.dl1_delta.value
        }}% {{ orMoreIf100Percent(streamStats.summary.dl1_delta.value) }}).
        <span v-if="isMax1DayFlowHighlyVariable">&#x26A0;&#xFE0F;</span>
      </li>
      <li>
        The mean number of high flow events is projected to
        {{
          blurbFromEventCountOrDuration(
            streamStats.summary.fh1_delta.value,
            'event'
          )
        }}, and the mean duration of high flow events is projected to
        {{
          blurbFromEventCountOrDuration(
            streamStats.summary.dh15_delta.value,
            'day'
          )
        }}.
      </li>
      <li>
        The mean number of low flow events is projected to
        {{
          blurbFromEventCountOrDuration(
            streamStats.summary.fl1_delta.value,
            'event'
          )
        }}, and the mean duration of low flow events is projected to
        {{
          blurbFromEventCountOrDuration(
            streamStats.summary.dl16_delta.value,
            'day'
          )
        }}.
      </li>
    </ul>
    <p v-if="isMeanAnnualFlowHighlyVariable || isMax1DayFlowHighlyVariable">
      <span class="warn">&#x26A0;&#xFE0F;</span> Models outputs vary by 50% or
      more for these variables.
    </p>
    <p>
      Historical data uses the Maurer calibration, 1976&ndash;2005. Future
      projections for mid-century (2046&ndash;2075) use the mean of 13 global
      circulation models and a middle-of-the-road emissions scenario (RCP 6.0).
    </p>
  </div>
</template>

<style lang="scss" scoped></style>
