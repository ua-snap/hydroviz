import autoComplete from '@tarekraafat/autocomplete.js'
import '@tarekraafat/autocomplete.js/dist/css/autoComplete.02.css'

export default defineNuxtPlugin(nuxtApp => {
  return {
    provide: {
      autoComplete,
    },
  }
})
