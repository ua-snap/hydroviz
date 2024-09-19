import argparse
import sys
from pathlib import Path
from functions import *


def arguments(argv):
    """Parse some args"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, help="directory where hydrologic stats CSVs are located", required=True)
    parser.add_argument("--output_dir", type=str, help="directory where hydrologic stats netCDFs will be saved", required=True)
    parser.add_argument("--conda_init_script", type=str, help="location of conda initialization script", required=True)
    parser.add_argument("--conda_env_name", type=str, help="conda environment to use", required=True)
    parser.add_argument("--build_nc_script", type=str, help="location of build_nc.py", required=True)
    
    args = parser.parse_args()
    data_dir = args.data_dir
    output_dir = args.output_dir
    conda_init_script = args.conda_init_script
    conda_env_name = args.conda_env_name
    build_nc_script = args.build_nc

    return data_dir, output_dir, conda_init_script, conda_env_name, build_nc_script


if __name__ == "__main__":

    data_dir, output_dir, conda_init_script, conda_env_name, build_nc_script = arguments(sys.argv)

    # set up filepaths for slurm job
    sbatch_fp = Path(output_dir).join("build_nc.slurm")
    sbatch_out_fp = Path(output_dir).join("build_nc_%j.out")

    # write sbatch head + commands, then submit job
    sbatch_head = write_sbatch_head(sbatch_out_fp, conda_init_script, conda_env_name)
    write_sbatch(sbatch_fp, sbatch_out_fp, sbatch_head, build_nc_script, data_dir, output_dir)
    submit_sbatch(sbatch_fp)