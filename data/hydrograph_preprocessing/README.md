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
- `pyarrow`
- `xarray`
- `pandas`
- `numpy`
- `dask`

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
    /path/to/slurm_script.sh \
    --job-name "combine_climatology" \
    --memory "500G" \
    --cpus 28 \
    --workers 4 \
    --threads-per-worker 6
```

### Complete Workflow with Combining

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
sbatch scripts_dir/combine_job.sh
```

The combining job uses the **analysis** partition with high-memory nodes (up to 1.5TB) for efficient processing of large datasets.

## Input File Format

The input CSV file should have:
- A "Date" column with datetime values
- Additional columns named with stream IDs (numeric)
- Streamflow values in the data columns

## Output File Format

The output NetCDF file contains:
- `doy_min`: Daily minimum streamflow by day-of-year and era
- `doy_mean`: Daily mean streamflow by day-of-year and era  
- `doy_max`: Daily maximum streamflow by day-of-year and era

Dimensions:
- `era`: One historical and three projection periods (1976-2005, 2016-2045, 2046-2075, 2071-2100)
- `doy`: Day of year (1-366)
- `stream_id`: Stream identifiers

## Memory Considerations

The script processes data in chunks to manage memory usage:
- CSV data is first converted to Parquet format for efficient processing
- Streamflow columns are processed in configurable chunks
- Climatology calculations are done in stream chunks
- Combining step is performed on high-memory partition

## Notes

- Error messages are sent to stderr, and should appear in SLURM output files
- Intermediate parquet files are automatically cleaned up unless `--keep-intermediate` is specified
- The script creates output and temp directories if they don't exist
- Temp directory / subdirectories may persist after cleanup, but they will be empty