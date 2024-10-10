import argparse
import sys
import os
from pathlib import Path
import pandas as pd
import geopandas as gpd
from datetime import datetime
from functions import *


def arguments(argv):
    """Parse some args"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, help="directory where hydrologic stats CSVs are located", required=True)
    parser.add_argument("--gis_dir", type=str, help="directory where GIS files are located", required=True)
    parser.add_argument("--output_dir", type=str, help="directory where hydrologic stats netCDFs will be saved", required=True)
   
    args = parser.parse_args()
    data_dir = args.data_dir
    gis_dir = args.gis_dir
    output_dir = args.output_dir

    return data_dir, gis_dir, output_dir


if __name__ == "__main__":

    data_dir, gis_dir, output_dir = arguments(sys.argv)

    print(f"Reading hydro stats CSVs from {data_dir}...\n")

    # list CSV files
    seg_files = list(Path(data_dir).glob("dynamic*seg*.csv"))
    seg_files += list(Path(data_dir).glob("static*seg*.csv"))

    hru_files = list(Path(data_dir).glob("dynamic*hru*.csv"))
    hru_files += list(Path(data_dir).glob("static*hru*.csv"))

    # filter files
    seg_files = filter_files(seg_files, "seg")
    hru_files = filter_files(hru_files, "hru")

    print(f"Reading GIS files from {gis_dir}...\n")

    # get seg/hru shapefiles to extract IDs
    seg_shp_path = os.path.join(gis_dir, "Segments_subset.shp")
    seg_shp = gpd.read_file(seg_shp_path)
    hru_shp_path = os.path.join(gis_dir, "HRU_subset.shp")
    hru_shp = gpd.read_file(hru_shp_path)
    # get crosswalk to fix HRU IDs
    hru_xwalk = pd.read_csv(os.path.join(gis_dir, "nhm_hru_id_crosswalk.csv"), dtype={'hru_id':str, 'hru_id_nat':str})

    print(f"Parsing geometry IDs and model / scenario / era coordinates...\n")

    # get geometry IDs
    seg_ids = pd.read_csv(seg_files[0]).seg_id.astype(int).tolist()
    hru_ids = pd.read_csv(hru_files[0]).hru_id.astype(int).tolist()

    # get unique coordinates
    geom_coords_dict = {}
    geom_coords_dict["seg"] = get_unique_coords(seg_files)
    geom_coords_dict["hru"] = get_unique_coords(hru_files)

    # create empty netCDFs and populate with the data from CSVs

    print("Creating empty netCDF dataset to hold stream segment statistics...\n")
    seg_ds = create_empty_dataset(geom_coords_dict["seg"], seg_ids)
    print(f"Populating dataset from {len(seg_files)} stream segment statistic CSVs...\n")
    seg_ds = populate_dataset(seg_ds, seg_files)
    print(f"Clipping dataset to the extent of {seg_shp_path} ...\n")
    seg_ds = clip_dataset(seg_ds, seg_shp, "seg")
    seg_outfile = os.path.join(output_dir, "seg.nc")
    print(f"Writing populated netCDF to {seg_outfile}...\n")
    seg_ds.to_netcdf(seg_outfile)
    del seg_ds

    print("Creating empty netCDF dataset to hold watershed statistics...\n")
    hru_ds = create_empty_dataset(geom_coords_dict["hru"], hru_ids)
    print(f"Populating dataset from {len(hru_files)} watershed statistic CSVs...\n")
    hru_ds = populate_dataset(hru_ds, hru_files)
    hru_ds = crosswalk_hrus(hru_ds, hru_xwalk)
    print(f"Clipping dataset to the extent of {hru_shp_path} ...\n")
    hru_ds = clip_dataset(hru_ds, hru_shp, "hru")
    hru_outfile = os.path.join(output_dir, "hru.nc")
    print(f"Writing populated netCDF to {hru_outfile}...\n")
    hru_ds.to_netcdf(hru_outfile)
    del hru_ds

    print("Processing finished at ", datetime.now())

