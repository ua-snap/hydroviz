<script setup>
import { NuxtLink } from '#components'
</script>

<template>
  <nav
    class="navbar navbar-bordered"
    role="navigation"
    aria-label="main navigation"
  >
    <div class="container">
      <div class="navbar-menu is-active">
        <div class="navbar-start">
          <NuxtLink to="/" class="navbar-item">Home</NuxtLink>
          <NuxtLink to="/about" class="navbar-item">About</NuxtLink>
          <NuxtLink to="/how-to" class="navbar-item">How-To Guide</NuxtLink>
          <NuxtLink to="/models-and-uncertainty" class="navbar-item"
            >Models and Uncertainty</NuxtLink
          >
          <NuxtLink to="/data" class="navbar-item">Data</NuxtLink>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar-bordered {
  border-bottom: 1px solid #e5e5e5;
}
</style>
