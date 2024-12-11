import pandas as pd
import matplotlib.pyplot as plt

# Define file paths for histo.xvg and profile.xvg
histo_file_path = 'histo.xvg'
profile_file_path = 'profile.xvg'

# Read histo.xvg file, skipping the first 17 rows
histo_data = pd.read_csv(histo_file_path, delim_whitespace=True, comment='@', header=None, skiprows=17)

# Read profile.xvg file, also skipping the first 17 rows
profile_data = pd.read_csv(profile_file_path, delim_whitespace=True, comment='@', header=None, skiprows=17)

# The first column is the reaction coordinate (X-axis) for both files
x_histo = histo_data.iloc[:, 0]
x_profile = profile_data.iloc[:, 0]

# Select the Y columns from 2 to 24 (index 1 to 23 in Python) for histo
y_histo_columns = histo_data.iloc[:, 1:24]

# The second column in profile.xvg (index 1 in Python) is the profile Y values
y_profile = profile_data.iloc[:, 1]

# Create the stacked plot
fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

# Plot histo.xvg data
for col in y_histo_columns.columns:
    axs[0].plot(x_histo, y_histo_columns[col], color='black')  # Set line color to black

axs[0].set_facecolor('white')  # Set plot background color to white
axs[0].set_ylabel('Distribution')
axs[0].set_title('Reaction Coordinate vs. Distribution (histo.xvg)')
axs[0].grid(False)  # Disable grid

# Plot profile.xvg data
axs[1].plot(x_profile, y_profile, color='black')  # Set line color to black
axs[1].set_facecolor('white')  # Set plot background color to white
axs[1].set_xlabel('Reaction Coordinate')
axs[1].set_ylabel('Profile')
axs[1].set_title('Reaction Coordinate vs. Profile (profile.xvg)')
axs[1].grid(False)  # Disable grid

# Adjust layout and show the plot
plt.tight_layout()
plt.show()
