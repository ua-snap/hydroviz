<script setup lang="ts">
const router = useRouter()

// Returns to the map, restoring its zoom/center/phase via browser history when
// this report was reached from the map. On a direct visit (shared link) there
// is no in-app history to go back to, so fall back to the home page.
const goBackToMap = () => {
  if (window.history.state?.back) {
    router.back()
  } else {
    navigateTo('/')
  }
}
</script>

<template>
  <section class="section pb-0">
    <div class="container">
      <a class="content is-size-5" href="/" @click.prevent="goBackToMap"
        >&larr; Go back, choose another segment</a
      >
    </div>
  </section>
</template>

<style lang="scss" scoped></style>
