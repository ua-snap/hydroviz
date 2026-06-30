import type { RouterConfig } from '@nuxt/schema'

export default <RouterConfig>{
  async scrollBehavior(to, from, savedPosition) {
    // Back/forward: restore the remembered position.
    if (savedPosition) return savedPosition

    // Hash target (e.g. search -> "#conus-map"): wait for the element to exist,
    // since the map sections render/resize asynchronously, then scroll to it.
    if (to.hash) {
      const el = await new Promise<Element | null>(resolve => {
        const start = Date.now()
        const tick = () => {
          const found = document.querySelector(to.hash)
          if (found) resolve(found)
          else if (Date.now() - start < 3000) requestAnimationFrame(tick)
          else resolve(null)
        }
        tick()
      })
      if (el) return { el: to.hash, behavior: 'smooth' }
    }

    // Same-page query updates (the map writes its pan/phase back to the URL via
    // router.replace/push with no hash) must NOT move the scroll position --
    // otherwise the page jumps to the top right after the hash scroll lands.
    // Returning false leaves the current scroll untouched.
    if (to.path === from.path) return false

    // Genuine page-to-page navigation: start at the top.
    return { left: 0, top: 0 }
  },
}
