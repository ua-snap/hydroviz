import argparse
import sys
from pathlib import Path
import pandas as pd
from functions import *


def arguments(argv):
    """Parse some args"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, help="directory where hydrologic stats CSVs are located", required=True)
    parser.add_argument("--output_dir", type=str, help="directory where hydrologic stats netCDFs will be saved", required=True)
   
    args = parser.parse_args()
    data_dir = args.data_dir
    output_dir = args.output_dir

    return data_dir, output_dir


if __name__ == "__main__":

    data_dir, output_dir = arguments(sys.argv)

    print(f"Reading hydro stats CSVs from {data_dir}...")

    # list CSV files
    seg_files = list(Path(data_dir).glob("dynamic*seg*.csv"))
    seg_files += list(Path(data_dir).glob("static*seg*.csv"))

    hru_files = list(Path(data_dir).glob("dynamic*hru*.csv"))
    hru_files += list(Path(data_dir).glob("static*hru*.csv"))

    # filter files
    seg_files = filter_files(seg_files)
    hru_files = filter_files(hru_files)

    # get geometry IDs
    seg_ids = pd.read_csv(seg_files[0]).seg_id.astype(str).tolist()
    hru_ids = pd.read_csv(hru_files[0]).hru_id.astype(str).tolist()

    # get unique coordinates
    geom_coords_dict = {}
    geom_coords_dict["seg"] = get_unique_coords(seg_files)
    geom_coords_dict["hru"] = get_unique_coords(hru_files)

    # create empty netCDFs and populate with the data from CSVs
    Path(output_dir).mkdir(exist_ok=True, parents=True)

    print("Creating empty netCDF dataset to hold stream segment statistics...")
    seg_ds = create_empty_dataset(geom_coords_dict["seg"], seg_ids)
    print(f"Populating dataset from {len(seg_files)} stream segment statistic CSVs...")
    populate_dataset(seg_ds, seg_files)
    seg_outfile = Path(output_dir).join("seg.nc")
    print(f"Writing populated netCDF to {seg_outfile}...")
    seg_ds.to_netcdf(seg_outfile)
    del seg_ds

    print("Creating empty netCDF dataset to hold watershed statistics...")
    hru_ds = create_empty_dataset(geom_coords_dict["hru"], hru_ids)
    print(f"Populating dataset from {len(hru_files)} watershed statistic CSVs...")
    populate_dataset(hru_ds, hru_files)
    hru_outfile = Path(output_dir).join("hru.nc")
    print(f"Writing populated netCDF to {hru_outfile}...")
    hru_ds.to_netcdf(hru_outfile)
    del hru_ds


