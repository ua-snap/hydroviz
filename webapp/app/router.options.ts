import type { RouterConfig } from '@nuxt/schema'

// Interval for the polling loops below. setTimeout rather than
// requestAnimationFrame, because rAF is paused entirely in hidden/background
// tabs and the loops must still make progress there (e.g. a report opened in
// a background tab, or a headless browser).
const pollMs = 100

// Poll until check() returns a truthy value or the timeout (ms) elapses;
// resolves with the value, or null on timeout/error. Report sections render
// asynchronously (gated on data fetches), so scroll targets can appear well
// after navigation completes.
const waitFor = <T>(check: () => T | null | false, timeout: number) =>
  new Promise<T | null>(resolve => {
    const start = Date.now()
    const tick = () => {
      let found: T | null | false = null
      try {
        found = check()
      } catch {
        return resolve(null)
      }
      if (found) resolve(found)
      else if (Date.now() - start < timeout) setTimeout(tick, pollMs)
      else resolve(null)
    }
    tick()
  })

// Hold an anchor element at the top of the viewport while late-rendering
// content above it (charts, maps) keeps changing the page height. Browsers do
// this natively for late-loading fragments on plain pages; the SPA has to do
// it by hand. Stops once the element's position has been stable for a moment
// (or at the timeout), and backs off immediately if the user scrolls on their
// own. Resolves true if the pin ran to completion, false if the user took
// over.
const pinToAnchor = (el: Element, timeout: number) =>
  new Promise<boolean>(resolve => {
    const settleMs = 500
    let cancelled = false
    const cancel = () => {
      cancelled = true
    }
    const cancelEvents = ['wheel', 'touchstart', 'mousedown', 'keydown']
    cancelEvents.forEach(type =>
      window.addEventListener(type, cancel, { passive: true })
    )
    const done = (completed: boolean) => {
      cancelEvents.forEach(type => window.removeEventListener(type, cancel))
      resolve(completed)
    }
    const start = Date.now()
    let lastTop: number | null = null
    let stableSince = Date.now()
    const tick = () => {
      if (cancelled) return done(false)
      const absTop = Math.round(el.getBoundingClientRect().top + window.scrollY)
      if (absTop !== lastTop) {
        lastTop = absTop
        window.scrollTo(0, absTop)
        stableSince = Date.now()
      }
      if (Date.now() - stableSince >= settleMs || Date.now() - start >= timeout)
        return done(true)
      setTimeout(tick, pollMs)
    }
    tick()
  })

export default <RouterConfig>{
  async scrollBehavior(to, from, savedPosition) {
    // First navigation after a full page load -- a reload, or the Back button
    // returning from an external site. In-app navigation always has a
    // resolved "from" route; the router's start location has no matches.
    const initialLoad = from.matched.length === 0

    // In-app back/forward: restore the remembered position.
    if (savedPosition && !initialLoad) return savedPosition

    // Hash target (e.g. search -> "#conus-map", or returning from an external
    // site to "#get-and-use"): wait for the element to exist, since the
    // sections render/resize asynchronously, then scroll to it. In-app clicks
    // animate; a full page load instead jumps to the anchor right away and
    // pins it while the content above finishes rendering. S3 hashbang
    // redirect URLs ("#!/...", see layouts/default.vue) are not element
    // anchors and are not valid selectors, so skip them.
    if (to.hash && !to.hash.startsWith('#!')) {
      // A full page load also waits on data fetches, so allow extra time.
      const el = await waitFor(
        () => document.querySelector(to.hash),
        initialLoad ? 10000 : 3000
      )
      if (el) {
        if (!initialLoad) return { el: to.hash, behavior: 'smooth' }
        // Let the router apply the final position only if the user hasn't
        // scrolled away mid-pin; returning false leaves their scroll alone.
        const completed = await pinToAnchor(el, 10000)
        return completed ? { el: to.hash } : false
      }
    }

    // Full page load with a remembered position but no hash target (the
    // position is saved in history.state as the page unloads): wait until the
    // async content has made that position reachable, otherwise the scroll
    // would be clamped to the height of the still-loading page.
    if (savedPosition) {
      await waitFor(
        () =>
          document.documentElement.scrollHeight - window.innerHeight >=
          savedPosition.top,
        10000
      )
      return savedPosition
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
