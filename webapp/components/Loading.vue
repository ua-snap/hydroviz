<script setup lang="ts">
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { streamStats, segmentName, isLoading } = storeToRefs(streamSegmentStore)
</script>
<template>
	<div v-if="isLoading == true" class="loading content is-size-4">
		<p>Loading data&hellip; this can take a minute or two.</p>
		<progress class="progress" />
	</div>
</template>
