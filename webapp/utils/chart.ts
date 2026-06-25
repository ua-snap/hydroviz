import type { Config, Layout } from 'plotly.js'
import lowess from '@stdlib/stats-lowess'

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
  hovermode: false,
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

// Shift a DOY-indexed dataset to hydro year (Oct 1 - Sept 30)
export const convertDoysToHydroYearDoys = (series: number[]): number[] => {
  let octDec = series.slice(273) // through end of array (366)
  let janSept = series.slice(0, 273)
  return octDec.concat(janSept)
}

// Round to significant digits.  Stub.
function roundTo(num, sig = 3) {
  return Number(num.toPrecision(sig))
}

// Converts & LOWESS smooths a timeseries of Y values
// Need to trick it so there's not discontinuity between day 366/1.
export const processLowessAndHydroYear = (
  traceData: number[],
  doys: number[]
): number[] => {
  let hydroYearTraceData = convertDoysToHydroYearDoys(traceData)

  // Bit tricky: we index the day-of-year as 1...366 for the x-axis
  // for the purpose of the lowess calculation, but the y-values represent
  // the hydro-year shifted values.  This gives us the correct, smooth
  // chart form.
  let smoothed = lowess(doys, hydroYearTraceData, {
    f: 0.05,
    sorted: true,
  })
  let hydroOrderedSmoothedY = smoothed.y.map((value: number) => {
    return roundTo(value)
  })
  return hydroOrderedSmoothedY
}

// Get offset x-tick values for monthly charts
export const getOffsetXTickVals = (
  xTickValOffsets: Record<string, number>,
  scenario: string
): number[] => {
  const numMonths = 12
  const xTickVals = Array.from({ length: numMonths }, (_, i) => i)
  const offset: number = xTickValOffsets[scenario] ?? 0
  const offsetXTickVals = xTickVals.map(tickVal => tickVal + offset)
  return offsetXTickVals
}

// Convert day-of-year to 360-degree representation for polar charts
// Values exceeding 360 cannot be plotted on a Plotly.js polarscatter chart.
// So, slightly squeeze 366 calendar to a 360 degree representation.
export const convertTo360 = (doy: number): number => {
  return ((doy - 1) / 366) * 360
}
