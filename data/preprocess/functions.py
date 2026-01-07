import numpy as np
import pandas as pd
import xarray as xr
from luts import *


def filter_files(files, type):
    # ignore the files with long historical range (1952-2005 and 1952-2010); this overlaps the
    # normal historical range (1976-2005) and is confusing
    # type is either "seg" or "hru": use possible filtering based on type in the future

    filtered_files = []
    starting_len = len(files)
    count = 0
    for f in files:
        if "diff" in f.name:
            count = count + 1
            pass
        elif "1952_2005" in f.name:
            count = count + 1
            pass
        elif "1952_2010" in f.name:
            count = count + 1
            pass
        else:
            filtered_files.append(f)

    print(
        f"Filtered {count} files from type '{type}' list; {len(filtered_files)} files remain out of {starting_len} original files.\n"
    )
    return filtered_files


def get_unique_coords(files):
    # get unique coordinates from the file names

    landcovers = []
    models = []
    scenarios = []
    variants = []
    eras = []

    for file in files:
        parts = file.name.split("_")
        try:
            landcover, model, scenario, variant, era = (
                parts[0],
                parts[1],
                parts[2],
                parts[3],
                "_".join([parts[5], parts[6].split(".")[0]]),
            )
        except:
            print(f"Error parsing file: {file.name}")
            continue

        landcovers.append(landcover)
        models.append(model)
        scenarios.append(scenario)
        variants.append(variant)
        eras.append(era)

    landcovers = sorted(list(set(landcovers)))
    models = sorted(list(set(models)))
    scenarios = sorted(list(set(scenarios)))
    variants = sorted(list(set(variants)))
    eras = sorted(list(set(eras)))

    dict = {
        "landcovers": landcovers,
        "models": models,
        "scenarios": scenarios,
        "variants": variants,
        "eras": eras,
    }

    return dict


def create_empty_dataset(dict, stream_ids):

    stat_vars = list(stat_vars_dict.keys())

    landcovers, models, scenarios, eras = (
        dict["landcovers"],
        dict["models"],
        dict["scenarios"],
        dict["eras"],
    )

    # create a dict with an empty array of nan values for each stat variable
    # shape is defined by the length of all coords
    # we will fill in the nan values with actual data later, if they exists
    data_dict = {}
    for stat in stat_vars:
        data_dict[stat] = (
            ["landcover", "model", "scenario", "era", "stream_id"],
            np.zeros((len(landcovers), len(models), len(scenarios), len(eras), len(stream_ids)))
            * np.nan,
        )

    ds = xr.Dataset(
        data_dict,
        coords={
            "landcover": (["landcover"], encode(landcovers, "landcover")),
            "model": (["model"], encode(models, "model")),
            "scenario": (["scenario"], encode(scenarios, "scenario")),
            "era": (["era"], encode(eras, "era")),
            "stream_id": (["stream_id"], stream_ids),
        },
    )

    return ds


def encode(list, type):
    # encode the list of strings based on the encodings lookup table
    # type is the type of encoding to use, e.g. "landcover", "model", "scenario", "era"

    if type == "landcover":
        return [encodings_lookup["landcover"][x] for x in list]
    elif type == "model":
        return [encodings_lookup["model"][x] for x in list]
    elif type == "scenario":
        return [encodings_lookup["scenario"][x] for x in list]
    elif type == "era":
        return [encodings_lookup["era"][x] for x in list]


def populate_dataset(ds, files):

    stat_vars = list(stat_vars_dict.keys())

    for file in files:
        # parse filename to find coords where data should go
        try:
            parts = file.name.split("_")
            landcover, model, scenario, era = (
                parts[0],
                parts[1],
                parts[2],
                "_".join([parts[5], parts[6].split(".")[0]]),
            )
        except:
            print(f"Error parsing file: {file.name}")
            print(f"Data will not be written to netCDF.")
            continue

        # only read in the columns we want, and use actual NaNs
        # this allows for missing columns in the CSV
        df = pd.read_csv(file, usecols=lambda c: c in stat_vars)
        df.replace(-99999, np.nan, inplace=True)

        # test for missing columns and add them (filled with NaNs) if they are missing
        for stat in stat_vars:
            if stat not in df.columns:
                df[stat] = np.nan

        # test that the dataframe length matches the length of the stream_ids in the dataset
        if len(df) != len(ds["stream_id"]):
            print(
                f"Error: length of CSV does not match length of stream_ids in dataset for {file.name}."
            )
            print(f"Data will not be written to netCDF.")
            continue

        # replace the dimension strings with integers based on encodings lookup table
        # this will also confirm that the parsed coords are valid and actually exist in encodings lookup table
        try:
            landcover_encoded = encodings_lookup["landcover"][landcover]
            model_encoded = encodings_lookup["model"][model]
            scenario_encoded = encodings_lookup["scenario"][scenario]
            era_encoded = encodings_lookup["era"][era]
        except:
            print(f"Error: one of {landcover}, {model}, {scenario}, {era} are invalid.")
            print(f"Data will not be written to netCDF.")
            continue

        for stat in df.columns:
            try:
                ds[stat].loc[
                    {
                        "landcover": landcover_encoded,
                        "model": model_encoded,
                        "scenario": scenario_encoded,
                        "era": era_encoded,
                    }
                ] = df[stat]
            except:
                print(
                    f"Indexing error for {stat} in {file.name}: one of {landcover}, {model}, {scenario}, {era} could not be found in the dataset."
                )
                print(f"Data will not be written to netCDF.")
                continue

            # drop column after use (improves performance)
            df.drop(columns=[stat], inplace=True)

        # use luts dicts to add global metadata to the dataset; for serialization during file writing, each item needs to be a string or list, can't be a dict
        ds = ds.assign_attrs(
            {
                "Data Source": str(data_source_dict),
                "CMIP5 GCM Metadata": str(gcm_metadata_dict),
            }
        )

    return ds


def populate_encodings_metadata(ds):
    # for each dimension, add the encoding lookup dict from reverse_encodings_lookup
    # e.g., for "model", add reverse_encodings_lookup["model"] as metadata under the "encodings" attribute for that dimension
    # NOTE: some model names were capitalized in the metadata for consistency; see luts.py for details
    # NOTE: era names were hyphenated in the metadata for consistency; see luts.py for details
    for dim in ["landcover", "model", "scenario", "era"]:
        ds[dim].attrs["encoding"] = str(reverse_encodings_lookup[dim])
    
    # for each variable, add the statistic metadata from stat_vars_dict
    for var in stat_vars_dict.keys():
        ds[var].attrs["description"] = stat_vars_dict[var]["statistic_description"]
        ds[var].attrs["units"] = stat_vars_dict[var]["units"]
    return ds

def sort_by_model_dimension(ds):
    # sort the model dimension: they are all integer values, but we need to ensure they are in order before writing to netCDF
    sorted_models = sorted(ds["model"].values.tolist())
    ds = ds.sel(model=sorted_models)
    return ds

def convert_to_float32(ds):
    # convert all data variables and dimensions to float32 to save space
    for var in ds.data_vars:
        ds[var] = ds[var].astype(np.float32)
    for dim in ["landcover", "model", "scenario", "era"]:
        ds[dim] = ds[dim].astype(np.float32)
    # assert stream_id is int32
    ds["stream_id"] = ds["stream_id"].astype(np.int32)
    return ds


def crosswalk_hrus(ds, df):
    xwalk_dict = {k: v for k, v in zip(df["hru_id"], df["hru_id_nat"])}
    new_ids = [xwalk_dict.get(k) for k in ds["stream_id"].values.tolist()]
    ds["stream_id"] = new_ids
    return ds


def clip_dataset(ds, shp, type):
    # clip the dataset to the actual data extent using geometry IDs

    if type == "seg":
        ds = ds.sel(stream_id=ds.stream_id.isin(shp.seg_id_nat.astype(str).tolist()))
        return ds
    elif type == "hru":
        ds = ds.sel(stream_id=ds.stream_id.isin(shp.hru_id_nat.astype(str).tolist()))
        return ds