# script to build JSON files for Rasdaman ingest
# this script should read the attributes of the netCDF files, which will contain a dictionary of the encodings

# this ingest was used a template (minus the spatial components): https://github.com/ua-snap/rasdaman-ingest/blob/7536c17a0df2ecec18c965f030d7e943bccd2d01/iem/gipl2_4km/ingest.json

import argparse
import sys
import os
from datetime import datetime
from functions import *


def arguments(argv):
    """Parse some args"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_dir",
        type=str,
        help="directory where hydrologic stats netCDFs were saved",
        required=True,
    )

    args = parser.parse_args()
    output_dir = args.output_dir

    return output_dir


if __name__ == "__main__":

    output_dir = arguments(sys.argv)

    print(f"Opening output netCDF files in {output_dir}...\n")

    # list NC files
    try:
        seg_file = os.path.join(output_dir, "seg.nc")
        seg_ds = xr.open_dataset(seg_file)
    except:
        print(f"Error finding seg.nc in {output_dir}")
        sys.exit(1)

    try:
        hru_file = os.path.join(output_dir, "hru.nc")
        hru_ds = xr.open_dataset(hru_file)
    except:
        print(f"Error finding hru.nc in {output_dir}")
        sys.exit(1)

    print(f"Creating ingest JSON from netCDFs in {output_dir}...\n")

    # build ingest JSON files using attributes from netCDFs
    seg_ingest_json = build_ingest_json(seg_ds, "seg")
    hru_ingest_json = build_ingest_json(hru_ds, "hru")

    print("Writing ingest JSON files to {output_dir}...\n")

    # write ingest JSON files
    with open(os.path.join(output_dir, "seg_ingest.json"), "w") as f:
        f.write(seg_ingest_json)
    with open(os.path.join(output_dir, "hru_ingest.json"), "w") as f:
        f.write(hru_ingest_json)

    print("JSON files finished at ", datetime.now(), "\n")
