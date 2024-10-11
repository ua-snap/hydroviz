import argparse
import sys
import os
import subprocess
from pathlib import Path

def arguments(argv):
    """Parse some args"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, help="directory where hydrologic stats CSVs are located", required=True)
    parser.add_argument("--gis_dir", type=str, help="directory where GIS files are located", required=True)
    parser.add_argument("--output_dir", type=str, help="directory where hydrologic stats netCDFs will be saved", required=True)
    parser.add_argument("--conda_init_script", type=str, help="location of conda initialization script", required=True)
    parser.add_argument("--conda_env_name", type=str, help="conda environment to use", required=True)
    parser.add_argument("--build_nc_script", type=str, help="location of build_nc.py", required=True)
    
    args = parser.parse_args()
    data_dir = args.data_dir
    gis_dir = args.gis_dir
    output_dir = args.output_dir
    conda_init_script = args.conda_init_script
    conda_env_name = args.conda_env_name
    build_nc_script = args.build_nc_script

    return data_dir, gis_dir, output_dir, conda_init_script, conda_env_name, build_nc_script


def write_sbatch_head(sbatch_out_fp, conda_init_script, conda_env_name):
    """Make a string of SBATCH commands that can be written into a .slurm script

    Args:
        conda_init_script (path_like): path to a script that contains commands for initializing the shells on the compute nodes to use conda activate

    Returns:
        sbatch_head (str): string of SBATCH commands ready to be used as parameter in sbatch-writing functions. The following gaps are left for filling with .format:
            - output slurm filename
    """
    sbatch_head = (
        "#!/bin/sh\n"
        "#SBATCH --nodes=1\n"
        f"#SBATCH --cpus-per-task=24\n"
        f"#SBATCH -p t2small\n"
        f"#SBATCH --output {sbatch_out_fp}\n"
        # print start time
        "echo Start slurm && date\n"
        "echo\n"
        # prepare shell for using activate
        f"source {conda_init_script}\n"
        f"conda activate {conda_env_name}\n"
    )

    return sbatch_head


def write_sbatch(
    sbatch_fp,
    sbatch_out_fp,
    sbatch_head,
    build_nc_script,
    data_dir,
    gis_dir,
    output_dir,
):
    """Write an sbatch script for building the netCDFs

    Args:
        sbatch_fp (path_like): path to .slurm script to write sbatch commands to
        sbatch_out_fp (path_like): path to where sbatch stdout should be written
        sbatch_head (dict): string for sbatch head script

    Returns:
        None, writes the commands to sbatch_fp
    """
    pycommands = "\n"
    pycommands += (
        f"python {build_nc_script} "
        f"--data_dir {data_dir} "
        f"--gis_dir {gis_dir} "
        f"--output_dir {output_dir} "
    )

    #TODO: add the build_ingest_json.py script to pycommands here

    pycommands += "\n\n"

    commands = sbatch_head.format(sbatch_out_fp=sbatch_out_fp) + pycommands

    with open(sbatch_fp, "w") as f:
        f.write(commands)

    return


def submit_sbatch(sbatch_fp):
    """Submit a script to slurm via sbatch

    Args:
        sbatch_fp (pathlib.PosixPath): path to .slurm script to submit

    Returns:
        job id for submitted job
    """
    out = subprocess.check_output(["sbatch", str(sbatch_fp)])
    job_id = out.decode().replace("\n", "").split(" ")[-1]

    return job_id


if __name__ == "__main__":

    data_dir, gis_dir, output_dir, conda_init_script, conda_env_name, build_nc_script = arguments(sys.argv)

    # create the output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True, parents=True)

    # set up filepaths for slurm job
    sbatch_fp = os.path.join(output_dir, "build_nc.slurm")
    sbatch_out_fp = os.path.join(output_dir, "build_nc_%j.out")

    # write sbatch head + commands, then submit job
    sbatch_head = write_sbatch_head(sbatch_out_fp, conda_init_script, conda_env_name)
    write_sbatch(sbatch_fp, sbatch_out_fp, sbatch_head, build_nc_script, data_dir, gis_dir, output_dir)
    submit_sbatch(sbatch_fp)