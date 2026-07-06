<script lang="ts" setup>
// Legacy route: stream reports moved to /conus/stream/<segment id>.
// Redirect so old bookmarks and shared links keep working.
const route = useRoute()

await navigateTo(
  {
    path: `/conus/stream/${route.params.segment}`,
    query: route.query,
    hash: route.hash,
  },
  { redirectCode: 301, replace: true }
)
</script>

<template>
  <div></div>
</template>

<style scoped></style>
