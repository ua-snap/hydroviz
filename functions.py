import pandas as pd
import numpy as np
import xarray as xr
from luts import era_lookup, stat_vars_dict


def filter_files(files):
# ignore Maurer files and the "diff" files
# also ignore the files with full historical range (1952-2005); this overlaps the
# normal historical range (1976-2005) and is confusing

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

    print(f"Removed {count} files from list; {len(filtered_files)} files remain out of {starting_len} original files.")
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


def create_empty_dataset(dict, stat_vars_dict, geom_ids):

    stat_vars = stat_vars_dict.keys()

    lcs, models, scenarios, eras = dict["lcs"], dict["models"], dict["scenarios"], dict["eras"]

    # build list of era strings
    eras_index = []
    for e in eras:
        eras_index.append(era_lookup[e])

    # create a dict with an empty array of nan values for each stat variable
    # shape is defined by the length of all coords
    # we will fill in the nan values with actual data later, if they exists
    data_dict = {}
    for stat in stat_vars:
        data_dict[stat] = (["lc", "model", "scenario", "era", "geom_id"], 
                           np.zeros((len(lcs), len(models), len(scenarios), len(eras_index), len(geom_ids))) * np.nan)

    ds = xr.Dataset(data_dict, 
                    coords={
            "lc": (["lc"], lcs),
            "model": (["model"], models), 
            "scenario": (["scenario"], scenarios),
            "era": (["era"], eras_index),
            "geom_id": (["geom_id"], geom_ids),
        },
    )

    return ds
