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
  xAxisConfig?: Partial<Layout['xaxis']>,
  yAxisConfig?: Partial<Layout['yaxis']>,
  legendConfig?: Partial<Layout['legend']>
): Partial<Layout> => ({
  title: {
    text: title,
    font: {
      size: 24,
    },
    automargin: true,
  },
  xaxis: {
    automargin: true,
    gridcolor: '#aaaaaa',
    ...xAxisConfig,
  },
  yaxis: {
    gridcolor: '#aaaaaa',
    automargin: true,
    title: {
      text: yAxisLabel,
      font: {
        size: 18,
      },
    },
    ...yAxisConfig,
  },
  legend: {
    ...legendConfig,
  },
  margin: {
    l: 100,
    t: 50,
    b: 100,
    pad: 20,
  },
  autosize: true,
})

export const initializeChart = (
  $Plotly: any,
  chartId: string,
  buildChart: Function,
  sourceData: any
): void => {
  // BUG: this check passes and it tries to render even when
  // newValue is actually null.  (!)
  if (sourceData) {
    $Plotly.purge(chartId)
    buildChart(sourceData)
    window.dispatchEvent(new Event('resize'))
  }
}
