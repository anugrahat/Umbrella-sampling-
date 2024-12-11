#!/bin/bash

#SBATCH --job-name=wham_bootstrap      # Job name
#SBATCH --account=ahnlab               # Account name
#SBATCH --partition=gpu-ahn            # Partition name
#SBATCH --nodes=1                      # Number of nodes
#SBATCH --ntasks-per-node=1            # Number of tasks per node
#SBATCH --cpus-per-task=64             # Number of CPU cores per task
#SBATCH --gres=gpu:0                   # No GPUs needed for WHAM
#SBATCH --time=250:00:00               # Time limit hrs:min:sec
#SBATCH --mail-type=BEGIN,END          # Send email at start and end of job
#SBATCH --mail-user=anuthyagatur@ucdavis.edu # Your email address

# Load required modules
module load gromacs/2024
module load anaconda3/2020.11  # Use Anaconda for Python
gmx_mpi  wham -it tpr-files.dat -if pullf-files.dat -o -hist -unit kCal -nBootstrap 50
