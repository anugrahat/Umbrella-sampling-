import numpy as np

# Parameters
input_file = 'summary_distances.dat'
output_file = 'sampled_frames.txt'
start_distance = 4.834  # nm
end_distance = 9.784
   # nm
step_distance = 0.15  # nm

# Read the data from the file
data = np.loadtxt(input_file)

# Extract the frame numbers and COM distances
frame_numbers = data[:, 0].astype(int)
com_distances = data[:, 1]

# Initialize variables
sampled_frames = []
sampled_distances = []
current_distance = start_distance

# Sampling loop
while current_distance <= end_distance:
    # Find the index of the closest COM distance to the current target distance
    idx = np.where((com_distances >= current_distance) & (com_distances < current_distance + step_distance))[0]
    
    if len(idx) > 0:
        sampled_frames.append(frame_numbers[idx[0]])
        sampled_distances.append(com_distances[idx[0]])

    # Move to the next target distance
    current_distance += step_distance

# Remove duplicates
unique_sampled_frames = []
for i, frame in enumerate(sampled_frames):
    if frame not in unique_sampled_frames:
        unique_sampled_frames.append(frame)

# Write the sampled frame numbers to the output file
with open(output_file, 'w') as f:
    for frame in unique_sampled_frames:
        f.write(f'conf{frame}\n')

print(f"Sampling complete. Output written to {output_file}")
