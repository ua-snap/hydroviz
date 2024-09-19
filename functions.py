import subprocess
import numpy as np
import xarray as xr
from luts import era_lookup, stat_vars_dict



##### DATA PROCESSING FUNCTIONS #####

def filter_files(files):
# ignore Maurer files and the "diff" files
# also ignore the files with full historical range (1952-2005); this overlaps the
# normal historical range (1976-2005) and is confusing

    filtered_files = []
    starting_len = len(files)
    count = 0
    for f in files:
        if "Maurer" in f.name: 
            count = count+1
            pass
        elif "diff" in f.name:
            count = count+1
            pass
        elif "1952_2005" in f.name:
            count = count+1
            pass
        else:
            filtered_files.append(f)

    print(f"Removed {count} files from list; {len(filtered_files)} files remain out of {starting_len} original files.")
    return filtered_files


def get_unique_coords(files):
# get unique coordinates from the file names

    lcs = []
    models = [] 
    scenarios = []
    variants = []
    eras = []

    for file in files:
        parts = file.name.split('_')
        try:
            lc, model, scenario, variant, era = parts[0], parts[1], parts[2], parts[3], "_".join([parts[5], parts[6].split(".")[0]])
        except:
            print(f"Error parsing file: {file.name}")
            continue

        lcs.append(lc)
        models.append(model)
        scenarios.append(scenario)
        variants.append(variant)
        eras.append(era)

    lcs = sorted(list(set(lcs)))
    models = sorted(list(set(models))) 
    scenarios = sorted(list(set(scenarios)))
    variants = sorted(list(set(variants)))
    eras = sorted(list(set(eras)))

    dict = {
        "lcs": lcs,
        "models": models,
        "scenarios": scenarios,
        "variants": variants,
        "eras": eras,
    }

    return dict


def create_empty_dataset(dict, geom_ids):

    stat_vars = stat_vars_dict.keys()

    lcs, models, scenarios, eras = dict["lcs"], dict["models"], dict["scenarios"], dict["eras"]

    # build list of era strings
    eras_index = []
    for e in eras:
        eras_index.append(era_lookup[e])

    # create a dict with an empty array of nan values for each stat variable
    # shape is defined by the length of all coords
    # we will fill in the nan values with actual data later, if they exists
    data_dict = {}
    for stat in stat_vars:
        data_dict[stat] = (["lc", "model", "scenario", "era", "geom_id"], 
                           np.zeros((len(lcs), len(models), len(scenarios), len(eras_index), len(geom_ids))) * np.nan)

    ds = xr.Dataset(data_dict, 
                    coords={
            "lc": (["lc"], lcs),
            "model": (["model"], models), 
            "scenario": (["scenario"], scenarios),
            "era": (["era"], eras_index),
            "geom_id": (["geom_id"], geom_ids),
        },
    )

    return ds




##### SLURM FUNCTIONS #####

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
        f"--output_dir {output_dir} "
    )
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