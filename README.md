# hydroviz
Visualization of hydrological futures data from the Southeast CASC.

Read a project description [here](https://secasc.ncsu.edu/2023/08/28/modeling-hydrologic-simulations-for-past-future-conditions-across-the-conterminous-us/). Read a paper (Regan and others, 2018) about the of the Precipitation-Runoff Modeling System (PRMS) [here](https://pubs.usgs.gov/publication/tm6B9). 

The data can be found [here](https://www.usgs.gov/data/model-input-and-output-hydrologic-simulations-conterminous-united-states-historical-and-future). Use the `download.ipynb` notebook to download the data using the ScienceBase API (requires install of [sciencebasepy](https://github.com/DOI-USGS/sciencebasepy/tree/master)), or just access on Chinook at `import/beegfs/CMIP6/jdpaul3/hydroviz_data`. 



`python run_build_nc.py --data_dir /beegfs/CMIP6/jdpaul3/hydroviz_data/stats --output_dir /beegfs/CMIP6/jdpaul3/hydroviz_data/nc --conda_init_script /beegfs/CMIP6/jdpaul3/hydroviz/conda_init.sh --conda_env_name snap-geo --build_nc_script /beegfs/CMIP6/jdpaul3/hydroviz/build_nc.py`