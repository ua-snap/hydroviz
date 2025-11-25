#!/usr/bin/env python3
"""
Generate a SLURM job script for combining NetCDF files using the "analysis" partition.

This script creates a SLURM job that uses the high-memory analysis partition
to combine multiple NetCDF climatology files using Dask distributed processing.
"""

import sys
import argparse
from pathlib import Path


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate SLURM job script for NetCDF file combining",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "input_dir",
        type=str,
        help="Directory containing NetCDF files to combine"
    )
    
    parser.add_argument(
        "output_file",
        type=str,
        help="Path for output combined NetCDF file"
    )
    
    parser.add_argument(
        "script_dir",
        type=str,
        help="Directory where the SLURM script will be saved"
    )
    
    parser.add_argument(
        "--job-name",
        type=str,
        default="combine_netcdf",
        help="SLURM job name"
    )
    
    parser.add_argument(
        "--memory",
        type=str,
        default="500G",
        help="Memory allocation for job"
    )
    
    parser.add_argument(
        "--cpus",
        type=int,
        default=28,
        help="Number of CPUs per task"
    )
    
    parser.add_argument(
        "--time-limit",
        type=str,
        default="01:00:00",
        help="Time limit for job (HH:MM:SS)"
    )
    
    parser.add_argument(
        "--conda-env",
        type=str,
        default="snap-geo",
        help="Conda environment to activate"
    )
    
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of Dask workers"
    )
    
    parser.add_argument(
        "--threads-per-worker",
        type=int,
        default=6,
        help="Number of threads per Dask worker"
    )
    
    parser.add_argument(
        "--pattern",
        type=str,
        default="*_doy_mmm_by_era.nc",
        help="Glob pattern to match NetCDF files"
    )
    
    return parser.parse_args()


def generate_slurm_script(args):
    """Generate SLURM script content."""
    
    script_content = f"""#!/bin/bash
#SBATCH --job-name={args.job_name}
#SBATCH --partition=analysis
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task={args.cpus}
#SBATCH --mem={args.memory}
#SBATCH --time={args.time_limit}
#SBATCH --output={args.script_dir}/logs/%x_%j.out

# Activate conda environment
source $HOME/miniconda3/etc/profile.d/conda.sh
conda activate {args.conda_env}

echo "Starting NetCDF file combining at $(date)"
echo "Job running on node: $HOSTNAME"
echo "Available memory: {args.memory}"
echo "CPUs allocated: {args.cpus}"
echo "Dask workers: {args.workers}"
echo "Threads per worker: {args.threads_per_worker}"

# Run the combining script
python combine_netcdf_files.py \\
    "{args.input_dir}" \\
    "{args.output_file}" \\
    --pattern "{args.pattern}" \\
    --workers {args.workers} \\
    --threads-per-worker {args.threads_per_worker}

# Check exit status
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo "NetCDF combining completed successfully at $(date)"
    
    # Display output file info
    if [ -f "{args.output_file}" ]; then
        echo "Output file size: $(du -h '{args.output_file}' | cut -f1)"
        echo "Output file info:"
        ncdump -h "{args.output_file}" | head -20
    fi
else
    echo "NetCDF combining failed with exit code $EXIT_CODE at $(date)"
    if [ $EXIT_CODE -eq 137 ] || [ $EXIT_CODE -eq 9 ]; then
        echo "This appears to be a memory-related failure. Consider increasing memory allocation."
    fi
    exit $EXIT_CODE
fi

echo "Job completed at $(date)"
"""
    
    return script_content


def main():
    """Main function to generate SLURM script."""
    args = parse_arguments()
    
    # Convert paths to Path objects
    input_dir = Path(args.input_dir)
    output_file = Path(args.output_file)
    script_dir = Path(args.script_dir)

    # Create log directory if it doesn't exist
    (script_dir / "logs").mkdir(parents=True, exist_ok=True)
    
    # Validate input directory exists
    if not input_dir.exists():
        print(f"Error: Input directory does not exist: {input_dir}", file=sys.stderr)
        sys.exit(1)
    
    # Check for NetCDF files
    nc_files = list(input_dir.glob(args.pattern))
    if not nc_files:
        print(f"Warning: No NetCDF files found matching '{args.pattern}' in {input_dir}")
    else:
        print(f"Found {len(nc_files)} NetCDF files to combine:")
        for f in sorted(nc_files):
            print(f"  {f.name}")
    
    # Create output and script directories
    output_file.parent.mkdir(parents=True, exist_ok=True)
    script_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate script content
    script_content = generate_slurm_script(args)
    
    # Write SLURM script
    script_path = script_dir / f"{args.job_name}.slurm" 
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    # Make script executable
    script_path.chmod(0o755)
    
    print(f"Generated SLURM script: {script_path}")
    print(f"To submit: sbatch {script_path}")
    print(f"Output will be written to: {output_file}")
    print(f"Log will be written to: {script_dir}/logs/{args.job_name}_<job_id>.out")


if __name__ == "__main__":
    main()