#!/bin/bash

#SBATCH --job-name=md1                 # Job name
#SBATCH --account=ahnlab               # Account name
#SBATCH --partition=gpu-ahn            # Partition name
#SBATCH --nodes=1                      # Number of nodes
#SBATCH --ntasks-per-node=1            # Number of tasks per node (usually 1 for GPU jobs)
#SBATCH --cpus-per-task=64             # Number of CPU cores per task (adjust if needed, but <= 64 for GROMACS recommendation)
#SBATCH --gres=gpu:0                   # Request 1 GPU
#SBATCH --time=250:00:00               # Time limit hrs:min:sec
#SBATCH --mail-type=BEGIN,END          # Send email at start and end of job
#SBATCH --mail-user=anuthyagatur@ucdavis.edu # Your email address

# Load GROMACS module
module load gromacs/2024

# Create the output directory if it doesn't exist
mkdir -p US

#################################################
# get_distances.sh
#
#   Script iteratively calls gmx distance and
#   assembles a series of COM distance values
#   indexed by frame number, for use in
#   preparing umbrella sampling windows.
#
# Written by: Justin A. Lemkul, Ph.D.
#    Contact: jalemkul@vt.edu
#
#################################################

#echo 0 | gmx trjconv -s replica2.tpr -f replica2.xtc -o US/conf.gro -sep

# Compute distances
for (( i=0; i<5001; i++ ))
do
    gmx distance -s replica2.tpr -f US/conf${i}.gro -n rbd_2_reg.ndx -select 'com of group "chauA" plus com of group "rest"' -oall US/dist${i}.xvg 
done

# Compile summary
touch US/summary_distances.dat
for (( i=0; i<5001; i++ ))
do
    d=`tail -n 1 US/dist${i}.xvg | awk '{print $2}'`
    echo "${i} ${d}" >> US/summary_distances.dat
    rm US/dist${i}.xvg
done

exit;
