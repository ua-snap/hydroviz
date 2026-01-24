type StreamflowStatisticName =
  | 'dh1'
  | 'dh2'
  | 'dh3'
  | 'dh4'
  | 'dh5'
  | 'dh15'
  | 'dl1'
  | 'dl2'
  | 'dl3'
  | 'dl4'
  | 'dl5'
  | 'dl16'
  | 'lf1'
  | 'spr_dur3'
  | 'spr_dur7'
  | 'sum_dur3'
  | 'sum_dur7'
  | 'fh1'
  | 'fh5'
  | 'fh6'
  | 'fh7'
  | 'fl1'
  | 'fl3'
  | 'spr_freq'
  | 'sum_freq'
  | 'ma3'
  | 'ma4'
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
  | 'mh14'
  | 'mh20'
  | 'ml17'
  | 'spr_mag'
  | 'sum_cv'
  | 'sum_mag'
  | 'ra1'
  | 'ra3'
  | 'ra8'
  | 'spr_ord'
  | 'sum_ord'
  | 'th1'
  | 'tl1'

export const streamflowStatisticCategories = [
  'magnitude',
  'frequency',
  'duration',
  'timing',
  'rate_of_change',
] as const
export type StreamflowStatisticCategory =
  (typeof streamflowStatisticCategories)[number]

interface StreamflowStatistic {
  id: StreamflowStatisticName
  category: StreamflowStatisticCategory
  code_base: 'mhit' | 'matlab'
  difference_method: 'ratio' | 'absolute'
  description_full: string
  description: string
  units: string
  units_short: string
}

const streamflowStatistics: StreamflowStatistic[] = [
  {
    id: 'dh1',
    category: 'duration',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Annual maximum daily flow.   Compute the maximum of a 1-day moving average flow for each year.  DH1 is the mean of these values (cubic feet per second - temporal).',
    description: 'Annual maximum daily flow',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'dh2',
    category: 'duration',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Annual maximum of 3-day moving average flows.  Compute the maximum of a 3-day moving average flow for each year. DH2 is the mean of these values (cubic feet per second - tempora[...]',
    description: 'Annual maximum of 3-day moving average flows',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'dh3',
    category: 'duration',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Annual maximum of 7-day moving average flows.    Compute the maximum of a 7-day moving average flow for each year. DH3 is the mean of these values (cubic feet per second - tempora[...]',
    description: 'Annual maximum of 7-day moving average flows',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'dh4',
    category: 'duration',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Annual maximum of 30-day moving average flows.   Compute the maximum of 30-day moving average flows.    Compute the maximum of a 30-day moving average flow for each year.    DH4 is the[...]',
    description: 'Annual maximum of 30-day moving average flows',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'dh5',
    category: 'duration',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Annual maximum of 90-day moving average flows. Compute the maximum of a 90-day moving average flow for each year. DH5 is the mean of these values (cubic feet per second - tempo[...]',
    description: 'Annual maximum of 90-day moving average flows',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'dh15',
    category: 'duration',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'High flow pulse duration.  Compute the average duration for flow events with flows above a threshold equal to the 75th percentile value for each year in the flow record. DH15 i[...]',
    description: 'High flow pulse duration',
    units: 'days per year',
    units_short: 'days/yr',
  },
  {
    id: 'dl1',
    category: 'duration',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Annual minimum daily flow.  Compute the minimum 1-day average flow for each year. DL1 is the mean of these values (cubic feet per second - temporal).',
    description: 'Annual minimum daily flow',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'dl2',
    category: 'duration',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Annual minimum of 3-day moving average flow. Compute the minimum of a 3-day moving average flow for each year. DL2 is the mean of these values (cubic feet per second - temporal[...]',
    description: 'Annual minimum of 3-day moving average flow',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'dl3',
    category: 'duration',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Annual minimum of 7-day moving average flow. Compute the minimum of a 7-day moving average flow for each year. DL3 is the mean of these values (cubic feet per second - temporal[...]',
    description: 'Annual minimum of 7-day moving average flow',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'dl4',
    category: 'duration',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Annual minimum of 30-day moving average flow. Compute the minimum of a 30-day moving average flow for each year. DL4 is the mean of these values (cubic feet per second - tempor[...]',
    description: 'Annual minimum of 30-day moving average flow',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'dl5',
    category: 'duration',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Annual minimum of 90-day moving average flow. Compute the minimum of a 90-day moving average flow for each year. DL5 is the mean of these values (cubic feet per second - tempor[...]',
    description: 'Annual minimum of 90-day moving average flow',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'dl16',
    category: 'duration',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Low flow pulse duration. Compute the average pulse duration for each year for flow events below a threshold equal to the 25th percentile value for the entire flow record. DL16[...]',
    description: 'Low flow pulse duration',
    units: 'days per year',
    units_short: 'days/yr',
  },
  {
    id: 'lf1',
    category: 'duration',
    code_base: 'matlab',
    difference_method: 'absolute',
    description_full:
      'Number of days per year below a threshold of 0.1 cubic feet per second per square mile.    LF1 is the median annual number of days below the threshold (number of days/year - [...]',
    description: 'Number of days per year below a low-flow threshold',
    units: 'days per year',
    units_short: 'days/yr',
  },
  {
    id: 'spr_dur3',
    category: 'duration',
    code_base: 'matlab',
    difference_method: 'ratio',
    description_full:
      'Spring (April-June) maximum of 3-day moving average flows.    Compute the maximum of a 3-day moving average flow for each year.    SPR_DUR3 is the median of these values (cubi[...]',
    description: 'Spring (April–June) maximum of 3-day moving average flows',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'spr_dur7',
    category: 'duration',
    code_base: 'matlab',
    difference_method: 'ratio',
    description_full:
      'Spring (April-June) maximum of 7-day moving average flows.   Compute the maximum of a 7-day moving average flow for each year. SPR_DUR7 is the median of these values (cubi[...]',
    description: 'Spring (April–June) maximum of 7-day moving average flows',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'sum_dur3',
    category: 'duration',
    code_base: 'matlab',
    difference_method: 'ratio',
    description_full:
      'Summer (July-September) minimum of 3-day moving average flow.   Compute the minimum of a 3-day moving average flow for each year. SUM_DUR3 is the median of these values (c[...]',
    description: 'Summer (July–September) minimum of 3-day moving average flow',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'sum_dur7',
    category: 'duration',
    code_base: 'matlab',
    difference_method: 'ratio',
    description_full:
      'Summer (July-September) minimum of 7-day moving average flow.   Compute the minimum of a 7-day moving average flow for each year.    SUM_DUR7 is the median of these values (c[...]',
    description: 'Summer (July–September) minimum of 7-day moving average flow',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'fh1',
    category: 'frequency',
    code_base: 'mhit',
    difference_method: 'absolute',
    description_full:
      'High flood pulse count. Compute the average number of flow events with flows above a threshold equal to the 75th percentile value for the entire flow record.    FH1 is the mea[...]',
    description: 'High flood pulse count',
    units: 'events per year',
    units_short: 'events/yr',
  },
  {
    id: 'fh5',
    category: 'frequency',
    code_base: 'mhit',
    difference_method: 'absolute',
    description_full:
      'Flood frequency.  Compute the average number of flow events with flows above a threshold equal to the median flow value for the entire flow record.  FH5 is the mean number of[...]',
    description: 'Flood frequency (above median flow)',
    units: 'events per year',
    units_short: 'events/yr',
  },
  {
    id: 'fh6',
    category: 'frequency',
    code_base: 'mhit',
    difference_method: 'absolute',
    description_full:
      'Flood frequency. Compute the average number of flow events with flows above a threshold equal to three times the median flow value for the entire flow record.  FH6 is the me[...]',
    description: 'Flood frequency (above 3× median flow)',
    units: 'events per year',
    units_short: 'events/yr',
  },
  {
    id: 'fh7',
    category: 'frequency',
    code_base: 'mhit',
    difference_method: 'absolute',
    description_full:
      'Flood frequency.    Compute the average number of flow events with flows above a threshold equal to seven times the median flow value for the entire flow record.  FH7 is the me[...]',
    description: 'Flood frequency (above 7× median flow)',
    units: 'events per year',
    units_short: 'events/yr',
  },
  {
    id: 'fl1',
    category: 'frequency',
    code_base: 'mhit',
    difference_method: 'absolute',
    description_full:
      'Low flood pulse count. Compute the average number of flow events with flows below a threshold equal to the 25th percentile value for the entire flow record.   FL1 is the mean[...]',
    description: 'Low flood pulse count',
    units: 'events per year',
    units_short: 'events/yr',
  },
  {
    id: 'fl3',
    category: 'frequency',
    code_base: 'mhit',
    difference_method: 'absolute',
    description_full:
      'Frequency of low pulse spells. Compute the average number of flow events with flows below a threshold equal to 5 percent of the mean flow value for the entire flow record.    [...]',
    description: 'Frequency of low pulse spells',
    units: 'events per year',
    units_short: 'events/yr',
  },
  {
    id: 'spr_freq',
    category: 'frequency',
    code_base: 'matlab',
    difference_method: 'absolute',
    description_full:
      'Flood frequency for April-June.  Compute the average number of flow events with flows above a threshold equal to the 10th percentile for the entire flow record.  SPR_F[...]',
    description: 'Spring flood frequency (April–June)',
    units: 'events per year',
    units_short: 'events/yr',
  },
  {
    id: 'sum_freq',
    category: 'frequency',
    code_base: 'matlab',
    difference_method: 'absolute',
    description_full:
      'Flood frequency for July-September.  Compute the average number of flow events with flows below a threshold equal to the 90th percentile for the entire flow record. S[...]',
    description: 'Summer flood frequency (July–September)',
    units: 'events per year',
    units_short: 'events/yr',
  },
  {
    id: 'ma3',
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Coefficient of variation (standard deviation/mean) for each year.    Compute the coefficient of variation for each year of daily flows.   Compute the mean of the annual coefficient[...]',
    description: 'Coefficient of variation of annual daily flows',
    units: 'percent',
    units_short: '%',
  },
  {
    id: 'ma4',
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Standard deviation of the percentiles of the logs of the entire flow record divided by the mean of percentiles of the logs.    Compute the log10 of the daily flows for the entir[...]',
    description: 'Standard deviation divided by mean of log-flow percentiles',
    units: 'percent',
    units_short: '%',
  },
  {
    id: 'ma12',
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full: 'Mean of monthly flow values for January.',
    description: 'Mean of monthly flow values for January',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'ma13',
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full: 'Mean of monthly flow values for February.',
    description: 'Mean of monthly flow values for February',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'ma14',
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full: 'Mean of monthly flow values for March.',
    description: 'Mean of monthly flow values for March',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'ma15',
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full: 'Mean of monthly flow values for April.',
    description: 'Mean of monthly flow values for April',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'ma16',
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full: 'Mean of monthly flow values for May.',
    description: 'Mean of monthly flow values for May',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'ma17',
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full: 'Mean of monthly flow values for June.',
    description: 'Mean of monthly flow values for June',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'ma18',
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full: 'Mean of monthly flow values for July.',
    description: 'Mean of monthly flow values for July',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'ma19',
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full: 'Mean of monthly flow values for August.',
    description: 'Mean of monthly flow values for August',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'ma20',
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full: 'Mean of monthly flow values for September.',
    description: 'Mean of monthly flow values for September',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'ma21',
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full: 'Mean of monthly flow values for October.',
    description: 'Mean of monthly flow values for October',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'ma22',
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full: 'Mean of monthly flow values for November.',
    description: 'Mean of monthly flow values for November',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'ma23',
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full: 'Mean of monthly flow values for December.',
    description: 'Mean of monthly flow values for December',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'ma99',
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Annual mean streamflow, calculated as the mean of the monthly mean flows.',
    description:
      'Annual mean streamflow, calculated as the mean of the monthly mean flows',
    units: 'cubic feet per second',
    units_short: 'ft&sup3;/s',
  },
  {
    id: 'mh14',
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Median of annual maximum flows.  Compute the annual maximum flows from monthly maximum flows.  Compute the ratio of annual maximum flow to median annual flow for each year.  MH1[...]',
    description: 'Median ratio of annual maximum flow to median annual flow',
    units: 'dimensionless',
    units_short: '&mdash;',
  },
  {
    id: 'mh20',
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Specific mean annual maximum flow. MH20 is the mean of the annual maximum flows divided by the drainage area (cubic feet per second/square mile - temporal).',
    description: 'Specific mean annual maximum flow',
    units: 'cubic feet per second per square mile',
    units_short: 'ft&sup3;/s/mi&sup2;',
  },
  {
    id: 'ml17',
    category: 'magnitude',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Base flow.    Compute the mean annual flows.    Compute the minimum of a 7-day moving average flow for each year and divide them by the mean annual flow for that year.  ML17 is the [...]',
    description: 'Base flow index',
    units: 'dimensionless',
    units_short: '&mdash;',
  },
  {
    id: 'spr_mag',
    category: 'magnitude',
    code_base: 'matlab',
    difference_method: 'ratio',
    description_full:
      'Specific mean spring (April-June) maximum flow. The spr_mag statistic is the median of the annual maximum flows divided by the drainage area (cubic feet per second/squar[...]',
    description: 'Specific mean spring (April–June) maximum flow',
    units: 'cubic feet per second per square mile',
    units_short: 'ft&sup3;/s/mi&sup2;',
  },
  {
    id: 'sum_cv',
    category: 'magnitude',
    code_base: 'matlab',
    difference_method: 'ratio',
    description_full:
      'Coefficient of variation (standard deviation/mean) for each year for the summer (July-September). Compute the coefficient of variation for each year of daily flows.  Compu[...]',
    description: 'Coefficient of variation of summer daily flows',
    units: 'percent',
    units_short: '%',
  },
  {
    id: 'sum_mag',
    category: 'magnitude',
    code_base: 'matlab',
    difference_method: 'absolute',
    description_full:
      'Minimum of the summer (July-September) flows divided by the drainage area (cubic feet per second/square mile - temporal).',
    description: 'Minimum summer flow divided by drainage area',
    units: 'cubic feet per second per square mile',
    units_short: 'ft&sup3;/s/mi&sup2;',
  },
  {
    id: 'ra1',
    category: 'rate_of_change',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Rise rate.   Compute the change in flow for days in which the change is positive for the entire flow record. RA1 is the mean of these values (cubic feet per second/day - te[...]',
    description: 'Rise rate',
    units: 'cubic feet per second per day',
    units_short: 'ft&sup3;/s/day',
  },
  {
    id: 'ra3',
    category: 'rate_of_change',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Fall rate.  Compute the change in flow for days in which the change is negative for the entire flow record. RA3 is the mean of these values (cubic feet per second/day - te[...]',
    description: 'Fall rate',
    units: 'cubic feet per second per day',
    units_short: 'ft&sup3;/s/day',
  },
  {
    id: 'ra8',
    category: 'rate_of_change',
    code_base: 'mhit',
    difference_method: 'ratio',
    description_full:
      'Number of reversals.  Compute the number of days in each year when the change in flow from one day to the next changes direction. RA8 is the median of the yearly values (d[...]',
    description: 'Number of flow reversals',
    units: 'days',
    units_short: 'days',
  },
  {
    id: 'spr_ord',
    category: 'timing',
    code_base: 'matlab',
    difference_method: 'absolute',
    description_full:
      'Julian date of spring (April-June) maximum. Determine the Julian date that the maximum flow occurs for each year. SPR_ORD is the median of these values (Julian day - tem[...]',
    description: 'Julian date of spring maximum flow',
    units: 'Julian day',
    units_short: 'Julian day',
  },
  {
    id: 'sum_ord',
    category: 'timing',
    code_base: 'matlab',
    difference_method: 'absolute',
    description_full:
      'Julian date of summer (July-September) minimum. Determine the Julian date that the minimum flow occurs for each water year. SUM_ORD is the median of these values (Julian[...]',
    description: 'Julian date of summer minimum flow',
    units: 'Julian day',
    units_short: 'Julian day',
  },
  {
    id: 'th1',
    category: 'timing',
    code_base: 'mhit',
    difference_method: 'absolute',
    description_full:
      'Julian date of annual maximum.   Determine the Julian date that the maximum flow occurs for each year.   TH1 is the median of these values (Julian day - temporal).',
    description: 'Julian date of annual maximum flow',
    units: 'Julian day',
    units_short: 'Julian day',
  },
  {
    id: 'tl1',
    category: 'timing',
    code_base: 'mhit',
    difference_method: 'absolute',
    description_full:
      'Julian date of annual minimum.  Determine the Julian date that the minimum flow occurs for each water year.  TL1 is the median of these values (Julian day - temporal).',
    description: 'Julian date of annual minimum flow',
    units: 'Julian day',
    units_short: 'Julian day',
  },
]

export {
  streamflowStatistics,
  type StreamflowStatistic,
  type StreamflowStatisticName,
}
