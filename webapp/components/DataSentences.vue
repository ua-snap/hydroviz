<script setup lang="ts">
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
</script>

<template>
  <div class="content is-size-5">
    <ul>
      <li>
        Historically, this stream has a mean annual flow of about
        {{ streamStats.summary.ma99_hist.value }} cfs. The mean annual flow is
        projected to
        {{ adjectiveForPercent(streamStats.summary.ma99_delta.value) }} ({{
          streamStats.summary.ma99_delta.value
        }}%) by mid-century.
      </li>
      <li>
        The maximum 1-day flow is projected to
        {{ adjectiveForPercent(streamStats.summary.dh1_delta.value) }} ({{
          streamStats.summary.dh1_delta.value
        }}%) and the minimum 1-day flow is projected to
        {{ adjectiveForPercent(streamStats.summary.dl1_delta.value) }} ({{
          streamStats.summary.dl1_delta.value
        }}%).
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
        }}
        .
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
    <p>
      Historical data uses the Maurer calibration, 1976–2005. Future projections
      use an model ensemble mean (13 models) for mid-century (2046–2075, with a
      middle-of-the-road emissions scenario (RCP 6.0).
    </p>
    <p>
      Note that models predict a large range of values for this variable.
      &#x26A0;&#xFE0F;
    </p>
  </div>
</template>

<style lang="scss" scoped></style>
