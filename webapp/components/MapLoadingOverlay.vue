<script setup lang="ts">
import waterLoaderUrl from '@/assets/water-loader.svg'
</script>

<template>
  <div class="map-loading-overlay">
    <img :src="waterLoaderUrl" class="map-loading-icon" alt="" />
    <p class="mt-3 has-text-white is-size-3 has-text-weight-semibold">
      <slot />
    </p>
  </div>
</template>

<style lang="scss" scoped>
// Covers the nearest positioned ancestor: the element wrapping the map
// must have position: relative.
.map-loading-overlay {
  position: absolute;
  inset: 0;
  // Above Leaflet panes (max ~700) and controls (~1000).
  z-index: 1100;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(128, 128, 128, 0.5);
  pointer-events: all;
}

.map-loading-icon {
  width: 6rem;
  height: 6rem;
}
</style>
