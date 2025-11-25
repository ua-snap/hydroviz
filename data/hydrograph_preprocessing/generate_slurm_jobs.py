#!/usr/bin/env python3
"""
Generate SLURM job scripts for processing streamflow CSV files.

This script scans a directory for CSV files matching the streamflow data pattern
and generates individual SLURM job scripts for each file using the 
process_streamflow_climatology.py script.
"""

import os
import sys
import argparse
from pathlib import Path
import glob


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate SLURM job scripts for streamflow CSV processing",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "input_dir",
        type=str,
        help="Directory containing CSV files to process"
    )
    
    parser.add_argument(
        "output_dir", 
        type=str,
        help="Directory to save processed NetCDF files"
    )
    
    parser.add_argument(
        "temp_dir",
        type=str, 
        help="Directory for temporary intermediate files"
    )
    
    parser.add_argument(
        "scripts_dir",
        type=str,
        help="Directory to save generated SLURM job scripts"
    )
    
    parser.add_argument(
        "--pattern",
        type=str,
        default="*_nsegment_summary_seg_outflow.csv",
        help="Glob pattern to match CSV files"
    )
    
    parser.add_argument(
        "--job-name-prefix",
        type=str,
        default="streamflow",
        help="Prefix for SLURM job names"
    )
    
    parser.add_argument(
        "--partition",
        type=str,
        default="t2small",
        help="SLURM partition to use"
    )
    
    parser.add_argument(
        "--memory",
        type=str,
        default="96G",
        help="Memory allocation for jobs"
    )
    
    parser.add_argument(
        "--cpus",
        type=int,
        default=24,
        help="Number of CPUs per task"
    )
    
    parser.add_argument(
        "--time-limit",
        type=str,
        default="00:30:00",
        help="Time limit for jobs (HH:MM:SS)"
    )
    
    parser.add_argument(
        "--conda-env",
        type=str,
        default="snap-geo",
        help="Conda environment to activate"
    )
    
    parser.add_argument(
        "--processing-script",
        type=str,
        default="process_streamflow_climatology.py",
        help="Path to the processing script"
    )
    
    parser.add_argument(
        "--keep-intermediate",
        action="store_true",
        help="Pass --keep-intermediate flag to processing script"
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


def generate_slurm_script(csv_file, output_file, temp_dir, args, scripts_dir):
    """Generate a SLURM job script for a single CSV file."""
    
    # Create job name from CSV filename
    csv_name = Path(csv_file).stem
    job_name = f"{args.job_name_prefix}_{csv_name}"
    
    # Build processing command
    processing_cmd = [
        "python", args.processing_script,
        f'"{csv_file}"',
        f'"{output_file}"', 
        f'"{temp_dir}"',
        f"--chunk-size {args.chunk_size}",
        f"--stream-chunk-size {args.stream_chunk_size}"
    ]
    
    if args.keep_intermediate:
        processing_cmd.append("--keep-intermediate")
    
    processing_cmd_str = " \\\n    ".join(processing_cmd)
    
    # Generate SLURM script content
    script_content = f"""#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task={args.cpus}
#SBATCH --mem={args.memory}
#SBATCH --partition={args.partition}
#SBATCH --time={args.time_limit}
#SBATCH --output={scripts_dir}/logs/%x_%j.out

# Activate conda environment
source $HOME/miniconda3/etc/profile.d/conda.sh
conda activate {args.conda_env}

echo "Starting processing at $(date)"

# Run the script
{processing_cmd_str}

# Check exit status
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo "Processing completed successfully at $(date)"
else
    echo "Processing failed with exit code $EXIT_CODE at $(date)"
    if [ $EXIT_CODE -eq 137 ] || [ $EXIT_CODE -eq 9 ]; then
        echo "This appears to be a memory-related failure. Consider increasing the memory allocation."
    fi
    exit $EXIT_CODE
fi
"""

    return script_content


def main():
    """Main function to generate SLURM scripts."""
    args = parse_arguments()
    
    # Convert paths to Path objects
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    temp_dir = Path(args.temp_dir)
    scripts_dir = Path(args.scripts_dir)
    
    # Validate input directory
    if not input_dir.exists():
        print(f"Error: Input directory does not exist: {input_dir}", file=sys.stderr)
        sys.exit(1)
    
    # Create output directories
    for directory in [output_dir, temp_dir, scripts_dir]:
        directory.mkdir(parents=True, exist_ok=True)
    
    # Create logs directory for SLURM output
    logs_dir = scripts_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Find CSV files matching the pattern
    csv_files = list(input_dir.glob(args.pattern))
    
    if not csv_files:
        print(f"No CSV files found matching pattern '{args.pattern}' in {input_dir}")
        sys.exit(1)
    
    print(f"Found {len(csv_files)} CSV files to process")
    
    # Generate scripts for each CSV file
    generated_scripts = []
    
    for csv_file in csv_files:
        # Generate output NetCDF filename
        csv_name = csv_file.stem
        if "_nsegment_summary_seg_outflow" in csv_name:
            netcdf_name = csv_name.replace("_nsegment_summary_seg_outflow", "_doy_mmm_by_era.nc")
        else:
            netcdf_name = csv_name + "_doy_mmm_by_era.nc"
        
        output_file = output_dir / netcdf_name
        
        # Create file-specific temp directory
        file_temp_dir = temp_dir / csv_name
        
        # Generate SLURM script
        script_content = generate_slurm_script(
            str(csv_file), 
            str(output_file), 
            str(file_temp_dir),
            args,
            str(scripts_dir)
        )
        
        # Save script
        script_filename = f"{csv_name}.sh"
        script_path = scripts_dir / script_filename
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make script executable
        script_path.chmod(0o755)
        
        generated_scripts.append(script_path)
        print(f"Generated: {script_path}")
    
    # Create a summary file
    summary_file = scripts_dir / "job_summary.txt"
    with open(summary_file, 'w') as f:
        f.write(f"Generated SLURM job scripts: {len(generated_scripts)}\n")
        f.write(f"Generated on: {os.popen('date').read().strip()}\n")
        f.write(f"Input directory: {input_dir}\n")
        f.write(f"Output directory: {output_dir}\n") 
        f.write(f"Temp directory: {temp_dir}\n")
        f.write(f"Scripts directory: {scripts_dir}\n\n")
        f.write("Generated scripts:\n")
        for script in generated_scripts:
            f.write(f"  {script.name}\n")
    
    print(f"\nGenerated {len(generated_scripts)} SLURM job scripts in {scripts_dir}")
    print(f"Summary written to: {summary_file}")
    print(f"\nTo submit all jobs, run:")
    print(f"  python submit_jobs.py {scripts_dir}")


if __name__ == "__main__":
    main()