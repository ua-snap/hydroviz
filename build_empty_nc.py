from pathlib import Path
import xarray as xr
import pandas as pd
import numpy as np

from functions import *
from luts import stat_vars_dict

data_dir = Path("/beegfs/CMIP6/jdpaul3/hydroviz_data/stats")
output_dir = Path("/beegfs/CMIP6/jdpaul3/hydroviz_data/nc")

seg_files = list(data_dir.glob("dynamic*seg*.csv"))
seg_files += list(data_dir.glob("static*seg*.csv"))

hru_files = list(data_dir.glob("dynamic*hru*.csv"))
hru_files += list(data_dir.glob("static*hru*.csv"))

seg_files = filter_files(seg_files)
hru_files = filter_files(hru_files)

seg_ids = pd.read_csv(seg_files[0]).seg_id.astype(str).tolist()
hru_ids = pd.read_csv(hru_files[0]).hru_id.astype(str).tolist()

geom_coords_dict = {}
geom_coords_dict["seg"] = get_unique_coords(seg_files)
geom_coords_dict["hru"] = get_unique_coords(hru_files)

seg_ds = create_empty_dataset(geom_coords_dict["seg"], stat_vars_dict, seg_ids)
seg_ds.to_netcdf(output_dir.join("seg.nc"))

hru_ds = create_empty_dataset(geom_coords_dict["hru"], stat_vars_dict, hru_ids)
hru_ds.to_netcdf(output_dir.join("hru.nc"))
