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

# List of new configuration directories to process
new_configs=("981" "954" "967" "970" "960")

# Loop over the specified new configuration directories
for config in "${new_configs[@]}"; do
  dir="conf${config}"
  
  # Check if the directory exists
  if [ -d "$dir" ]; then
    # Navigate into the directory
    cd "$dir"

    # Check if srun_pull.sh exists
    if [ -f "srun_pull.sh" ]; then
      # Submit the job using sbatch
      sbatch srun_umbrella.sh
      echo "Submitted job for $dir"
    else
      echo "srun_pull.sh not found in $dir, skipping..."
    fi

    # Go back to the parent directory
    cd ..
  else
    echo "$dir does not exist, skipping..."
  fi
done
