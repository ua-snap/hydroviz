type StatCode =
  | 'dh3'
  | 'dh15'
  | 'dl3'
  | 'dl16'
  | 'fh1'
  | 'fl1'
  | 'fl3'
  | 'ma12'
  | 'ma13'
  | 'ma14'
  | 'ma15'
  | 'ma16'
  | 'ma17'
  | 'ma18'
  | 'ma19'
  | 'ma20'
  | 'ma21'
  | 'ma22'
  | 'ma23'
  | 'ra1'
  | 'ra3'
  | 'th1'
  | 'tl1'

interface StatDetails {
  category: string
  code_base: string
  difference_method: string
  title: string
  description: string
  units: string
}

export const statVars: Record<StatCode, StatDetails> = {
  dh3: {
    category: 'duration',
    code_base: 'mhit',
    difference_method: 'ratio',
    title: 'Annual maximum of 7-day moving average flows',
    description:
      'Compute the maximum of a 7-day moving average flow for each year. DH3 is the median of these values (cubic feet per second).',
    units: 'cfs',
  },
  dh15: {
    category: 'duration',
    code_base: 'mhit',
    difference_method: 'ratio',
    title: 'High flow pulse duration',
    description:
      'Compute the average duration for flow events with flows above a threshold equal to the 75th percentile value for each year in the flow record. DH15 is the median of these values (days/year).',
    units: 'days/year',
  },
  dl3: {
    category: 'duration',
    code_base: 'mhit',
    difference_method: 'ratio',
    title: 'Annual minimum of 7-day moving average flow',
    description:
      'Compute the minimum of a 7-day moving average flow for each year. DL3 is the median of these values (cubic feet per second).',
    units: 'cfs',
  },
  dl16: {
    category: 'duration',
    code_base: 'mhit',
    difference_method: 'ratio',
    title: 'Low flow pulse duration',
    description:
      'Compute the average pulse duration for each year for flow events below a threshold equal to the 25th percentile value for the entire flow record. DL16 is the median of these values (days/year).',
    units: 'days/year',
  },
  fh1: {
    category: 'frequency',
    code_base: 'mhit',
    difference_method: 'absolute',
    title: 'High flood pulse count',
    description:
      'Compute the average number of flow events with flows above a threshold equal to the 75th percentile value for the entire flow record. FH1 is the median of these values (events/year).',
    units: 'events/year',
  },
  fl1: {
    category: 'frequency',
    code_base: 'mhit',
    difference_method: 'absolute',
    title: 'Low flood pulse count',
    description:
      'Compute the average number of flow events with flows below a threshold equal to the 25th percentile value for the entire flow record. FL1 is the median of these values (events/year).',
    units: 'events/year',
  },
  fl3: {
    category: 'frequency',
    code_base: 'mhit',
    difference_method: 'absolute',
    title: 'Frequency of low pulse spells',
    description:
      'Compute the average number of flow events with flows below a threshold equal to 5 percent of the mean flow value for the entire flow record. FL3 is the median of these values (events/year).',
    units: 'events/year',
  },
  ma12: {
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    title: 'Mean of monthly flow values for January',
    description: '',
    units: 'cfs',
  },
  ma13: {
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    title: 'Mean of monthly flow values for February',
    description: '',
    units: 'cfs',
  },
  ma14: {
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    title: 'Mean of monthly flow values for March',
    description: '',
    units: 'cfs',
  },
  ma15: {
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    title: 'Mean of monthly flow values for April',
    description: '',
    units: 'cfs',
  },
  ma16: {
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    title: 'Mean of monthly flow values for May',
    description: '',
    units: 'cfs',
  },
  ma17: {
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    title: 'Mean of monthly flow values for June',
    description: '',
    units: 'cfs',
  },
  ma18: {
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    title: 'Mean of monthly flow values for July',
    description: '',
    units: 'cfs',
  },
  ma19: {
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    title: 'Mean of monthly flow values for August',
    description: '',
    units: 'cfs',
  },
  ma20: {
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    title: 'Mean of monthly flow values for September',
    description: '',
    units: 'cfs',
  },
  ma21: {
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    title: 'Mean of monthly flow values for October',
    description: '',
    units: 'cfs',
  },
  ma22: {
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    title: 'Mean of monthly flow values for November',
    description: '',
    units: 'cfs',
  },
  ma23: {
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    title: 'Mean of monthly flow values for December',
    description: '',
    units: 'cfs',
  },
  ra1: {
    category: 'rate_of_change',
    code_base: 'mhit',
    difference_method: 'ratio',
    title: 'Rise rate',
    description:
      'Compute the change in flow for days in which the change is positive for the entire flow record. RA1 is the median of these values (cubic feet per second/day).',
    units: 'cfs/day',
  },
  ra3: {
    category: 'rate_of_change',
    code_base: 'mhit',
    difference_method: 'ratio',
    title: 'Fall rate',
    description:
      'Compute the change in flow for days in which the change is negative for the entire flow record. RA3 is the median of these values (cubic feet per second/day).',
    units: 'cfs/day',
  },
  th1: {
    category: 'timing',
    code_base: 'mhit',
    difference_method: 'absolute',
    title: 'Julian date of annual maximum',
    description:
      'Determine the Julian date that the maximum flow occurs for each year. TH1 is the median of these values (Julian day - temporal).',
    units: 'day',
  },
  tl1: {
    category: 'timing',
    code_base: 'mhit',
    difference_method: 'absolute',
    title: 'Julian date of annual minimum',
    description:
      'Determine the Julian date that the minimum flow occurs for each water year. TL1 is the median of these values (Julian day - temporal).',
    units: 'day',
  },
}
