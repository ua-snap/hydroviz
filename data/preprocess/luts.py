
# metadata for the summary statistics
# the keys of this dict also serve to filter the columns read from the statistics CSVs in functions.populate_dataset()
# therefore, commenting out keys in this dict will prevent those statistics from being read into the netCDFs
stat_vars_dict = {
    "dh1": {
        "category": "duration",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Annual maximum daily flow. Compute the maximum of a 1-day moving average flow for each year. DH1 is the median of these values (cubic feet per second - temporal).",
        "units": "cfs",
    },
    "dh2": {
        "category": "duration",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Annual maximum of 3-day moving average flows. Compute the maximum of a 3-day moving average flow for each year. DH2 is the median of these values (cubic feet per second - temporal).",
        "units": "cfs",
    },
    "dh3": {
        "category": "duration",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Annual maximum of 7-day moving average flows. Compute the maximum of a 7-day moving average flow for each year. DH3 is the median of these values (cubic feet per second - temporal).",
        "units": "cfs",
    },
    "dh4": {
        "category": "duration",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Annual maximum of 30-day moving average flows. Compute the maximum of 30-day moving average flows. Compute the maximum of a 30-day moving average flow for each year. DH4 is the median of these values (cubic feet per second - temporal).",
        "units": "cfs",
    },
    "dh5": {
        "category": "duration",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Annual maximum of 90-day moving average flows. Compute the maximum of a 90-day moving average flow for each year. DH5 is the median of these values (cubic feet per second - temporal).",
        "units": "cfs",
    },
    "dh15": {
        "category": "duration",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "High flow pulse duration. Compute the average duration for flow events with flows above a threshold equal to the 75th percentile value for each year in the flow record. DH15 is the median of the yearly average durations (days/year - temporal).",
        "units": "days/year",
    },
    "dl1": {
        "category": "duration",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Annual minimum daily flow. Compute the minimum 1-day average flow for each year. DL1 is the median of these values (cubic feet per second - temporal).",
        "units": "cfs",
    },
    "dl2": {
        "category": "duration",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Annual minimum of 3-day moving average flow. Compute the minimum of a 3-day moving average flow for each year. DL2 is the median of these values (cubic feet per second - temporal).",
        "units": "cfs",
    },
    "dl3": {
        "category": "duration",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Annual minimum of 7-day moving average flow. Compute the minimum of a 7-day moving average flow for each year. DL3 is the median of these values (cubic feet per second - temporal).",
        "units": "cfs",
    },
    "dl4": {
        "category": "duration",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Annual minimum of 30-day moving average flow. Compute the minimum of a 30-day moving average flow for each year. DL4 is the median of these values (cubic feet per second - temporal).",
        "units": "cfs",
    },
    "dl5": {
        "category": "duration",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Annual minimum of 90-day moving average flow. Compute the minimum of a 90-day moving average flow for each year. DL5 is the median of these values (cubic feet per second - temporal).",
        "units": "cfs",
    },
    "dl16": {
        "category": "duration",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Low flow pulse duration. Compute the average pulse duration for each year for flow events below a threshold equal to the 25th percentile value for the entire flow record. DL16 is the median of the yearly average durations (days/year - temporal).",
        "units": "days/year",
    },
    "lf1": {
        "category": "duration",
        "code_base": "matlab",
        "difference_method": "absolute",
        "statistic_description": "Number of days per year below a threshold of 0.1 cubic feet per second per square mile. LF1 is the median annual number of days below the threshold (number of days/year - temporal).",
        "units": "days/year",
    },
    "spr_dur3": {
        "category": "duration",
        "code_base": "matlab",
        "difference_method": "ratio",
        "statistic_description": "Spring (April-June) maximum of 3-day moving average flows. Compute the maximum of a 3-day moving average flow for each year. SPR_DUR3 is the median of these values (cubic feet per second - temporal).",
        "units": "cfs",
    },
    "spr_dur7": {
        "category": "duration",
        "code_base": "matlab",
        "difference_method": "ratio",
        "statistic_description": "Spring (April-June) maximum of 7-day moving average flows. Compute the maximum of a 7-day moving average flow for each year. SPR_DUR7 is the median of these values (cubic feet per second - temporal).",
        "units": "cfs",
    },
    "sum_dur3": {
        "category": "duration",
        "code_base": "matlab",
        "difference_method": "ratio",
        "statistic_description": "Summer (July-September) minimum of 3-day moving average flow. Compute the minimum of a 3-day moving average flow for each year. SUM_DUR3 is the median of these values (cubic feet per second - temporal).",
        "units": "cfs",
    },
    "sum_dur7": {
        "category": "duration",
        "code_base": "matlab",
        "difference_method": "ratio",
        "statistic_description": "Summer (July-September) minimum of 7-day moving average flow. Compute the minimum of a 7-day moving average flow for each year. SUM_DUR7 is the median of these values (cubic feet per second - temporal).",
        "units": "cfs",
    },
    "fh1": {
        "category": "frequency",
        "code_base": "mhit",
        "difference_method": "absolute",
        "statistic_description": "High flood pulse count. Compute the average number of flow events with flows above a threshold equal to the 75th percentile value for the entire flow record. FH1 is the median number of events (number of events/year - temporal).",
        "units": "events/year",
    },
    "fh5": {
        "category": "frequency",
        "code_base": "mhit",
        "difference_method": "absolute",
        "statistic_description": "Flood frequency. Compute the average number of flow events with flows above a threshold equal to the median flow value for the entire flow record. FH5 is the median number of events (number of events/year - temporal).",
        "units": "events/year",
    },
    "fh6": {
        "category": "frequency",
        "code_base": "mhit",
        "difference_method": "absolute",
        "statistic_description": "Flood frequency. Compute the average number of flow events with flows above a threshold equal to three times the median flow value for the entire flow record. FH6 is the median number of events (number of events/year - temporal).",
        "units": "events/year",
    },
    "fh7": {
        "category": "frequency",
        "code_base": "mhit",
        "difference_method": "absolute",
        "statistic_description": "Flood frequency. Compute the average number of flow events with flows above a threshold equal to seven times the median flow value for the entire flow record. FH7 is the median number of events (number of events/year - temporal).",
        "units": "events/year",
    },
    "fl1": {
        "category": "frequency",
        "code_base": "mhit",
        "difference_method": "absolute",
        "statistic_description": "Low flood pulse count. Compute the average number of flow events with flows below a threshold equal to the 25th percentile value for the entire flow record. FL1 is the median number of events (number of events/year - temporal).",
        "units": "events/year",
    },
    "fl3": {
        "category": "frequency",
        "code_base": "mhit",
        "difference_method": "absolute",
        "statistic_description": "Frequency of low pulse spells. Compute the average number of flow events with flows below a threshold equal to 5 percent of the mean flow value for the entire flow record. FL3 is the median number of events (number of events/year - temporal).",
        "units": "events/year",
    },
    "spr_freq": {
        "category": "frequency",
        "code_base": "matlab",
        "difference_method": "absolute",
        "statistic_description": "Flood frequency for April-June. Compute the average number of flow events with flows above a threshold equal to the 10th percentile for the entire flow record. SPR_FREQ is the median number of events (number of events/year - temporal).",
        "units": "events/year",
    },
    "sum_freq": {
        "category": "frequency",
        "code_base": "matlab",
        "difference_method": "absolute",
        "statistic_description": "Flood frequency for July-September. Compute the average number of flow events with flows below a threshold equal to the 90th percentile for the entire flow record. SUM_FREQ is the median number of events (number of events/year - temporal).",
        "units": "events/year",
    },
    "ma3": {
        "category": "magnitude",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Coefficient of variation (standard deviation/mean) for each year. Compute the coefficient of variation for each year of daily flows. Compute the median of the annual coefficients of variation (percent - temporal).",
        "units": "percent",
    },
    "ma4": {
        "category": "magnitude",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Standard deviation of the percentiles of the logs of the entire flow record divided by the mean of percentiles of the logs. Compute the log10 of the daily flows for the entire record. Compute the 5th, 10th, 15th, 20th, 25th, 30th, 35th, 40th, 45th, 50th, 55th, 60th, 65th, 70th, 75th, 80th, 85th, 90th, and 95th percentiles for the logs of the entire flow record. Percentiles are computed by interpolating between the ordered (ascending) logs of the flow values. Compute the standard deviation and mean for the percentile values. Divide the standard deviation by the mean (percent - spatial).",
        "units": "percent",
    },
    "ma12": {
        "category": "magnitude",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Mean of monthly flow values for January.",
        "units": "cfs",
    },
    "ma13": {
        "category": "magnitude",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Mean of monthly flow values for February.",
        "units": "cfs",
    },
    "ma14": {
        "category": "magnitude",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Mean of monthly flow values for March.",
        "units": "cfs",
    },
    "ma15": {
        "category": "magnitude",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Mean of monthly flow values for April.",
        "units": "cfs",
    },
    "ma16": {
        "category": "magnitude",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Mean of monthly flow values for May.",
        "units": "cfs",
    },
    "ma17": {
        "category": "magnitude",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Mean of monthly flow values for June.",
        "units": "cfs",
    },
    "ma18": {
        "category": "magnitude",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Mean of monthly flow values for July.",
        "units": "cfs",
    },
    "ma19": {
        "category": "magnitude",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Mean of monthly flow values for August.",
        "units": "cfs",
    },
    "ma20": {
        "category": "magnitude",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Mean of monthly flow values for September.",
        "units": "cfs",
    },
    "ma21": {
        "category": "magnitude",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Mean of monthly flow values for October.",
        "units": "cfs",
    },
    "ma22": {
        "category": "magnitude",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Mean of monthly flow values for November.",
        "units": "cfs",
    },
    "ma23": {
        "category": "magnitude",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Mean of monthly flow values for December.",
        "units": "cfs",
    },
    "mh14": {
        "category": "magnitude",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Median of annual maximum flows. Compute the annual maximum flows from monthly maximum flows. Compute the ratio of annual maximum flow to median annual flow for each year. MH14 is the median of these ratios (dimensionless - temporal).",
        "units": "dimensionless",
    },
    "mh20": {
        "category": "magnitude",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Specific mean annual maximum flow. MH20 is the median of the annual maximum flows divided by the drainage area (cubic feet per second/square mile - temporal).",
        "units": "cfs/square_mile",
    },
    "ml17": {
        "category": "magnitude",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Base flow. Compute the mean annual flows. Compute the minimum of a 7-day moving average flow for each year and divide them by the mean annual flow for that year. ML17 is the median of those ratios (dimensionless - temporal).",
        "units": "dimensionless",
    },
    "spr_mag": {
        "category": "magnitude",
        "code_base": "matlab",
        "difference_method": "ratio",
        "statistic_description": "Specific mean spring (April-June) maximum flow. MH20 is the median of the annual maximum flows divided by the drainage area (cubic feet per second/square mile - temporal).",
        "units": "cfs/square_mile",
    },
    "sum_cv": {
        "category": "magnitude",
        "code_base": "matlab",
        "difference_method": "ratio",
        "statistic_description": "Coefficient of variation (standard deviation/mean) for each year for the summer (July-September). Compute the coefficient of variation for each year of daily flows. Compute the median of the annual coefficients of variation (percent - temporal).",
        "units": "percent",
    },
    "sum_mag": {
        "category": "magnitude",
        "code_base": "matlab",
        "difference_method": "ratio",
        "statistic_description": "Minimum of the summer (July-September) flows divided by the drainage area (cubic feet per second/square mile - temporal).",
        "units": "cfs/square_mile",
    },
    "ra1": {
        "category": "rate_of_change",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Rise rate. Compute the change in flow for days in which the change is positive for the entire flow record. RA1 is the median of these values (cubic feet per second/day - temporal).",
        "units": "cfs/day",
    },
    "ra3": {
        "category": "rate_of_change",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Fall rate. Compute the change in flow for days in which the change is negative for the entire flow record. RA3 is the median of these values (cubic feet per second/day - temporal).",
        "units": "cfs/day",
    },
    "ra9": {
        "category": "rate_of_change",
        "code_base": "mhit",
        "difference_method": "ratio",
        "statistic_description": "Number of reversals. Compute the number of days in each year when the change in flow from one day to the next changes direction. RA8 is the median of the yearly values (days - temporal).",
        "units": "days/year",
    },
    "spr_ord": {
        "category": "timing",
        "code_base": "matlab",
        "difference_method": "absolute",
        "statistic_description": "Julian date of spring (April-June) maximum. Determine the Julian date that the maximum flow occurs for each year. SPR_ORD is the median of these values (Julian day - temporal).",
        "units": "day",
    },
    "sum_ord": {
        "category": "timing",
        "code_base": "matlab",
        "difference_method": "absolute",
        "statistic_description": "Julian date of summer (July-September) minimum. Determine the Julian date that the minimum flow occurs for each water year. SUM_ORD is the median of these values (Julian day - temporal).",
        "units": "day",
    },
    "th1": {
        "category": "timing",
        "code_base": "mhit",
        "difference_method": "absolute",
        "statistic_description": "Julian date of annual maximum. Determine the Julian date that the maximum flow occurs for each year. TH1 is the median of these values (Julian day - temporal).",
        "units": "day",
    },
    "tl1": {
        "category": "timing",
        "code_base": "mhit",
        "difference_method": "absolute",
        "statistic_description": "Julian date of annual minimum. Determine the Julian date that the minimum flow occurs for each water year. TL1 is the median of these values (Julian day - temporal).",
        "units": "day",
    },
}


# encodings for netCDF, integers required for rasdaman ingest
encodings_lookup = {
    "landcover": {
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
        "Maurer": 8,
        "MIROC5": 9,
        "MIROC-ESM": 10,
        "MIROC-ESM-CHEM": 11,
        "MRI-CGCM3": 12,
        "NorESM1-M": 13,
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


# reverse encodings for netCDF attributes
reverse_encodings_lookup = {
    "landcover": {
        0: "dynamic",
        1: "static",
    },
    "model": {
        0: "ACCESS1-0",
        1: "bcc-csm1-1",
        2: "BNU-ESM",
        3: "CCSM4",
        4: "GFDL-ESM2G",
        5: "GFDL-ESM2M",
        6: "IPSL-CM5A-LR",
        7: "IPSL-CM5A-MR",
        8: "Maurer",
        9: "MIROC5",
        10: "MIROC-ESM",
        11: "MIROC-ESM-CHEM",
        12: "MRI-CGCM3",
        13: "NorESM1-M",
    },
    "scenario": {
        0: "historical",
        1: "rcp26",
        2: "rcp45",
        3: "rcp60",
        4: "rcp85",
    },
    "era": {
        0: "1976_2005", # historical
        1: "2016_2045", # early century
        2: "2046_2075", # mid century
        3: "2071_2100", # late century
    },
}


# information about the dataset itself
data_source_dict = {"Title":"Model Input and Output for Hydrologic Simulations for the Conterminous United States for Historical and Future Conditions Using the National Hydrologic Model Infrastructure (NHMI) and the Coupled Model Intercomparison Project Phase 5 (CMIP5), 1950 - 2100",
                    "URL":"https://doi.org/10.5066/P9EBKREQ",
                    "Description":"This data release contains inputs for and outputs from hydrologic simulations for the conterminous United States (CONUS) using the Precipitation Runoff Modeling System (PRMS) version 5.1.0 (https://www.usgs.gov/software/precipitation-runoff-modeling-system-prms) and the USGS National Hydrologic Model Infrastructure (NHMI, Regan and others, 2018). These simulations were developed to provide estimates of the water budget and statistics of streamflow for historical and potential future conditions using atmospheric forcing data from Coupled Model Intercomparison Project phase 5 (CMIP5). Specific file types include: 1) input forcings of minimum air temperature, maximum air temperature, and daily precipitation derived from general circulation models (GCM, table1_GCMs_used.csv), 2) output files of simulated streamflow for each stream segment in the model, 3) GIS files of the model hydrologic response units and stream segments, and 4) a suite of streamflow statistics for each modeled segment. This data release complements data release (https://doi.org/10.5066/P9CVHLMB) which contains historical simulations based on historically observed atmospheric forcings rather than GCM-derived forcings. The same parameter files and model configuration files were used for all model runs and are available in that data release.",
                    "Authors":"Jacob H LaFontaine, Jeffrey W Riley",
                    "Date":"2023-08-23",
                    "Citation":"LaFontaine, J.H., and Riley, J.W., 2023, Model Input and Output for Hydrologic Simulations for the Conterminous United States for Historical and Future Conditions Using the National Hydrologic Model Infrastructure (NHM) and the Coupled Model Intercomparison Project Phase 5 (CMIP5), 1950 - 2100: U.S. Geological Survey data release, https://doi.org/10.5066/P9EBKREQ."}


# metadata about CMIP5 GCMs and scenarios modeled
gcm_metadata_dict = {"ACCESS1-0":
                     {"Modeling Center": "Commonwealth Scientific and Industrial Research Organization and Bureau of Meteorology, Australia",
                      "Representative Concentration Pathways": ["historical", "rcp4.5", "rcp8.5"]},
                    "bcc-csm1-1":
                        {"Modeling Center": "Beijing Climate Center, China Meteorological Adminstration, China",
                        "Representative Concentration Pathways": ["historical", "rcp2.6", "rcp4.5", "rcp6.0", "rcp8.5"]},
                    "BNU-ESM":
                        {"Modeling Center": "College of Global Change and Earth System Science, Beijing Normal University, China",
                        "Representative Concentration Pathways": ["historical", "rcp4.5", "rcp8.5"]},
                    "CCSM4":
                        {"Modeling Center": "National Center for Atmospheric Research, USA",
                        "Representative Concentration Pathways": ["historical", "rcp2.6", "rcp4.5", "rcp6.0", "rcp8.5"]},
                    "GFDL-ESM2G":
                        {"Modeling Center": "National Oceanic and Atmospheric Administration Gephysical Fluid Dynamics Laboratory, USA",
                        "Representative Concentration Pathways": ["historical", "rcp2.6", "rcp4.5", "rcp6.0", "rcp8.5"]},
                    "GFDL-ESM2M":
                        {"Modeling Center": "National Oceanic and Atmospheric Administration Gephysical Fluid Dynamics Laboratory, USA",
                        "Representative Concentration Pathways": ["historical", "rcp2.6", "rcp4.5", "rcp6.0", "rcp8.5"]},
                    "IPSL-CM5A-LR":
                        {"Modeling Center": "Institut Pierre-Simon Laplace, France",
                        "Representative Concentration Pathways": ["historical", "rcp2.6", "rcp4.5", "rcp6.0", "rcp8.5"]},
                    "IPSL-CM5A-MR":
                        {"Modeling Center": "Institut Pierre-Simon Laplace, France",
                        "Representative Concentration Pathways": ["historical", "rcp2.6", "rcp4.5", "rcp6.0", "rcp8.5"]},
                    "Maurer":{"Modeling Center": "U.S. Geological Survey",
                        "Representative Concentration Pathways": ["historical"]},
                    "MIROC5":
                        {"Modeling Center": "Japan Agency for Marine-Earth Science and Technology, Atmospheric and Ocean Research Institute (The University of Tokyo), and National Institute for Environmental Studies, Japan",
                        "Representative Concentration Pathways": ["historical", "rcp2.6", "rcp4.5", "rcp6.0", "rcp8.5"]},
                    "MIROC-ESM":
                        {"Modeling Center": "Japan Agency for Marine-Earth Science and Technology, Atmospheric and Ocean Research Institute (The University of Tokyo), and National Institute for Environmental Studies, Japan",
                        "Representative Concentration Pathways": ["historical", "rcp2.6", "rcp4.5", "rcp6.0", "rcp8.5"]},
                    "MIROC-ESM-CHEM":
                        {"Modeling Center": "Japan Agency for Marine-Earth Science and Technology, Atmospheric and Ocean Research Institute (The University of Tokyo), and National Institute for Environmental Studies, Japan",
                        "Representative Concentration Pathways": ["historical", "rcp2.6", "rcp4.5", "rcp6.0", "rcp8.5"]},
                    "MRI-CGCM3":
                        {"Modeling Center": "Meteorological Research Institute, Japan",
                        "Representative Concentration Pathways": ["historical", "rcp2.6", "rcp4.5", "rcp6.0", "rcp8.5"]},
                    "NorESM1-M":
                        {"Modeling Center": "Norwegian Climate Centre, Norway",
                        "Representative Concentration Pathways": ["historical", "rcp2.6", "rcp4.5", "rcp6.0", "rcp8.5"]},
                    }