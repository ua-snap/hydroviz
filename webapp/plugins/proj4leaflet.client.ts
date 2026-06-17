import proj4leaflet from 'proj4leaflet'

export default defineNuxtPlugin(nuxtApp => {
  return {
    provide: {
      proj4leaflet,
    },
  }
})
