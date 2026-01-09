import type { Config, Layout } from 'plotly.js-dist-min'

export const getConfig = (filename: string): Partial<Config> => ({
  responsive: true, // changes the height / width dynamically for charts
  displayModeBar: true, // always show the camera icon
  displaylogo: false,
  modeBarButtonsToRemove: [
    'zoom2d',
    'pan2d',
    'select2d',
    'lasso2d',
    'zoomIn2d',
    'zoomOut2d',
    'autoScale2d',
    'resetScale2d',
  ],
  toImageButtonOptions: {
    format: 'png',
    filename: filename,
    scale: 2,
  },
})

export const getLayout = (
  title: string,
  yAxisLabel: string,
  xAxisConfig?: Partial<Layout['xaxis']>
): Partial<Layout> => ({
  title: {
    text: title,
    font: {
      size: 24,
    },
  },
  xaxis: {
    ...xAxisConfig,
  },
  yaxis: {
    title: {
      text: yAxisLabel,
      font: {
        size: 18,
      },
    },
  },
})
