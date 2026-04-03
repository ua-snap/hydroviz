// f)ormat n)umber with c)ommas
export const fnc = (number: number): string => {
  return new Intl.NumberFormat().format(number)
}

// round to sig)nificant fig)ures
export const roundSigFig = (number: number): number => {
  let precision = 3
  if (number > 100000) {
    precision = 4
  }
  if (number < 100) {
    precision = 2
  }

  return Number(number.toPrecision(precision))
}

export const doyToDateString = (doy: number, monthOnly: boolean = false) => {
  const year = 2025 // Can be any year, but not a leap year.
  const date = new Date(year, 0) // January 1st of the given year
  date.setDate(Math.round(doy)) // Add DOY as days offset
  const options: Intl.DateTimeFormatOptions = monthOnly
    ? { month: 'short' }
    : { month: 'short', day: 'numeric' }
  return date.toLocaleDateString('en-US', options)
}
