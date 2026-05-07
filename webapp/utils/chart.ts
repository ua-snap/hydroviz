import type { Config, Layout } from 'plotly.js'

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
    yref: 'container',
    y: 0.95,
  },
  xaxis: {
    automargin: true,
    gridcolor: 'rgba(0,0,0,0.08)',
    ...xAxisConfig,
  },
  yaxis: {
    gridcolor: 'rgba(0,0,0,0.08)',
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
    t: 80,
    b: 60,
    pad: 20,
  },
  autosize: true,
  dragmode: false,
})

// Recursively extract all relevant values (data keys not in excludeKeys) from
// API data response, find the min/max values, add some padding, and return.
export const getDataRange = (
  data: any,
  excludeKeys: string[] = []
): { yMin: number; yMax: number } => {
  const extractNumbers = (obj: any): number[] => {
    if (typeof obj === 'number') {
      return [obj]
    }
    if (Array.isArray(obj)) {
      return obj.flatMap(extractNumbers)
    }
    if (obj && typeof obj === 'object') {
      const allowedEntries = Object.entries(obj).filter(
        ([key]) => !excludeKeys.includes(key)
      )
      return allowedEntries.flatMap(([, value]) => extractNumbers(value))
    }
    return []
  }

  const allValues = extractNumbers(data)
  const paddingFactor = 0.05
  return {
    yMin: Math.min(...allValues) * (1 - paddingFactor),
    yMax: Math.max(...allValues) * (1 + paddingFactor),
  }
}

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
