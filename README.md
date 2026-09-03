# Precision Functional Mapping Workshop materials for the flux 2026 Meeting

This workshop provides a hands-on introduction to several practical considerations in precision functional mapping (PFM). Rather than focusing only on the final outputs of a PFM analysis, the exercises are designed to demonstrate how those outputs are affected by decisions made during data collection, processing, and quality assessment. We hope that this workshop will give attendees some tools and a starting point for working with PFM data in the future. 

The workshop is organized into three hands-on sections:

1. [Exercise 1: Reliability](#exercise-1-reliability)
2. [Exercise 2: Network Identification](#exercise-2-network-identification)
3. [Exercise 3: Quality Assessment](#exercise-3-quality-assessment)

Each section includes example data and resources that can be used to work through the exercises.

General or additional resources can be found here: [Workshop Resources](#workshop-resources)

# Before the workshop (please do this if you plan to follow along in real time!):

Please do the following if you haven't worked with neuroimaging data in Python before:
1. Download the workshop files.
   - Either click the green "Code" button at the top of this page, then in the dropdown, click "Download ZIP" or git clone if you already use Github.
2. Install miniconda based on your OS: https://docs.conda.io/en/latest/miniconda.html
3. Open terminal (on Mac) or Anaconda/Miniconda Prompt (Windows).
   - On Mac: Open spotlight search at the top bar and type in terminal (click to launch).
   - On Windows: Open Anaconda Prompt or Miniconda Prompt via the start menu.
4. Create a workshop environment in Terminal/Anaconda or Miniconda Prompt by entering the following command:

   ```conda create -n FluxPFMWorkshop2026 python=3.11```
   
6. Then activate the environment and get the required packages by entering the following command in Terminal/Anaconda or Miniconda Prompt.

   ```conda activate FluxPFMWorkshop2026```

   ```conda install -c conda-forge jupyter numpy pandas scipy matplotlib nibabel```

8. Check that you can launch Jupyter notebook, by entering the following commands in Terminal/Anaconda or Miniconda Prompt.

   ```cd ~/Downloads/FluxPFMWorkshop2026```

   Note: cd (change directory) to wherever you have placed the workshop folder, which could potentially be in your iCloud or OneDrive depending on your default download settings.

   ```jupyter lab```

10. In Jupyter, make sure that the notebook is using the FluxPFMWorkshop2026 kernel.
   If needed, select: Kernel -> Change Kernel -> FluxPFMWorkshop2026

If you close out of Jupyter, you can launch this again by running steps 6 and 7.

---

# Exercise 1: Reliability

Individual-level functional connectivity estimates depend heavily on the amount of data available. In this section, we will explore how connectivity estimates change as additional data are included and why collecting sufficient data is particularly important for precision functional mapping.

The goal is to move beyond thinking about reliability as a single number and instead directly observe how an individual's functional connectivity estimates stabilize as more data are added.

## Calculating reliability of functional connectivity using PFM data. 

This method is based on previously published work in Laumann et al. 2015, Gordon et al. 2017 and others. You can also generate ICC as well, but this needs to be run on a cluster because of the compute demands. We are using Pearson's R as previously published for the workshop as these estimates run quickly.
![Alt Text](/01_Reliability/notebooks/images/cPFM_reliability.svg)

## Connectivity and reliability using repeated sampling (8 sessions)

We will begin by examining functional connectivity and reliability calculated using 8 sessions of good (post-motion censored at .2 FD) data from one participant in the [child Precision Functional Mapping (cPFM) dataset](#workshop-resources). Our default settings are using 60 minutes for our high confidence subset, and using the remaining data for our test subset.

### Files and Resources
> **Exercise 1 files:** [Exercise 1: folder](https://github.com/Greene-Lab/FluxPFMWorkshop2026/tree/main/01_Reliability)

---

## How Much Data Is Enough?

Next, we will compare reliability estimates generated from an example of more "standard" amounts of resting state fMRI data (5-15 minutes of high confidence data).

The purpose of this exercise is to directly visualize how functional connectivity estimates change as more data are included.

<img src="/01_Reliability/notebooks/images/truetime.png" width="500">

---

## Iterations and Sampling Variability

Using the same amount of data does not necessarily produce the same result every time.

We will repeat the analysis using different subsets or iterations of the available data and examine how the resulting connectivity estimates change from iteration to iteration.

This exercise highlights the variability that can occur from moment to moment and how the specific samples of data can impact reliability. This emphasizes why estimates with more data show a more generalizable picture of an individual's connectivity.

<img src="/01_Reliability/notebooks/images/rands.png" width="500">

---

## Optional: Intraclass Correlation

If computational requirements allow, we may also calculate intraclass correlation (ICC) locally for an example participant.

This exercise would provide a quantitative complement to the visual reliability comparisons above.

---

# Exercise 2: Network Identification

Precision functional mapping allows functional networks to be accurately identified within individual participants, rather than relying exclusively on group-average network definitions. These group average networks often attribute connectivity from specific regions of an individual's brain to the "incorrect" network. This can add noise to our analyses. 

In this section, we will explore how individual-specific networks are identified using Infomap and how methodological choices—including graph density thresholds and the amount of available data affect the resulting network assignments.

![Alt Text](/02_NetworkID/images/networks_example.png)
![Alt Text](/02_NetworkID/images/connectivity_example.png)

### Files and Resources
> **Exercise 2 files:** [UCSD OneDrive Share](https://ucsdcloud-my.sharepoint.com/:f:/g/personal/greene-lab_ucsd_edu/IgDGiIjyJqF_SKeGlxs17LH_AQp5ZDRoLXhGPziV59X8Uro)
> 

## Exploring Infomap Thresholds

We will begin by examining network assignments generated across different Infomap thresholds.

The goal is to develop an intuition for how thresholding changes the graph used for community detection and, consequently, the resulting network assignments.

We will examine Infomap outputs derived from density thresholds ranging from extremely sparse graphs to increasingly dense graphs and discuss how these densities affect the resulting network solution.

**Topics covered:**

- What an Infomap threshold represents
- Network assignments at sparse thresholds
- Network assignments at increasingly dense thresholds
- How threshold choice influences the resulting network assignment

---

## Initial Workbench Setup

1. Open Connectome Workbench Viewer
   - wb_view either in the search bar or terminal
   - click cancel on recent files window
2. Load surface files
   - File -> Open File
   - Change "Files of type" at bottom to "Any file"
   - Browse to your files downloaded from the [UCSD OneDrive Share](https://ucsdcloud-my.sharepoint.com/:f:/g/personal/greene-lab_ucsd_edu/IgDGiIjyJqF_SKeGlxs17LH_AQp5ZDRoLXhGPziV59X8Uro)
   - Choose the following two files and click open:
        - Conte69.R.inflated.32k_fs_LR.surf.gii
        - Conte69.L.inflated.32k_fs_LR.surf.gii
3. Load Network Map
   - File -> Open File
   - Browse to same downloaded folder
   - Choose the following file and click open:
      - sub-cPFM05_Final_Network_Map.dscalar.nii
4. Repeat the process above and load the following files
   - sub-cPFM05_0.2FDcens_6.0mmSmoothed_Left_Cortex_Only.dtseries.nii
   - sub-cPFM05_Infomap_Raw_Assignment.dtseries.nii
     
   (BELOW ARE OPTIONAL)
   - sub-cPFM05_0.2FDcens_6.0mmSmoothed_Left_Cortex_Only_5min_crop.dtseries.nii
   - sub-cPFM05_0.2FDcens_6.0mmSmoothed_Left_Cortex_Only_10min_crop.dtseries.nii
   - sub-cPFM05_0.2FDcens_6.0mmSmoothed_Left_Cortex_Only_15min_crop.dtseries.nii

---

## Understanding Infomap Assignments Based on Varying Density Thresholds

Network assignments derived from Infomap community detection require connectivity matrices with varying density thresholds. In our work, we use 18 thresholds from .1% to 5%.

By comparing the community assignments created from each density threshold, then choosing a best fit based on all the info across all thresholds, we are able to choose network assignments that are highly accurate for an individual. 

To view how density thresholds impact Infomap community assignments: 

1. Open the following file in Connectome Workbench Viewer
   - sub-cPFM05_Infomap_Raw_Assignment.dtseries.nii
2. Select the file on a layer and click the wrench to change the color palette to "power_surf" to help distinguish between community assignments
---PIC

3. Now scroll through the "Map" layers to see Infomap communities created from the strongest .1% (Map "1 seconds") to strongest 5% (Map "18 seconds") functional connections. 

--- PIC opf MAP

-- PIC OF .1% PIC OF 5%







---

# Workshop Resources

[cPFM Dataset](https://openneuro.org/datasets/ds007196)

[Connectome Workbench](https://www.humanconnectome.org/software/connectome-workbench)





we can put citations and maybe links or stuff that doesn't fit above here. 

