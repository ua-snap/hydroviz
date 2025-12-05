# script to build JSON files for Rasdaman ingest
# this script should read the attributes of the netCDF files, which will contain a dictionary of the encodings

# this ingest was used a template (minus the spatial components): https://github.com/ua-snap/rasdaman-ingest/blob/7536c17a0df2ecec18c965f030d7e943bccd2d01/iem/gipl2_4km/ingest.json

import argparse
import sys
import os
import json
import xarray as xr
from datetime import datetime



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


def build_ingest_json(ds, type):
    # build the ingest JSON file for Rasdaman

    # geometry specific titles
    if type == "seg":
        title_string = "'Hydrological Summary Statistics for CONUS Stream Segments'"
        coverage_id = "conus_hydro_segments"
        nc_path = "seg.nc"
    elif type == "hru":
        title_string = "'Hydrological Summary Statistics for CONUS Watersheds'"
        coverage_id = "conus_hydro_hrus"
        nc_path = "hru.nc"

    # read encodings from the dataset
    nc_encoding_dict = eval(ds.attrs["Rasdaman Encodings"])
    stats_metadata = eval(ds.attrs["Statistics Metadata"])

    # build the ingest JSON parts
    # encodings part
    encoding_dict = {}
    for stat in stats_metadata.keys():
        encoding_dict[stat] = stats_metadata[stat]["units"]
    for dim in nc_encoding_dict.keys():
        encoding_dict[dim] = {}
        # reverse the encoding dictionary
        for dim_val in nc_encoding_dict[dim].keys():
            encoding_dict[dim][nc_encoding_dict[dim][dim_val]] = dim_val
    # convert the encodings dictionary into a string
    encoding_dict = json.dumps(encoding_dict)
    # bands part
    band_list = []
    for stat in stats_metadata.keys():
        stat_dict = {"name": stat, "identifier": stat, "nilValue": "-9999.0"}
        band_list.append(stat_dict)
    # axes part
    axes_dict = {}
    grid_order = 0
    # list all dims including geom_id
    all_dims = list(nc_encoding_dict.keys())
    # move geom_id to the end of the list
    all_dims.append(all_dims.pop(all_dims.index("geom_id")))

    for dim in all_dims:
        axes_dict[dim] = {
            "min": f"${{netcdf:variable:{dim}:min}}",
            "max": f"${{netcdf:variable:{dim}:max}}",
            "directPositions": f"${{netcdf:variable:{dim}}}",
            "gridOrder": grid_order,
            "irregular": "true",
        }
        grid_order = grid_order + 1
    # assemble the parts into the ingest JSON
    ingest_dict = {
        "config": {
            "service_url": "https://localhost/rasdaman/ows",
            "tmp_directory": "/tmp/",
            "crs_resolver": "http://localhost:8080/def/",
            "default_crs": "http://localhost:8080/def/crs/EPSG/0/3338",
            "default_null_values": ["-9999"],
            "mock": "false",
            "automated": "true",
            "insitu": "true",
        },
        "input": {
            "coverage_id": f"{coverage_id}",
            "paths": [f"{nc_path}"],
        },
        "recipe": {
            "name": "general_coverage",
            "options": {
                "tiling": "ALIGNED [0:*, 0:*, 0:*, 0:*, 0:*] tile size 4194304",
                "wms_import": "false",
                "import_order": "ascending",
                "coverage": {
                    "crs": 'OGC/0/Index1D?axis-label="lc"@OGC/0/Index1D?axis-label="model"@OGC/0/Index1D?axis-label="scenario"@OGC/0/Index1D?axis-label="era"@OGC/0/Index1D?axis-label="geom_id"',
                    "metadata": {
                        "type": "xml",
                        "global": {"Title": f"{title_string}"},
                        "local": {"Encoding": encoding_dict},
                    },
                    "slicer": {
                        "type": "netcdf",
                        "pixelIsPoint": "true",
                        "bands": band_list,
                        "axes": axes_dict,
                    },
                },
            },
        },
    }

    ingest_json = json.dumps(ingest_dict, indent=2)

    # replace "true" and "false" quoted strings with non-quoted strings
    # not sure if this is necessary, but this matches the formatting I see in the example injest JSON
    ingest_json = ingest_json.replace('"false"', "false")
    ingest_json = ingest_json.replace('"true"', "true")

    return ingest_json



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

    print(f"Writing ingest JSON files to {output_dir}...\n")

    # write ingest JSON files
    with open(os.path.join(output_dir, "seg_ingest.json"), "w") as f:
        f.write(seg_ingest_json)
    with open(os.path.join(output_dir, "hru_ingest.json"), "w") as f:
        f.write(hru_ingest_json)

    print("JSON files finished at ", datetime.now(), "\n")
