// Send uncaught client-side exceptions to the full-screen error page
// (error.vue). Errors thrown during SSR already end up there; without this,
// errors thrown after hydration are only logged to the console and leave the
// app in a broken state.
export default defineNuxtPlugin(nuxtApp => {
  const showErrorPage = (error: unknown) => {
    // Ignore errors that arrive once the error page is already showing.
    if (nuxtApp.payload.error) return
    showError(error instanceof Error ? error : new Error(String(error)))
  }

  // Errors from Vue component code: setup, render, lifecycle hooks,
  // watchers, and template event handlers. Nuxt installs its own app-level
  // error handler for initial load but removes it once the app has mounted,
  // leaving later errors unhandled (Vue then rethrows and the app is left in
  // a broken state). Reinstate one so those errors land on the error page.
  nuxtApp.hook('app:mounted', () => {
    nuxtApp.vueApp.config.errorHandler = error => showErrorPage(error)
  })

  // Errors from outside Vue: Leaflet and Plotly event handlers, timers, etc.
  window.addEventListener('error', event =>
    showErrorPage(event.error ?? event.message),
  )
  window.addEventListener('unhandledrejection', event =>
    showErrorPage(event.reason),
  )
})
