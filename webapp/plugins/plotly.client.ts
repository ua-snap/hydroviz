import Plotly from 'plotly.js-dist-min'

export default defineNuxtPlugin(nuxtApp => {
  return {
    provide: {
      Plotly,
    },
  }
})
