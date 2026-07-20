<script setup>
import { NuxtLink } from '#components'

const trackNavClick = route => {
  window.trackUmamiEvent('nav-click', { route })
}
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
          <NuxtLink to="/" class="navbar-item" @click="trackNavClick('/')"
            >Home</NuxtLink
          >
          <NuxtLink
            to="/about"
            class="navbar-item"
            @click="trackNavClick('/about')"
            >About</NuxtLink
          >
          <NuxtLink
            to="/how-to"
            class="navbar-item"
            @click="trackNavClick('/how-to')"
            >How-To Guide</NuxtLink
          >
          <NuxtLink
            to="/models-and-uncertainty"
            class="navbar-item"
            @click="trackNavClick('/models-and-uncertainty')"
            >Models and Uncertainty</NuxtLink
          >
          <NuxtLink
            to="/data-and-methodology"
            class="navbar-item"
@click="trackNavClick('/data-and-methodology')"
            >Data and Methodology</NuxtLink
          >
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
