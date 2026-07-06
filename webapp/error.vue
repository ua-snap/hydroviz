<script lang="ts" setup>
import { computed } from 'vue'
import type { NuxtError } from '#app'

const props = defineProps<{
  error: NuxtError
}>()

const is404 = computed(() => props.error?.statusCode === 404)

const goHome = () => clearError({ redirect: '/' })
</script>

<template>
  <NavBar />
  <div class="error-hero">
    <div class="container clamp has-text-white">
      <h2 class="title is-2">
        {{ is404 ? 'This stream has run dry.' : 'Something went wrong.' }}
      </h2>
      <h3 class="subtitle is-3">
        {{ is404 ? 'Page not found (404)' : `Error ${error?.statusCode}` }}
      </h3>
      <p v-if="error?.message" class="block is-size-4">
        {{ error.message }}
      </p>
      <button class="button is-link is-medium" @click="goHome">
        Return to the home page
      </button>
      <p class="is-size-7 has-text-grey">Photo credit Matt Palmer / Unsplash</p>
    </div>
  </div>
  <Footer />
</template>

<style lang="scss" scoped>
.error-hero {
  h2,
  h3 {
    color: white !important;
  }
  height: 80vh;
  display: flex;
  align-items: center;
  background-image: url('~/assets/images/dry-streambed.jpg');
  background-size: cover;
  background-position: center;
}
</style>
