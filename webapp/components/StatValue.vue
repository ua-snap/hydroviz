<script setup lang="ts">
import { fnc, roundSigFig } from '~/utils/general'

const props = defineProps<{
  value: string | null
  past?: string | null
}>()

let value: number | null = null
if (props.value !== null && props.value !== undefined) {
  value = roundSigFig(Number(props.value))
}

let past: number | null = null
if (props.past !== null && props.past !== undefined) {
  past = roundSigFig(Number(props.past))
}

let formattedValue: string
if (props.value === null || props.value === undefined) {
  formattedValue = 'N/A'
} else {
  formattedValue = fnc(value!)
}
</script>

<template>
  <span>
    <span class="number">{{ formattedValue }}</span>
    <Diff v-if="past !== null && value !== null" :past="past" :future="value" />
  </span>
</template>
