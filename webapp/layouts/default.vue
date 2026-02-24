<script lang="ts" setup>
// Redirect S3 hashbang URLs to Nuxt URLs.
const route = useRoute()

// Switch back to clean URL after S3 redirect. Adapted from here:
// https://via.studio/journal/hosting-a-reactjs-app-with-routing-on-aws-s3
const path = (/#!(\/.*)$/.exec(route.fullPath) || [])[1]
if (path) {
  navigateTo({ path: path })
}
</script>

<template>
  <NuxtRouteAnnouncer />
  <NuxtPage />
</template>
