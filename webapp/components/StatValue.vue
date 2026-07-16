<script setup lang="ts">
import { fnc, roundSigFig } from '~/utils/general'
import { computed } from 'vue'

const props = defineProps<{
  value: string | number | null
  past?: string | number | null
  statId?: string | undefined
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
    return 'not available<sup>*</sup>'
  }
  return fnc(value.value)
})
</script>

<template>
  <span>
    <span class="number" v-html="formattedValue" />
    <Diff
      v-if="past !== null && value !== null"
      :past="past"
      :future="value"
      :statId="props.statId"
    />
  </span>
</template>
