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
