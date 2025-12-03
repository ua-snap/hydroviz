# Streamflow Climatology Processing Script

This script processes streamflow CSV data to generate daily climatology statistics by  era.

## Description

The script converts CSV streamflow data to NetCDF format and computes daily climatologies (minimum, mean, maximum) for one historical era, and three future projection eras:
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

All packages should be available in the `snap-geo` conda environment.

## Usage

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


## Batch Processing Scripts

For processing multiple CSV files, two additional scripts are provided:

### generate_slurm_jobs.py

Scans a directory for CSV files and generates individual SLURM job scripts for each file.

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

### Complete Workflow

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

Generates a SLURM job script for the combining task using the high-memory analysis partition.

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

Randomly samples coordinate combinations from the combined file and verifies that values match the corresponding source files. Handles cases where data is missing (NaN values) for certain model/scenario combinations.

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
- Provide a summary of passed/failed checks

## Rasdaman Database Preparation

For ingestion into Rasdaman databases, string dimensions must be converted to integers.

### convert_strings_for_rasdaman.py

Converts string dimensions (landcover, model, scenario, era) to integer indices while preserving the original mappings in coordinate attributes.

**Note:** This script should be run on a high-RAM compute node, not the login node, due to memory requirements for large files. Be sure to activate a conda environment that has `xarray` installed.

```bash
srun --partition=analysis --mem=750G --pty /bin/bash
conda activate snap-geo
python convert_strings_for_rasdaman.py \
    /path/to/combined_output.nc \
    /path/to/rasdaman_ready_output.nc \
```

The script will:
- Convert specified string dimensions to integer indices (0, 1, 2, ...)
- Store original string mappings in coordinate attributes as 'encoding'
- Preserve all data variables and other coordinates unchanged
- Add compression to reduce file size

### Complete Workflow with All Steps

```bash
# Step 1: Generate processing scripts for all CSV files
python generate_slurm_jobs.py input_dir output_dir temp_dir scripts_dir

# Step 2: Submit processing jobs
python submit_jobs.py scripts_dir

# Step 3: Wait for jobs to complete, then generate combining job
python generate_combine_job.py \
    output_dir \
    output_dir/combined.nc \
    scripts_dir

# Step 4: Submit combining job
sbatch scripts_dir/combine_netcdf.slurm

# Monitor combining job progress (in separate terminal)
# First get the job ID from squeue, then monitor the log file
squeue -u $USER  # Note the job ID
watch tail -n 20 scripts_dir/logs/combine_netcdf_<job_id>.out

# Step 5: Quality control verification (after combining completes)
python qc_combined_netcdf.py \
    output_dir/combined.nc \
    output_dir \
    --samples 20

# Step 6: Convert for Rasdaman ingestion (run on high-RAM compute node)
srun --partition=analysis --mem=750G --pty /bin/bash
conda activate snap-geo
python convert_strings_for_rasdaman.py \
    /path/to/combined_output.nc \
    /path/to/rasdaman_ready_output.nc \
```

The combining job uses the **analysis** partition with high-memory nodes (up to 1.5TB) for efficient processing of large datasets.

## Input File Format

The input CSV file should have:
- A "Date" column with datetime values
- Additional columns named with stream IDs (numeric)
- Streamflow values in the data columns

## Output File Format

### Individual NetCDF Files
Each processed CSV file produces a NetCDF file with:
- `doy_min`: Daily minimum streamflow by day-of-year and era
- `doy_mean`: Daily mean streamflow by day-of-year and era  
- `doy_max`: Daily maximum streamflow by day-of-year and era

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
  - `scenario`: All scenarios (e.g., 'historical', 'rcp26', 'ssp245', etc.)

### Rasdaman-Ready File
The Rasdaman conversion creates an integer-indexed version:
- Same data structure as combined file
- String dimensions converted to integers (0, 1, 2, ...)
- Original string mappings stored in coordinate attributes as 'encoding'

## Memory Considerations

The script processes data in chunks to manage memory usage:
- CSV data is first converted to Parquet format for efficient processing
- Streamflow columns are processed in configurable chunks
- Climatology calculations are done in stream chunks
- Combining step is performed on high-memory analysis partition (up to 1.5TB available)
- Real-time memory, CPU, and I/O monitoring during combining operations
- Progress tracking with elapsed time and completion estimates

## Error Handling and Monitoring

The scripts include comprehensive error handling and monitoring:
- Detailed error messages sent to stderr and SLURM output files
- Environment conflict detection (conda vs pipenv)
- Resource usage monitoring (RAM, CPU load, I/O wait)
- Progress tracking for long-running operations
- Automatic cleanup of intermediate files
- Validation of coordinate combinations in QC checks

## Notes

- All error messages appear in SLURM output files for debugging
- Intermediate parquet files are automatically cleaned up unless `--keep-intermediate` is specified
- Scripts create output and temp directories automatically if they don't exist
- Temp directories may persist after cleanup but will be empty
- The combining operation includes progress monitoring with resource usage statistics
- QC script handles mixed-case model names and validates missing data combinations
- Rasdaman conversion preserves all data while making dimensions database-compatible
