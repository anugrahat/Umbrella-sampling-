#!/bin/bash
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

# Loop over all directories matching the pattern "conf*"
for dir in conf*; do
  # Check if it is indeed a directory
  if [ -d "$dir" ]; then
    # Navigate into the directory
    cd "$dir"

    # Check if srun_umbrella.sh exists
    if [ -f "srun_umbrella.sh" ]; then
      # Submit the job using sbatch
      sbatch srun_umbrella.sh
      echo "Submitted job for $dir"
    else
      echo "srun_umbrella.sh not found in $dir, skipping..."
    fi

    # Go back to the parent directory
    cd ..
  else
    echo "$dir is not a directory, skipping..."
  fi
done
