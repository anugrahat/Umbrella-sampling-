import os

# Base directory path
base_dir = "/home/anugraha/AAT_2023/human_newly_glycosylated_hu_AAT_hu_elastaste/charmm-gui-1691695038/gromacs/Pulling_replica2/replica_3/US/"

# List of folders to check
folders = [
    "conf0", "conf467", "conf573",   "conf595", "conf623", "conf637", "conf638", "conf667", "conf726",  "conf805",  
     "conf953", "conf954","conf960", "conf967", "conf970", "conf976", "conf981", "conf993", 
    "conf1011", "conf1088", "conf1173", "conf1316", "conf1385", 
    "conf1553", "conf1696", "conf1869", "conf2091", "conf2254", 
    "conf2391", "conf2574", "conf2694", "conf2815", "conf2970", 
    "conf3080", "conf3189", "conf3316", "conf3463", "conf3614", 
    "conf3833", "conf3987", "conf4252", "conf4292", "conf4505", 
    "conf4629", "conf4794"
  
]

tpr_files = []
pullf_files = []

# Iterate through each folder
for folder in folders:
    folder_path = os.path.join(base_dir, folder)
    umbrella_number = folder.split('conf')[1]
    pullf_file = f"umbrella{umbrella_number}_pullf.xvg"
    tpr_file = f"umbrella{umbrella_number}.tpr"
    
    pullf_file_path = os.path.join(folder_path, pullf_file)
    tpr_file_path = os.path.join(folder_path, tpr_file)
    
    # Check if both files exist
    if os.path.exists(pullf_file_path) and os.path.exists(tpr_file_path):
        tpr_files.append(tpr_file_path)
        pullf_files.append(pullf_file_path)

# Write the full paths of .tpr filenames to tpr-files.dat
with open('tpr-files.dat', 'w') as tpr_f:
    for tpr_file in tpr_files:
        tpr_f.write(f"{tpr_file}\n")

# Write the full paths of .xvg filenames to pullf-files.dat
with open('pullf-files.dat', 'w') as pullf_f:
    for pullf_file in pullf_files:
        pullf_f.write(f"{pullf_file}\n")

print("tpr-files.dat and pullf-files.dat have been created with the full file paths.")
