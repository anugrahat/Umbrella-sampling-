import os
import re
import shutil

# List of additional configurations from the image
new_configs = [
    "981", "954", "967", "970", "960"
]

def createOutputFile(template_file, frame_name, output_dir, search_string="XXX"):
    """Replace the search string with the frame name in a template file and save it."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    out_file = os.path.join(output_dir, template_file)

    with open(template_file, 'r') as f:
        file_contents = f.read()

    with open(out_file, 'w') as f:
        f.write(re.sub(search_string, frame_name, file_contents))

def copyAdditionalFiles(output_dir, additional_files):
    """Copy additional files into the output directory."""
    for file in additional_files:
        if os.path.exists(file):
            shutil.copy(file, output_dir)
        else:
            print(f"Warning: {file} not found. Skipping this file.")

def copyCorrespondingGroFile(frame_name, output_dir):
    """Copy the corresponding conf{frame_name}.gro file into the output directory."""
    gro_file = f"conf{frame_name}.gro"
    if os.path.exists(gro_file):
        shutil.copy(gro_file, output_dir)
    else:
        print(f"Warning: {gro_file} not found. Skipping this file.")

def createSrunScripts(frame_name, output_dir):
    """Create srun_pull.sh and srun_umbrella.sh scripts."""
    srun_pull_content = f"""#!/bin/bash
#SBATCH --job-name="combined_cmd_gamd"
#SBATCH --output="combined_cmd_gamd.%j.%N.out"
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=50G
#SBATCH --account=ahnlab
#SBATCH --partition=gpu-ahn
#SBATCH --no-requeue
#SBATCH --mail-user=tchettri@ucdavis.edu
#SBATCH --mail-type=ALL
#SBATCH -t 360:00:00

module load cuda/11.8.0
module load gromacs/2024

gmx_mpi grompp -f npt_umbrella.mdp -c conf{frame_name}.gro -p single2_large.top -r conf{frame_name}.gro -n rbd_2_reg.ndx -o npt{frame_name}.tpr -maxwarn 2
srun gmx_mpi mdrun -deffnm npt{frame_name} -nb gpu -bonded gpu
"""

    srun_umbrella_content = f"""#!/bin/bash
#SBATCH --job-name="combined_cmd_gamd"
#SBATCH --output="combined_cmd_gamd.%j.%N.out"
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=50G
#SBATCH --account=ahnlab
#SBATCH --partition=gpu-ahn
#SBATCH --no-requeue
#SBATCH --mail-user=tchettri@ucdavis.edu
#SBATCH --mail-type=ALL
#SBATCH -t 360:00:00

module load cuda/11.8.0
module load gromacs/2024

gmx_mpi grompp -f umbrella.mdp -c npt{frame_name}.gro -t npt{frame_name}.cpt -p single2_large.top -r npt{frame_name}.gro -n rbd_2_reg.ndx -o umbrella{frame_name}.tpr -maxwarn 2
srun gmx_mpi mdrun -deffnm umbrella{frame_name} -nb gpu -bonded gpu
"""

    with open(os.path.join(output_dir, "srun_pull.sh"), 'w') as f:
        f.write(srun_pull_content)
    
    with open(os.path.join(output_dir, "srun_umbrella.sh"), 'w') as f:
        f.write(srun_umbrella_content)

def generateFilesForNewFrames(template_files, additional_files):
    """Generate output files for each new frame using the provided template files."""
    for frame in new_configs:
        output_dir = f"conf{frame}"  # Directory named after the frame, e.g., conf824, conf830, etc.
        for template_file in template_files:
            createOutputFile(template_file, frame, output_dir, search_string="XXX")
        copyAdditionalFiles(output_dir, additional_files)
        copyCorrespondingGroFile(frame, output_dir)
        createSrunScripts(frame, output_dir)

# Example usage
if __name__ == "__main__":
    # List of template files (e.g., 'npt_umbrella.mdp', 'umbrella.mdp')
    template_files = ['npt_umbrella.mdp', 'umbrella.mdp']  # replace with your actual template files
    
    # List of additional files to copy (e.g., 'single2_large.top', 'rbd_2_reg.ndx')
    additional_files = ['single2_large.top', 'rbd_2_reg.ndx']  # replace with your actual additional files
    
    # Generate the files and directories for new frames
    generateFilesForNewFrames(template_files, additional_files)
