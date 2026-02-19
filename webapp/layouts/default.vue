<script lang="ts" setup>
// Redirect S3 hashbang URLs to Nuxt URLs.
const route = useRoute()
</script>

<template>
  <NuxtRouteAnnouncer />
  <NuxtPage />
</template>
