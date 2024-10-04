# hydroviz
Visualization of hydrological futures data from the Southeast CASC.

Read a project description [here](https://secasc.ncsu.edu/2023/08/28/modeling-hydrologic-simulations-for-past-future-conditions-across-the-conterminous-us/). Read a paper (Regan and others, 2018) about the Precipitation-Runoff Modeling System (PRMS) [here](https://pubs.usgs.gov/publication/tm6B9). The source data can be found [here](https://www.usgs.gov/data/model-input-and-output-hydrologic-simulations-conterminous-united-states-historical-and-future).

According to the Regan paper above, the PRMS uses the original geospatial fabric of the National Hydrologic Model (Vigel & Bock, 2014; found [here](https://www.sciencebase.gov/catalog/item/535eda80e4b08e65d60fc834)) and **NOT** the updated v1.1 geospatial fabric (Santiago et al, 2020; found [here](https://www.sciencebase.gov/catalog/item/5e29d1a0e4b0a79317cf7f63)).


### How to use this codebase

- This codebase uses the `snap-geo` conda environment, details found [here](https://github.com/ua-snap/snap-geo/tree/add_conda_env). 

- Use `download.ipynb` if you want to download a copy of the data (requires install of [sciencebasepy](https://github.com/DOI-USGS/sciencebasepy/tree/master) into `snap-geo`). Be warned, there are problems with downloading the data via the `sciencebasepy` API, and therefore some of this process is manual point-and-click tedium. For testing, it's recommended to just access the data from this directory instead: `/import/beegfs/CMIP6/jdpaul3/hydroviz_data`

- Use the `eda.ipynb` notebook to familiarize yourself with the dataset structure.

- To coerce the data into a netCDF format, run the following command to submit an `sbatch` script. Change the script locations to match your repo location, and change the `--output_dir` argument to save the netCDF files to a different location and avoid overwriting previous outputs. The script should only take ~5 minutes to run once compute resources are allocated.

```
python run_build_nc.py --data_dir /beegfs/CMIP6/jdpaul3/hydroviz_data/stats --gis_dir /beegfs/CMIP6/jdpaul3/hydroviz_data/gis --output_dir /beegfs/CMIP6/jdpaul3/hydroviz_data/nc --conda_init_script /beegfs/CMIP6/jdpaul3/hydroviz/conda_init.sh --conda_env_name snap-geo --build_nc_script /beegfs/CMIP6/jdpaul3/hydroviz/build_nc.py
```

- Use the `qc.ipynb` notebook to compare values in the netCDFs to source values.

- Run the `xwalk.ipynb` notebook to crosswalk stream segment IDs and watershed IDs from the project geospatial data (`Segments_subset.shp` and `HRU_subset.shp`) to the GNIS name attributes in the NHM geospatial fabric. This notebook exports new shapefiles with the added GNIS common names for hosting in GeoServer ([gs.earthmaps.io](http://gs.earthmaps.io/)).
