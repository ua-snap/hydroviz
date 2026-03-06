import Plotly from 'plotly.js-basic-dist-min'

export default defineNuxtPlugin(nuxtApp => {
  return {
    provide: {
      Plotly,
    },
  }
})
