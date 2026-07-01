<script setup lang="ts">
import { computed } from 'vue'
import { fnc } from '~/utils/general'

const julianDateStats = [
  'spr_ord',
  'sum_ord',
  'th1',
  'tl1',
  'wt_ann_max_temp_doy_mean',
  'wt_7d_max_temp_doy_mean',
]

const props = defineProps({
  future: {
    type: Number,
    required: true,
  },
  past: {
    type: Number,
    required: true,
  },
  statId: {
    type: String,
    required: false,
  },
})

// Assuming future and past are defined as props
const pct = computed(() => {
  if (props.past === 0) {
    if (props.future === 0) {
      return 0
    }
    return props.future > 0 ? 100 : -100
  }

  return Math.round(((props.future - props.past) / props.past) * 100)
})

// Julian date diffs should be the shortest distance around the date circle.
// Consider the example of January 1st (1) vs. December 31st (366).
// The raw difference is 365 days, but the actual difference in time is just 1 day.
// See: https://github.com/ua-snap/hydroviz/blob/main/data/preprocess/shp/modulo.md
// JavaScript requires an extra addition to handle negative values correctly.
const julianDateDiff = computed(() => {
  return ((((props.future - props.past + 183) % 366) + 366) % 366) - 183
})

// It doesn't make sense to calculate percentage change on circular diffs from
// Julian dates, so treat them differently and use absolute difference instead.
const diffMagnitude = computed(() => {
  if (props.statId && julianDateStats.includes(props.statId)) {
    return Math.abs(julianDateDiff.value)
  } else {
    return Math.abs(pct.value)
  }
})

const isWeak = computed(() => {
  return diffMagnitude.value < 25
})

const isStrong = computed(() => {
  return diffMagnitude.value > 50
})

const diff = computed(() => {
  let diff: number | string

  if (props.statId && julianDateStats.includes(props.statId)) {
    diff = julianDateDiff.value
  } else {
    diff = props.future - props.past
  }

  if (diff > 0) {
    diff = '&plus;' + fnc(diff)
  } else if (diff < 0) {
    diff = '&minus;' + fnc(Math.abs(diff))
  } else {
    diff = '0'
  }
  return diff
})
</script>

<template>
  <span
    class="diff number"
    :class="{
      weak: isWeak,
      strong: isStrong,
    }"
    v-html="diff"
  ></span>
</template>
<style lang="scss" scoped>
.diff {
  display: block;

  &.weak {
    font-weight: 300;
  }
  &.strong {
    font-weight: 500;
  }
}
</style>
