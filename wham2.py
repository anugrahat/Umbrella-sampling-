import os

# Base directory path
base_dir = "/home/anugraha/AAT_2023/human_newly_glycosylated_hu_AAT_hu_elastaste/charmm-gui-1691695038/gromacs/Pulling_replica2/replica_3/US/"

tpr_files = []
pullf_files = []

# Iterate through each folder in the base directory
for folder in os.listdir(base_dir):
    # Check if the folder name matches the pattern 'conf$number$'
    if folder.startswith("conf") and folder[4:].isdigit():
        folder_path = os.path.join(base_dir, folder)
        umbrella_number = folder.split('conf')[1]
        pullf_file = f"umbrella{umbrella_number}_pullf.xvg"
        tpr_file = f"umbrella{umbrella_number}.tpr"
        
        pullf_file_path = os.path.join(folder_path, pullf_file)
        tpr_file_path = os.path.join(folder_path, tpr_file)
        
        # Check if both files exist
        if os.path.exists(pullf_file_path) and os.path.exists(tpr_file_path):
            tpr_files.append((umbrella_number, tpr_file_path))
            pullf_files.append((umbrella_number, pullf_file_path))

# Sort the files by umbrella number
tpr_files.sort(key=lambda x: int(x[0]))
pullf_files.sort(key=lambda x: int(x[0]))

# Write the sorted .tpr filenames to tpr-files.dat
with open('tpr-files.dat', 'w') as tpr_f:
    for _, tpr_file in tpr_files:
        tpr_f.write(f"{tpr_file}\n")

# Write the sorted .xvg filenames to pullf-files.dat
with open('pullf-files.dat', 'w') as pullf_f:
    for _, pullf_file in pullf_files:
        pullf_f.write(f"{pullf_file}\n")

print("tpr-files.dat and pullf-files.dat have been created with the full file paths in increasing order.")
