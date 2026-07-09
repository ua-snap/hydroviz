import type { Config, Layout } from 'plotly.js'
import lowess from '@stdlib/stats-lowess'

export const getConfig = (filename: string): Partial<Config> => {
  return {
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
  }
}

const getFooterCredits = (isAlaskaData: boolean): string => {
  if (isAlaskaData) {
    return 'Data provided by Dylan Blaskey, Keith Musselman, Andrew Newman, &amp; Yifan Cheng. (2024). doi:10.18739/A25M62870'
  } else {
    return (
      'Historical data provided by U.S. Geological Survey National Water Information System. doi:10.5066/F7P55KJN<br>' +
      'Projected data provided by LaFontaine, J.H., and Riley, J.W., 2023. doi:10.5066/P9EBKREQ'
    )
  }
}

// Keep plot area, footer position, and margins consistent across chart types.
// For both web display and exported PNG images.
const getLayoutPositions = (
  isTwoLineTitle: boolean,
  isAlaskaData: boolean,
  chartType: string
) => {
  let height: null | number = null
  let marginTop: null | number = null
  let marginBottom: null | number = null
  let footerY: null | number = null

  const generalizedChartTypes: Record<string, string> = {
    hydrograph: 'hydrograph',
    temperatureHydrograph: 'hydrograph',
    monthlyFlow: 'monthlyBoxPlots',
    monthlyTemperature: 'monthlyBoxPlots',
    maxFlowDates: 'maxDates',
    maxTempDates: 'maxDates',
  }

  let generalizedChartType = generalizedChartTypes[chartType]

  if (isTwoLineTitle) {
    if (isAlaskaData) {
      if (generalizedChartType === 'hydrograph') {
        height = 515
        marginTop = 100
        marginBottom = 145
        footerY = -0.5
      } else if (generalizedChartType === 'monthlyBoxPlots') {
        height = 535
        marginTop = 120
        marginBottom = 140
        footerY = -0.44
      } else if (generalizedChartType === 'maxDates') {
        height = 560
        marginTop = 120
        marginBottom = 130
        footerY = -0.35
      }
    } else {
      if (generalizedChartType === 'hydrograph') {
        height = 535
        marginTop = 100
        marginBottom = 160
        footerY = -0.55
      } else if (generalizedChartType === 'monthlyBoxPlots') {
        height = 520
        marginTop = 100
        marginBottom = 145
        footerY = -0.48
      } else if (generalizedChartType === 'maxDates') {
        height = 555
        marginTop = 120
        marginBottom = 130
        footerY = -0.4
      }
    }
  } else {
    if (isAlaskaData) {
      if (generalizedChartType === 'hydrograph') {
        height = 505
        marginTop = 80
        marginBottom = 150
        footerY = -0.5
      } else if (generalizedChartType === 'monthlyBoxPlots') {
        height = 505
        marginTop = 100
        marginBottom = 130
        footerY = -0.43
      } else if (generalizedChartType === 'maxDates') {
        height = 530
        marginTop = 100
        marginBottom = 120
        footerY = -0.35
      }
    } else {
      if (generalizedChartType === 'hydrograph') {
        height = 520
        marginTop = 80
        marginBottom = 165
        footerY = -0.55
      } else if (generalizedChartType === 'monthlyBoxPlots') {
        height = 505
        marginTop = 80
        marginBottom = 145
        footerY = -0.48
      } else if (generalizedChartType === 'maxDates') {
        height = 535
        marginTop = 100
        marginBottom = 130
        footerY = -0.4
      }
    }
  }
  return { height, marginTop, marginBottom, footerY }
}

export const getLayout = (
  chartType: string,
  title: string,
  yAxisLabel: string,
  xAxisConfig?: Partial<Layout['xaxis']>,
  yAxisConfig?: Partial<Layout['yaxis']>,
  legendConfig?: Partial<Layout['legend']>,
  isTwoLineTitle: boolean = false,
  isAlaskaData: boolean = false
): Partial<Layout> => {
  let { height, marginTop, marginBottom, footerY } = getLayoutPositions(
    isTwoLineTitle,
    isAlaskaData,
    chartType
  )
  return {
    title: {
      text: title,
      font: {
        size: 24,
      },
      automargin: true,
      yref: 'container',
      y: 0.93,
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
    height: height,
    margin: {
      l: 100,
      t: marginTop,
      b: marginBottom,
      pad: 20,
    },
    autosize: true,
    dragmode: false,
    hovermode: false,
    annotations: [
      {
        text: getFooterCredits(isAlaskaData),
        xref: 'paper',
        yref: 'paper',
        x: 0.5,
        y: footerY,
        showarrow: false,
        font: {
          size: 12,
          color: '#333',
        },
      },
    ],
  }
}

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
