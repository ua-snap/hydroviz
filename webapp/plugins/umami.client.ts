// Umami analytics event helper.
//
// The Umami script itself is loaded from nuxt.config.ts. This plugin defines a
// global guard function so components can record custom events without caring
// whether Umami actually loaded (it may be blocked by an ad blocker, or absent
// entirely during development because of the data-domains restriction).
declare global {
  interface Window {
    umami?: {
      track: (eventName: string, payload?: Record<string, unknown>) => void
    }
    trackUmamiEvent: (
      eventName: string,
      payload?: Record<string, unknown>
    ) => void
  }
}

export default defineNuxtPlugin(() => {
  // Guard in case Umami is not available
  window.trackUmamiEvent = function (eventName, payload) {
    if (window.umami && window.umami.track) {
      window.umami.track(eventName, payload)
    }
  }
})
