#!/usr/bin/env python3
"""
Process streamflow CSV data to generate daily climatology statistics by era.

This script converts CSV streamflow data to NetCDF format and computes daily
climatologies (min, mean, max) for three future projection eras:
2016-2045, 2046-2075, and 2071-2100. These eras are defined by water years
(October 1 through September 30) and match those used to aggregate
statistics in this dataset: https://doi.org/10.5066/P9EBKREQ.
The input data format is assumed to be consistent with the daily streamflow 
outputs from that same dataset.

Example usage:
--------------
python process_streamflow_climatology.py \
    input_streamflow.csv \  # Input CSV file path
    output_climatology.nc \  # Output NetCDF file path
    /path/to/temp_dir \      # Temporary directory for intermediate files
    --keep-intermediate \    # Optional flag to keep intermediate files
    --chunk-size 2000 \     # Optional chunk size for processing
    --stream-chunk-size 10000 # Optional stream chunk size for climatology calculation
--------------

"""

import os
import sys
import argparse
import tempfile
from pathlib import Path
import pyarrow.csv as csv
import pyarrow.parquet as pq
import xarray as xr
import pandas as pd
import numpy as np


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Process streamflow CSV to NetCDF climatology",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "input_csv",
        type=str,
        help="Path to input CSV file containing streamflow data"
    )
    
    parser.add_argument(
        "output_netcdf",
        type=str,
        help="Path for output NetCDF file with climatology data"
    )
    
    parser.add_argument(
        "temp_dir",
        type=str,
        help="Directory path for temporary intermediate files"
    )
    
    parser.add_argument(
        "--keep-intermediate",
        action="store_true",
        help="Keep intermediate files (parquet and full NetCDF)"
    )
    
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=2000,
        help="Chunk size for processing streamflow columns"
    )
    
    parser.add_argument(
        "--stream-chunk-size",
        type=int,
        default=10000,
        help="Number of streams to process at once for climatology calculation"
    )
    
    return parser.parse_args()


def csv_to_parquet(csv_path, parquet_path):
    """Convert CSV file to Parquet format."""
    read_opts = csv.ReadOptions(block_size=1 << 30)  # 1 GB chunks
    
    convert_opts = csv.ConvertOptions(
        strings_can_be_null=True,
        null_values=["", "NA", "NaN"]
    )
    
    table = csv.read_csv(
        csv_path,
        read_options=read_opts,
        convert_options=convert_opts
    )
    
    pq.write_table(table, parquet_path, compression="zstd")
    return table


def get_landcover_model_rcp_from_filename(filename):
    """Extract landcover and model information from filename.
    Filename is in format: <landcover>_<model>_<rcp>_...csv"""
    lower_name = filename.lower()

    landcover = "unknown"
    model = "unknown"
    rcp = "unknown"

    try:
        landcover = lower_name.split("_")[0]
    except IndexError:
        pass
    try:
        model = lower_name.split("_")[1]
    except IndexError:
        pass
    try:
        rcp = lower_name.split("_")[2]
    except IndexError:
        pass

    return landcover, model, rcp


def parquet_to_xarray(parquet_path, landcover, model, rcp, chunk_size=2000):
    """Convert Parquet file to xarray Dataset."""
    # Read the Parquet file
    df = pd.read_parquet(parquet_path)
    
    # Make sure Date is datetime
    df["Date"] = pd.to_datetime(df["Date"])
    
    # List of streamflow columns (all except Date)
    flow_cols = [c for c in df.columns if c != "Date"]
    
    # Convert to dataset, processing in chunks to reduce memory usage
    arrays = []
    stream_ids = []
    
    for i in range(0, len(flow_cols), chunk_size):
        cols_chunk = flow_cols[i:i+chunk_size]
        arrays.append(df[cols_chunk].astype("float32").values)
        stream_ids.extend([int(c) for c in cols_chunk])
    
    arr = np.hstack(arrays)  # stack all chunks along columns
    
    ds = xr.Dataset(
        {
            "streamflow": (("time", "stream_id"), arr)
        },
        coords={
            "time": df["Date"].values,
            "stream_id": stream_ids
        }
    )

    # add landcover, model, and rcp as dimensions with length 1
    # this allows us to combine together later if needed
    # allow for variable length strings, using dtype=object
    ds = ds.expand_dims({"landcover": [landcover], "model": [model], "scenario": [rcp]})
    ds["landcover"] = ds["landcover"].astype(object)
    ds["model"] = ds["model"].astype(object)
    ds["scenario"] = ds["scenario"].astype(object)
    
    return ds


def compute_climatology(ds, stream_chunk_size=10000, filename=""):
    """Compute daily climatology statistics by era."""
    # Add day-of-year coordinate
    ds = ds.assign_coords(doy=ds["time"].dt.dayofyear)

    # Define eras based on filename
    if "historical" in filename.lower():
        # Use historical era only
        eras = [("1976-10-01", "2005-09-30")]
    else:
        # Use projection eras
        eras = [
            ("2016-10-01", "2045-09-30"),
            ("2046-10-01", "2075-09-30"),
            ("2071-10-01", "2100-09-30"),
        ]
    
    # Process in smaller chunks to reduce memory usage
    n_streams = len(ds.stream_id)
    era_clims = {}
    
    for start_date, end_date in eras:
        era = ds.sel(time=slice(start_date, end_date))
        
        # Initialize lists to store results
        doy_mins, doy_means, doy_maxs = [], [], []
        
        # Process streams in chunks
        for i in range(0, n_streams, stream_chunk_size):
            end_idx = min(i + stream_chunk_size, n_streams)
            stream_chunk = era.isel(stream_id=slice(i, end_idx))
            
            # Compute climatologies for this chunk
            chunk_doy_min = stream_chunk.groupby("doy").min("time")
            chunk_doy_mean = stream_chunk.groupby("doy").mean("time")
            chunk_doy_max = stream_chunk.groupby("doy").max("time")
            
            doy_mins.append(chunk_doy_min["streamflow"])
            doy_means.append(chunk_doy_mean["streamflow"])
            doy_maxs.append(chunk_doy_max["streamflow"])
        
        # Concatenate all chunks
        era_doy_min = xr.concat(doy_mins, dim="stream_id")
        era_doy_mean = xr.concat(doy_means, dim="stream_id")
        era_doy_max = xr.concat(doy_maxs, dim="stream_id")
        
        daily_clim = xr.Dataset(
            {
                "doy_min": era_doy_min,
                "doy_mean": era_doy_mean,
                "doy_max": era_doy_max,
            },
            coords={
                "doy": era_doy_mean["doy"],
                "stream_id": era_doy_mean["stream_id"],
            }
        )
        era_clims[f"{start_date[:4]}-{end_date[:4]}"] = daily_clim
    
    # Combine into a single dataset with an 'era' dimension
    combined_clims = xr.concat(
        [era_clims[era] for era in era_clims],
        dim=pd.Index(list(era_clims.keys()), name="era")
    )
    
    return combined_clims


def cleanup_files(file_paths, keep_files=False):
    """Remove intermediate files and directories unless keep_files is True."""
    if keep_files:
        return
    
    for file_path in file_paths:
        try:
            path = Path(file_path)
            if path.exists():
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    import shutil
                    shutil.rmtree(path)
        except Exception:
            pass  # Ignore cleanup errors


def main():
    """Main processing function."""
    args = parse_arguments()
    
    # Validate input file exists
    if not os.path.exists(args.input_csv):
        print(f"Error: Input CSV file not found: {args.input_csv}", file=sys.stderr)
        sys.exit(1)
    
    # Create temp directory if it doesn't exist
    temp_dir = Path(args.temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Create output directory if it doesn't exist
    output_dir = Path(args.output_netcdf).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate intermediate file names
    csv_name = Path(args.input_csv).stem
    parquet_path = temp_dir / f"{csv_name}.parquet"
    netcdf_temp_path = temp_dir / f"{csv_name}.nc"
    
    # File-specific temp directory
    file_temp_dir = temp_dir / csv_name
    
    intermediate_files = [str(parquet_path), str(netcdf_temp_path)]
    
    try:
        # Step 1: Convert CSV to Parquet
        table = csv_to_parquet(args.input_csv, parquet_path)
        
        # Step 2: Convert Parquet to xarray Dataset
        landcover, model, rcp = get_landcover_model_rcp_from_filename(args.input_csv)
        ds = parquet_to_xarray(parquet_path, landcover, model, rcp, args.chunk_size)
        
        # Step 3: Save intermediate NetCDF file
        ds.to_netcdf(netcdf_temp_path)
        
        # Clear memory
        del ds, table
        
        # Step 4: Reload and compute climatology
        ds = xr.open_dataset(netcdf_temp_path)
        combined_clims = compute_climatology(ds, args.stream_chunk_size, args.input_csv)
        
        # Step 5: Save final climatology NetCDF
        combined_clims.to_netcdf(args.output_netcdf)
        
        # Clear memory
        del ds, combined_clims
        
        # Step 6: Cleanup intermediate files if requested
        cleanup_files(intermediate_files + [str(file_temp_dir)], args.keep_intermediate)
        
        print(f"Successfully processed {args.input_csv} -> {args.output_netcdf}")
        
    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        # Cleanup on error
        cleanup_files(intermediate_files + [str(file_temp_dir)], keep_files=False)
        sys.exit(1)


if __name__ == "__main__":
    main()