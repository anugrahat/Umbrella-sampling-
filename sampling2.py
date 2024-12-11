import os
import re
import shutil

def readSampledFrames(file_path):
    """
    Read the sampled frames file which contains lines like 'conf0', 'conf467', etc.
    """
    with open(file_path, 'r') as file:
        frames = [line.strip() for line in file.readlines()]
    return frames

def createOutputFile(template_file, frame_name, output_dir, search_string="XXX"):
    """
    Look for instances of the search string in a template file and replace with
    the frame name in a new file inside the specified directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    out_file = os.path.join(output_dir, template_file)

    # Read the contents of the template file
    with open(template_file, 'r') as f:
        file_contents = f.read()

    # Write out the template file contents, replacing all instances of 
    # the search string with the frame name
    with open(out_file, 'w') as f:
        f.write(re.sub(search_string, frame_name, file_contents))

def copyAdditionalFiles(frame_name, output_dir, additional_files):
    """
    Copy additional files into the output directory.
    """
    for file in additional_files:
        if os.path.exists(file):
            shutil.copy(file, output_dir)
        else:
            print(f"Warning: {file} not found. Skipping this file.")

def copyCorrespondingGroFile(frame_name, output_dir):
    """
    Copy the corresponding .gro file into the output directory.
    """
    gro_file = f"{frame_name}.gro"
    if os.path.exists(gro_file):
        shutil.copy(gro_file, output_dir)
    else:
        print(f"Warning: {gro_file} not found. Skipping this file.")

def createSrunScripts(frame_name, output_dir):
    """
    Create the srun_pull.sh and srun_umbrella.sh scripts with modified content based on the frame name.
    """
    srun_pull_content = f"""#!/bin/bash
#SBATCH --job-name="combined_cmd_gamd"
#SBATCH --output="combined_cmd_gamd.%j.%N.out"
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=50G
#SBATCH --account= #enter account#
#SBATCH --partition=#enter partition name#
#SBATCH --no-requeue
#SBATCH --mail-type=ALL
#SBATCH -t 360:00:00
module load cuda/11.8.0

module load gromacs/2024

gmx_mpi grompp -f npt_umbrella.mdp -c {frame_name}.gro -p single2_large.top -r {frame_name}.gro -n rbd_2_reg.ndx -o npt{frame_name[4:]}.tpr -maxwarn 2
srun gmx_mpi mdrun -deffnm npt{frame_name[4:]} -nb gpu -bonded gpu """

    srun_umbrella_content = f"""#!/bin/bash
#SBATCH --job-name="combined_cmd_gamd"
#SBATCH --output="combined_cmd_gamd.%j.%N.out"
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=50G
#SBATCH --account= #enter account#
#SBATCH --partition=#enter partition name#
#SBATCH --no-requeue
#SBATCH --mail-type=ALL
#SBATCH -t 360:00:00

module load cuda/11.8.0

module load gromacs/2024

gmx_mpi grompp -f umbrella.mdp -c npt{frame_name[4:]}.gro -t npt{frame_name[4:]}.cpt -p single2_large.top -r npt{frame_name[4:]}.gro -n rbd_2_reg.ndx -o umbrella{frame_name[4:]}.tpr -maxwarn 2
srun gmx_mpi mdrun -deffnm umbrella{frame_name[4:]} -nb gpu -bonded gpu 
"""

    with open(os.path.join(output_dir, "srun_pull.sh"), 'w') as f:
        f.write(srun_pull_content)
    
    with open(os.path.join(output_dir, "srun_umbrella.sh"), 'w') as f:
        f.write(srun_umbrella_content)

def generateFilesForSampledFrames(sampled_frames_file, template_files, additional_files):
    """
    Generate output files for each frame in the sampled_frames_file using the provided template file.
    Each frame gets its own directory, and additional files are copied into the directory.
    """
    frames = readSampledFrames(sampled_frames_file)
    
    print("Creating frame-specific directories and output files:")
    
    for frame in frames:
        output_dir = frame  # Directory named after the frame, e.g., conf0, conf467, etc.
        for template_file in template_files:
            createOutputFile(template_file, frame, output_dir, search_string="XXX")
        copyAdditionalFiles(frame, output_dir, additional_files)
        copyCorrespondingGroFile(frame, output_dir)
        createSrunScripts(frame, output_dir)

# Example usage
if __name__ == "__main__":
    # Define the path to your sampled frames file
    sampled_frames_file = 'sampled_frames.txt'
    
    # List of template files (e.g., 'npt_umbrella.mdp', 'umbrella.mdp')
    template_files = ['npt_umbrella.mdp', 'umbrella.mdp']  # replace with your actual template files
    
    # List of additional files to copy (e.g., 'single2_large.top', 'rbd_2_reg.ndx')
    additional_files = ['single2_large.top', 'rbd_2_reg.ndx']  # replace with your actual additional files
    
    # Generate the files and directories
    generateFilesForSampledFrames(sampled_frames_file, template_files, additional_files)
