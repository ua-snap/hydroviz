<script setup lang="ts">
import { fnc, roundSigFig } from '~/utils/general'
import { computed } from 'vue'

const props = defineProps<{
  value: string | null
  past?: string | null
}>()

const value = computed<number | null>(() => {
  if (props.value === null || props.value === undefined) {
    return null
  }
  return roundSigFig(Number(props.value))
})

const past = computed<number | null>(() => {
  if (props.past === null || props.past === undefined) {
    return null
  }
  return roundSigFig(Number(props.past))
})

const formattedValue = computed(() => {
  if (value.value === null) {
    return 'N/A'
  }
  return fnc(value.value)
})
</script>

<template>
  <span>
    <span class="number">{{ formattedValue }}</span>
    <Diff v-if="past !== null && value !== null" :past="past" :future="value" />
  </span>
</template>
