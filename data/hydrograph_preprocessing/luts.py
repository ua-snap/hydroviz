# metadata for the daily climatology statistics
stat_vars_dict = {
    "doy_min" : {
        "statistic_description" : "Minimum daily streamflow for day of year across all years in era",
        "units" : "cfs",
    },
    "doy_max" : {
        "statistic_description" : "Maximum daily streamflow for day of year across all years in era",
        "units" : "cfs",
    },
    "doy_mean" : {
        "statistic_description" : "Mean daily streamflow for day of year across all years in era",
        "units" : "cfs",
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