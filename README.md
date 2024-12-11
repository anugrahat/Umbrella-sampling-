Here's a step-by-step guide for submitting and running the umbrella sampling and WHAM workflow scripts:

---

### **Step 1: Prepare Distances**
1. **Submit the `extract.sh` script:**
   - This script calculates the distances between specified groups for umbrella sampling.
   ```bash
   sbatch extract.sh
   ```

---

### **Step 2: Sample Frames**
1. **Run the `sampling.py` script:**
   - This script reads the distances computed from Step 1 and samples frames to create umbrella sampling windows.
   ```bash
   python sampling.py
   ```

2. **Output:**
   - A file named `sampled_frames.txt` containing the selected frames.

---

### **Step 3: Generate Configuration Files**
1. **Run `sampling2.py`:**
   - These scripts set up configuration directories, copy necessary files, and create submission scripts (`srun_pull.sh` and `srun_umbrella.sh`) for each frame.
   ```bash
   python sampling2.py
   ```

2. **Output:**
   - Directories named `conf<frame_number>` (e.g., `conf981`) with necessary input files and job submission scripts.

---

### **Step 4: Submit Umbrella Sampling Simulations**
1. **Submit batch jobs for the simulations:**
   - Use `submit_all_extras.sh` or `submit_all_umbrella.sh` to submit jobs for all configurations.
   
   ```bash
   sbatch submit_all_umbrella.sh
   ```

2. **Monitor the progress of the submitted jobs:**
   - Use the `squeue` command to check job statuses:
     ```bash
     squeue -u <your_username>
     ```

---

### **Step 5: WHAM Analysis**
1. **Prepare Input Files:**
   - Use `wham.py` or `wham2.py` to generate the `tpr-files.dat` and `pullf-files.dat` files required for WHAM.
   ```bash
   python wham.py
   ```

2. **Submit the WHAM job:**
   - Run `wham.sh` to calculate the free energy profile using WHAM.
   ```bash
   sbatch wham.sh
   ```

3. **Output:**
   - Files containing the free energy profile (`-o`) and histogram (`-hist`) from WHAM.

---

### **Step 6: Visualize Results**
1. **Use `histo.py` to plot results:**
   - Visualize the reaction coordinate distribution and free energy profile.
   ```bash
   python histo.py
   ```

---

### **Quick Checklist**
- **Submit these scripts in order:**
  1. `extract.sh` (via `sbatch`)
  2. `sampling.py` (via Python)
  3. `sampling_1extras.py` or `sampling2.py` (via Python)
  4. `submit_all_extras.sh` or `submit_all_umbrella.sh` (via sbatch)
  5. `wham.py` or `wham2.py` (via Python)
  6. `wham.sh` (via `sbatch`)
  7. Visualize results with `histo.py` (via Python).

This order ensures all dependencies are correctly set up and that results are processed and visualized systematically.
