<script setup lang="ts">
import { computed } from 'vue'
import { roundSigFig, fnc } from '~/utils/general'
const { $_ } = useNuxtApp()

const props = defineProps({
  future: {
    type: Number,
    required: true,
  },
  past: {
    type: Number,
    required: true,
  },
})

// Assuming future and past are defined as props
const pct = computed(() => {
  return (((props.future - props.past) / props.past) * 100).toFixed(0)
})

// True if the difference is less than 10%, or 10mm
const isWeak = computed(() => {
  return Math.abs(pct.value) < 25
})

const isStrong = computed(() => {
  return Math.abs(pct.value) > 50
})

const isLess = computed(() => {
  return pct.value < 0
})

const isMore = computed(() => {
  return pct.value > 0
})

const diff = computed(() => {
  let diff = props.future - props.past
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
      less: isLess,
      more: isMore,
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
