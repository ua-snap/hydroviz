
# this dict holds metadata for the summary statistics
# the keys of this dict also serve to filter the columns read from the statistics CSVs in functions.populate_dataset()
# therefore, commenting out keys in this dict will prevent those statistics from being read into the netCDFs
stat_vars_dict = {
    "dh3" : {
        "category" : "duration",
        "code_base" : "mhit",
        "difference_method" : "ratio",
        "statistic_description" : "Annual maximum of 7-day moving average flows. Compute the maximum of a 7-day moving average flow for each year. DH3 is the median of these values (cubic feet per second - temporal)."
    },
    "dh15" : {
        "category" : "duration",
        "code_base" : "mhit",
        "difference_method" : "ratio",
        "statistic_description" : "High flow pulse duration. Compute the average duration for flow events with flows above a threshold equal to the 75th percentile value for each year in the flow record. DH15 is the median of the yearly average durations (days/year - temporal)."
    },
    "dl3" : {
        "category" : "duration",
        "code_base" : "mhit",
        "difference_method" : "ratio",
        "statistic_description" : "Annual minimum of 7-day moving average flow. Compute the minimum of a 7-day moving average flow for each year. DL3 is the median of these values (cubic feet per second - temporal)."
    },
    "dl16" : {
        "category" : "duration",
        "code_base" : "mhit",
        "difference_method" : "ratio",
        "statistic_description" : "Low flow pulse duration. Compute the average pulse duration for each year for flow events below a threshold equal to the 25th percentile value for the entire flow record. DL16 is the median of the yearly average durations (days/year - temporal)."
    },
    "fh1" : {
        "category" : "frequency",
        "code_base" : "mhit",
        "difference_method" : "absolute",
        "statistic_description" : "High flood pulse count. Compute the average number of flow events with flows above a threshold equal to the 75th percentile value for the entire flow record. FH1 is the median number of events (number of events/year - temporal)."
    },
    "fl1" : {
        "category" : "frequency",
        "code_base" : "mhit",
        "difference_method" : "absolute",
        "statistic_description" : "Low flood pulse count. Compute the average number of flow events with flows below a threshold equal to the 25th percentile value for the entire flow record. FL1 is the median number of events (number of events/year - temporal)."
    },
    "fl3" : {
        "category" : "frequency",
        "code_base" : "mhit",
        "difference_method" : "absolute",
        "statistic_description" : "Frequency of low pulse spells. Compute the average number of flow events with flows below a threshold equal to 5 percent of the mean flow value for the entire flow record. FL3 is the median number of events (number of events/year - temporal)."
    },
    "ma12" : {
        "category" : "magnitude",
        "code_base" : "mhit",
        "difference_method" : "ratio",
        "statistic_description" : "Mean of monthly flow values for January."
    },
    "ma13" : {
        "category" : "magnitude",
        "code_base" : "mhit",
        "difference_method" : "ratio",
        "statistic_description" : "Mean of monthly flow values for February."
    },
    "ma14" : {
        "category" : "magnitude",
        "code_base" : "mhit",
        "difference_method" : "ratio",
        "statistic_description" : "Mean of monthly flow values for March."
    },
    "ma15" : {
        "category" : "magnitude",
        "code_base" : "mhit",
        "difference_method" : "ratio",
        "statistic_description" : "Mean of monthly flow values for April."
    },
    "ma16" : {
        "category" : "magnitude",
        "code_base" : "mhit",
        "difference_method" : "ratio",
        "statistic_description" : "Mean of monthly flow values for May."
    },
    "ma17" : {
        "category" : "magnitude",
        "code_base" : "mhit",
        "difference_method" : "ratio",
        "statistic_description" : "Mean of monthly flow values for June."
    },
    "ma18" : {
        "category" : "magnitude",
        "code_base" : "mhit",
        "difference_method" : "ratio",
        "statistic_description" : "Mean of monthly flow values for July."
    },
    "ma19" : {
        "category" : "magnitude",
        "code_base" : "mhit",
        "difference_method" : "ratio",
        "statistic_description" : "Mean of monthly flow values for August."
    },
    "ma20" : {
        "category" : "magnitude",
        "code_base" : "mhit",
        "difference_method" : "ratio",
        "statistic_description" : "Mean of monthly flow values for September."
    },
    "ma21" : {
        "category" : "magnitude",
        "code_base" : "mhit",
        "difference_method" : "ratio",
        "statistic_description" : "Mean of monthly flow values for October."
    },
    "ma22" : {
        "category" : "magnitude",
        "code_base" : "mhit",
        "difference_method" : "ratio",
        "statistic_description" : "Mean of monthly flow values for November."
    },
    "ma23" : {
        "category" : "magnitude",
        "code_base" : "mhit",
        "difference_method" : "ratio",
        "statistic_description" : "Mean of monthly flow values for December."
    },
    "ra1" : {
        "category" : "rate_of_change",
        "code_base" : "mhit",
        "difference_method" : "ratio",
        "statistic_description" : "Rise rate. Compute the change in flow for days in which the change is positive for the entire flow record. RA1 is the median of these values (cubic feet per second/day - temporal)."
    },
    "ra3" : {
        "category" : "rate_of_change",
        "code_base" : "mhit",
        "difference_method" : "ratio",
        "statistic_description" : "Fall rate. Compute the change in flow for days in which the change is negative for the entire flow record. RA3 is the median of these values (cubic feet per second/day - temporal)."
    },
    "th1" : {
        "category" : "timing",
        "code_base" : "mhit",
        "difference_method" : "absolute",
        "statistic_description" : "Julian date of annual maximum. Determine the Julian date that the maximum flow occurs for each year. TH1 is the median of these values (Julian day - temporal)."
    },
    "tl1" : {
        "category" : "timing",
        "code_base" : "mhit",
        "difference_method" : "absolute",
        "statistic_description" : "Julian date of annual minimum. Determine the Julian date that the minimum flow occurs for each water year. TL1 is the median of these values (Julian day - temporal)."
    },
}

# encodings for netCDF, integers required for rasdaman ingest
encodings_lookup = {
    "lc": {
        "dynamic": 0,
        "static": 1,
    },
    "model": {
        "ACCESS1-0": 0,
        "bcc-csm1-1": 1,
        "BNU-ESM": 2,
        "CCSM4": 3,
        "GFDL-ESM2G": 4,
        "GFDL-ESM2M": 5,
        "IPSL-CM5A-LR": 6,
        "IPSL-CM5A-MR": 7,
        "MIROC5": 8,
        "MIROC-ESM": 9,
        "MIROC-ESM-CHEM": 10,
        "MRI-CGCM3": 11,
        "NorESM1-M": 12,
    },
    "scenario": {
        "historical": 0,
        "rcp26": 1,
        "rcp45": 2,
        "rcp60": 3,
        "rcp85": 4,
    },
    "era": {
        "1976_2005": 0, # historical
        "2016_2045": 1, # early century
        "2046_2075": 2, # mid century
        "2071_2100": 3, # late century
    },
}
