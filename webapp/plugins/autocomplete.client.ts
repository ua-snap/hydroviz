import autoComplete from '@tarekraafat/autocomplete.js'
import '@tarekraafat/autocomplete.js/dist/css/autoComplete.css'

export default defineNuxtPlugin(nuxtApp => {
  return {
    provide: {
      autoComplete,
    },
  }
})