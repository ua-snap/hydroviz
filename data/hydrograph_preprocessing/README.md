# Daily Streamflow Climatology Processing Pipeline

These scripts process streamflow CSV data to generate daily climatology statistics by era, and coerce them to netCDF format. The netCDFs are then combined into one file for easy ingestion into Rasdaman. All streamflow values are in units of cubic feet per second (cfs).

## Description

The pipeline converts CSV streamflow data to NetCDF format and computes daily climatologies for each combination of landcover type, model, scenario, and era. The minimum, mean, and maximum value for each day of year is computed for one historical era, and three future projection eras:
- 1976-2005
- 2016-2045
- 2046-2075  
- 2071-2100

## Dependencies

Required Python packages:
- `pyarrow` - For efficient CSV to Parquet conversion
- `xarray` - For NetCDF data manipulation
- `pandas` - For data processing
- `numpy` - For numerical operations  
- `dask` - For distributed computing (combining step)
- `psutil` - For system resource monitoring
- `random` - For QC sampling (built-in)

All packages should be available in the standard `snap-geo` conda environment.

## Daily Streamflow Climatology Script

```bash
python process_streamflow_climatology.py <input_csv> <output_netcdf> <temp_dir> [options]
```

### Required Arguments
- `input_csv`: Path to input CSV file containing streamflow data
- `output_netcdf`: Path for output NetCDF file with climatology data
- `temp_dir`: Directory path for temporary intermediate files

### Optional Arguments
- `--keep-intermediate`: Keep intermediate files (parquet and full NetCDF)
- `--chunk-size`: Chunk size for processing streamflow columns (default: 2000)
- `--stream-chunk-size`: Number of streams to process at once for climatology calculation (default: 10000)

### Examples

Basic usage:
```bash
python process_streamflow_climatology.py \
    input.csv \
    output_climatology.nc \
    ./tmp
```

Keep intermediate files:
```bash
python process_streamflow_climatology.py \
    input.csv \
    output_climatology.nc \
    ./tmp
    --keep-intermediate
```

Specify chunk size and stream chunk sizes
```bash
python process_streamflow_climatology.py \
    input.csv \
    output_climatology.nc \
    ./tmp
    --keep-intermediate
    --chunk-size 2000
    --stream-chunk-size 10000
```


## Daily Streamflow Climatology Batch Processing Scripts

For processing multiple CSV files, two additional scripts are provided:

### generate_slurm_jobs.py

Scans a directory for CSV files and generates individual SLURM job scripts for each file. Optionally, use a pattern to subset the CSV files in the directory.

```bash
python generate_slurm_jobs.py \
    /path/to/csv/files \
    /path/to/output/netcdf \
    /path/to/temp/dir \
    /path/to/slurm/scripts \
    --pattern "*_nsegment_summary_seg_outflow.csv" \
    --job-name-prefix "streamflow_clim" \
    --partition "t2small" \
    --memory "96G" \
    --cpus 24
```

### submit_jobs.py

Submits all generated SLURM job scripts in a directory.

```bash
python submit_jobs.py /path/to/slurm/scripts
```

### Complete Daily Streamflow Climatology Workflow

The processing time here really depends on the compute resources available, and the number of jobs that are allowed to run concurrently. Each individual job should take 5-7 minutes.

```bash
# Generate scripts for all CSV files
python generate_slurm_jobs.py input_dir output_dir temp_dir scripts_dir

# Submit all jobs
python submit_jobs.py scripts_dir
```

## Combining NetCDF Files

After individual climatology files are generated, you can combine them into a single dataset using `dask` distributed processing.

### combine_netcdf_files.py

Combines multiple NetCDF climatology files into a single merged dataset using Dask for efficient processing.

```bash
python combine_netcdf_files.py \
    /path/to/netcdf/files \
    /path/to/combined_output.nc \
    --workers 4 \
    --threads-per-worker 6 \
    --pattern "*_doy_mmm_by_era.nc"
```

### generate_combine_job.py

Generates a SLURM job script for the combining task. By default, this uses a high-RAM compute node on the analysis partition. This job should take 1-2 hours to run. Read about how to monitor slurm job progress in the _Complete Workflow with All Steps_ section below.

```bash
python generate_combine_job.py \
    /path/to/netcdf/files \
    /path/to/combined_output.nc \
    /path/to/slurm/scripts \
    --job-name "combine_netcdf" \
    --memory "750G" \
    --cpus 28 \
    --workers 6 \
    --threads-per-worker 4
```

## Quality Control and Verification

After combining files, you can verify the data integrity using the quality control script.

### qc_combined_netcdf.py

Randomly samples coordinate combinations from the combined file and verifies that values match the corresponding source files. Handles cases where data is missing (NaN values) for certain model/scenario combinations. This script does not require many resources and is safe to run from the login node.

```bash
python qc_combined_netcdf.py \
    /path/to/combined_output.nc \
    /path/to/source/netcdf/files \
    --samples 10
```

The script will:
- Generate random coordinate combinations respecting scenario-era constraints (historical only with 1976-2005, future scenarios only with future eras)
- Handle case mismatches between combined file (lowercase) and source filenames (mixed case)
- Verify that missing combinations properly result in NaN values
- Provide a summary of pass/fail checks

## Rasdaman Prep

For ingestion into Rasdaman, string dimensions must be converted to integers, and we need encoding information added to the dimension attributes. We also need to split the combined dataset into smaller pieces so that we aren't ingesting a file that is too large or complex to be performant. These tasks are done in separate steps here to increase granularity and allow for easier source dataset revisions if problems arise during the ingestion process.

### convert_strings_for_rasdaman.py

Converts string dimensions (landcover, model, scenario, era) to integer indices while preserving the original mappings in coordinate attributes.

**Note:** This script should be run on a high-RAM compute node, not the login node, due to memory requirements for large files. Be sure to activate a conda environment that has `xarray` installed. This should take about 1 hour to run.

```bash
srun --partition=analysis --mem=750G --pty /bin/bash
conda activate snap-geo
python convert_strings_for_rasdaman.py \
    /path/to/combined_output.nc \
    /path/to/rasdaman_ready_output.nc
```

The script will:
- Convert specified string dimensions to integer indices (0, 1, 2, ...)
- Store original string mappings in coordinate attributes as 'encoding'
- Preserve all data variables and other coordinates unchanged
- Add compression to reduce file size

### split_combined_netcdf_file.py

Splits the combined file into four separate files for ingestion. Files are split by time period (historical vs projected) and by landcover (static vs dynamic).

```bash
srun --partition=analysis --mem=750G --pty /bin/bash
conda activate snap-geo
python split_combined_netcdf_file.py \
    /path/to/rasdaman_ready_output.nc \
    /path/to/split/coverage/directory
```

**Note:** This script should also be run on a high-RAM compute node, not the login node, due to memory requirements for large files. Be sure to activate a conda environment that has `xarray` installed. This should take about 30 minutes to run.

# Complete Workflow with All Steps

```bash
# Step 1: Generate processing scripts for all CSV files
python generate_slurm_jobs.py input_dir netcdf_dir temp_dir scripts_dir

# Step 2: Submit processing jobs
python submit_jobs.py scripts_dir

# Step 3: Wait for jobs to complete, then generate combining job
python generate_combine_job.py \
    netcdf_dir \
    netcdf_dir/combined.nc \
    scripts_dir

# Step 4: Submit combining job
sbatch scripts_dir/combine_netcdf.slurm

# Monitor combining job progress
# First get the job ID from squeue or the terminal message after submitting the job, then monitor the log file
squeue -u $USER  # Note the job ID
watch tail -n 20 scripts_dir/logs/combine_netcdf_<job_id>.out

# Step 5: Quality control verification (after combining completes)
# this can be run from the login node
conda activate snap-geo
python qc_combined_netcdf.py \
    netcdf_dir/combined.nc \
    netcdf_dir \

# Step 6: Convert for Rasdaman ingestion
# run on high-RAM compute node
srun --partition=analysis --mem=750G --pty /bin/bash
conda activate snap-geo
python convert_strings_for_rasdaman.py \
    netcdf_dir/combined.nc \
    netcdf_dir/rasdaman_ready_output.nc \

# Step 7: Split into multiple coverages
# run on high-RAM compute node
srun --partition=analysis --mem=750G --pty /bin/bash
conda activate snap-geo
python split_combined_netcdf_file.py \
    netcdf_dir/rasdaman_ready_output.nc \
    netcdf_dir/coverages_to_export

```

# Notes

## Input Files

The input CSV files (from [here](https://www.sciencebase.gov/catalog/item/63890125d34ed907bf78e97f) and [here](https://www.sciencebase.gov/catalog/item/6373bf5cd34ed907bf6c6e38)) are about 20GB each unzipped, and have:
- A "Date" column with datetime values
- Additional columns named with stream IDs (numeric)
- Streamflow values in the data columns

Note that the `static_Maurer_nsegment_summary_seg_outflow.csv` and `dynamic_Maurer_nsegment_summary_seg_outflow.csv` input filenames were changed to `static_Maurer_historical_r1i1p1_nsegment_summary_seg_outflow.csv` and `dynamic_Maurer_historical_r1i1p1_nsegment_summary_seg_outflow.csv` to match the naming convention of the rest of the files, and make parsing filenames easier. The `r1i1p1` variant doesn't really mean anything here.

## Output Files

### Individual NetCDF Files
Each processed CSV file produces a NetCDF file with variables:
- `doy_min`: Daily minimum streamflow over era
- `doy_mean`: Daily mean streamflow over era
- `doy_max`: Daily maximum streamflow over era

Dimensions:
- `era`: Time periods (historical: 1976-2005; projections: 2016-2045, 2046-2075, 2071-2100)
- `doy`: Day of year (1-366)
- `stream_id`: Stream identifiers
- `landcover`: Land cover type (single value per file)
- `model`: Climate model (single value per file)
- `scenario`: Climate scenario (single value per file)

### Combined NetCDF File
The combined file merges all individual files along the model, scenario, and landcover dimensions:
- Same data variables: `doy_min`, `doy_mean`, `doy_max`
- Same `era`, `doy`, `stream_id` dimensions
- Expanded dimensions with multiple values:
  - `landcover`: All land cover types (e.g., 'dynamic', 'static')
  - `model`: All climate models (e.g., 'cesm2', 'miroc-esm-chem', etc.)
  - `scenario`: All scenarios (e.g., 'historical', 'rcp26', 'rcp45', etc.)

### Rasdaman-Ready File
The Rasdaman conversion creates an integer-indexed version:
- Same data structure as combined file
- String dimensions converted to integers (0, 1, 2, ...)
- Original string mappings stored in coordinate attributes as 'encoding'

### Split coverage files
The combined Rasdaman-ready file is split by time period and by landcover.
- Reduces coverage size 
- Split method can be easily adjusted for future optimization
- No need to run the whole pipeline again to experiment with split method

## Memory Considerations

The `process_streamflow_climatology.py` script tries to manage memory usage by:
- First converting CSV data to Parquet format for efficient processing
- Streamflow columns are processed in configurable chunks
- Climatology calculations are done in stream chunks
- Automatic cleanup of intermediate files
The combining step tries to manage memory usage by:
- Using a high-memory analysis partition (up to 1.5TB RAM available on these nodes)
- Real-time memory, CPU, and I/O monitoring during combining operations (via watching output files)
- Progress tracking with elapsed time and completion estimates (via watching output files)

## Error Handling and Monitoring

The scripts include comprehensive error handling and monitoring:
- Detailed error messages sent to stderr and SLURM output files (*.out and *.err)
- Environment conflict detection (conda vs pipenv)
- Validation of coordinate combinations in QC checks

## Additional Notes

- Scripts create output and temp directories automatically if they don't exist
- All error messages appear in SLURM *.err files for debugging
- Intermediate parquet files are automatically cleaned up unless `--keep-intermediate` is specified
- Temp directories may persist after cleanup but will be empty
- Be aware that the combined file output is compressed, and will be uncompressed when ingesting into Rasdaman; the Rasdaman coverage will likely be much larger size than the combined file!
