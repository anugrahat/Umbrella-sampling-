#!/bin/bash
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

# Load required modules
module load gromacs/2024
module load anaconda3/2020.11  # Use Anaconda for Python
gmx_mpi  wham -it tpr-files.dat -if pullf-files.dat -o -hist -unit kCal -nBootstrap 50
