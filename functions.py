import numpy as np
import pandas as pd
import xarray as xr
from luts import *


def filter_files(files, type):
# ignore Maurer files and the "diff" files
# also ignore the files with full historical range (1952-2005); this overlaps the
# normal historical range (1976-2005) and is confusing

# type is either "seg" or "hru": use possible filtering based on type in the future

    filtered_files = []
    starting_len = len(files)
    count = 0
    for f in files:
        if "Maurer" in f.name: 
            count = count+1
            pass
        elif "diff" in f.name:
            count = count+1
            pass
        elif "1952_2005" in f.name:
            count = count+1
            pass
        else:
            filtered_files.append(f)

    print(f"Filtered {count} files from type '{type}' list; {len(filtered_files)} files remain out of {starting_len} original files.\n")
    return filtered_files


def get_unique_coords(files):
# get unique coordinates from the file names

    lcs = []
    models = [] 
    scenarios = []
    variants = []
    eras = []

    for file in files:
        parts = file.name.split('_')
        try:
            lc, model, scenario, variant, era = parts[0], parts[1], parts[2], parts[3], "_".join([parts[5], parts[6].split(".")[0]])
        except:
            print(f"Error parsing file: {file.name}")
            continue

        lcs.append(lc)
        models.append(model)
        scenarios.append(scenario)
        variants.append(variant)
        eras.append(era)

    lcs = sorted(list(set(lcs)))
    models = sorted(list(set(models))) 
    scenarios = sorted(list(set(scenarios)))
    variants = sorted(list(set(variants)))
    eras = sorted(list(set(eras)))

    dict = {
        "lcs": lcs,
        "models": models,
        "scenarios": scenarios,
        "variants": variants,
        "eras": eras,
    }

    return dict


def create_empty_dataset(dict, geom_ids):

    stat_vars = list(stat_vars_dict.keys())

    lcs, models, scenarios, eras = dict["lcs"], dict["models"], dict["scenarios"], dict["eras"]

    # create a dict with an empty array of nan values for each stat variable
    # shape is defined by the length of all coords
    # we will fill in the nan values with actual data later, if they exists
    data_dict = {}
    for stat in stat_vars:
        data_dict[stat] = (["lc", "model", "scenario", "era", "geom_id"], 
                           np.zeros((len(lcs), len(models), len(scenarios), len(eras), len(geom_ids))) * np.nan)

    ds = xr.Dataset(data_dict, 
                    coords={
            "lc": (["lc"], encode(lcs, "lc")),
            "model": (["model"], encode(models, "model")), 
            "scenario": (["scenario"], encode(scenarios, "scenario")),
            "era": (["era"], encode(eras, "era")),
            "geom_id": (["geom_id"], geom_ids),
        },
    )

    return ds


def encode(list, type):
    # encode the list of strings based on the encodings lookup table
    # type is the type of encoding to use, e.g. "lc", "model", "scenario", "era"

    if type == "lc":
        return [encodings_lookup["lc"][x] for x in list]
    elif type == "model":
        return [encodings_lookup["model"][x] for x in list]
    elif type == "scenario":
        return [encodings_lookup["scenario"][x] for x in list]
    elif type == "era":
        return [encodings_lookup["era"][x] for x in list]


def populate_dataset(ds, files):

    stat_vars = list(stat_vars_dict.keys())

    # TODO: add a step to confirm that the CSV is the proper shape based on dataset geom_id coords
    # TODO: add a step to confirm that all stat vars from luts.py are found in CSV column names
    # TODO: add a step to confirm that the parsed coords all actually exist in the xarray dataset

    for file in files:
        # parse filename to find coords where data should go
        try:
            parts = file.name.split('_')
            lc, model, scenario, era = parts[0], parts[1], parts[2], "_".join([parts[5], parts[6].split(".")[0]])
        except:
            print(f"Error parsing file: {file.name}")
            print(f"Data will not be written to netCDF.")
            continue
        
        # only read in the columns we want, and use actual NaNs
        df = pd.read_csv(file, usecols = stat_vars)
        df.replace(-99999, np.nan, inplace=True)

        # replace the dimension strings with integers based on encodings lookup table
        lc_encoded = encodings_lookup["lc"][lc]
        model_encoded = encodings_lookup["model"][model]
        scenario_encoded = encodings_lookup["scenario"][scenario]
        era_encoded = encodings_lookup["era"][era]

        for stat in df.columns:
            try:
                ds[stat].loc[{"lc": lc_encoded, 
                              "model": model_encoded, 
                              "scenario": scenario_encoded, 
                              "era": era_encoded}] = df[stat]
            except:
                print(f"Indexing error for {stat} in {file.name}: one of {lc}, {model}, {scenario}, {era} could not be found in the dataset.")
            # drop column after use (improves performance)
            df.drop(columns=[stat], inplace=True)

    return ds


def crosswalk_hrus(ds, df):
    xwalk_dict = {k: v for k, v in zip(df['hru_id'], df['hru_id_nat'])}
    new_ids = [xwalk_dict.get(k) for k in ds['geom_id'].values.tolist()]
    ds['geom_id'] = new_ids
    return ds


def clip_dataset(ds, shp, type):
# clip the dataset to the actual data extent using geometry IDs

    if type == "seg":
        ds = ds.sel(geom_id = ds.geom_id.isin(shp.seg_id_nat.astype(str).tolist()))
        return ds
    elif type == "hru":
        ds = ds.sel(geom_id = ds.geom_id.isin(shp.hru_id_nat.astype(str).tolist()))
        return ds

#TODO: add function to write netCDF metadata from stat descriptions in luts.py and general dataset info
