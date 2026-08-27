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
3. Install miniconda based on your OS: https://docs.conda.io/en/latest/miniconda.html
4. Open terminal (on Mac) or Anaconda/Miniconda Prompt (Windows).
   - On Mac: Open spotlight search at the top bar and type in terminal (click to launch).
   - On Windows: Open Anaconda Prompt or Miniconda Prompt via the start menu.
5. Create a workshop environment in Terminal/Anaconda or Miniconda Prompt by entering the following command:
   - conda create -n FluxPFMWorkshop2026 python=3.11
6. Then activate the environment and get the required packages by entering the following command in Terminal/Anaconda or Miniconda Prompt.
   - conda activate FluxPFMWorkshop2026
   - conda install -c conda-forge jupyter numpy pandas scipy matplotlib nibabel
7. Check that you can launch Jupyter notebook, by entering the following commands in Terminal/Anaconda or Miniconda Prompt.
   - cd ~/Downloads/FluxPFMWorkshop2026
       - Note: cd (change directory) to wherever you have placed the workshop folder, which could potentially be in your iCloud or OneDrive depending on your default download settings.
   - jupyter lab
8. In Jupyter, make sure that the notebook is using the FluxPFMWorkshop2026 kernel.
   If needed, select: Kernel -> Change Kernel -> FluxPFMWorkshop2026

If you close out of Jupyter, you can launch this again by running steps 4 and 5.

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

Then discuss differences here.....

*** maybe put the instructions to the notebook here?? add the cell or something?

---

# Exercise 2: Network Identification



Precision functional mapping allows functional networks to be accurately identified within individual participants, rather than relying exclusively on group-average network definitions. These group average networks often attribute connectivity from specific regions in an individual's brain to the "incorrect" network. This can obviously add noise to our analyses. 

In this section, we will explore how individual-specific networks are identified using Infomap and how methodological choices—including graph density thresholds and the amount of available data—affect the resulting network assignments.

## Exploring Infomap Thresholds

We will begin by examining network assignments generated across different Infomap thresholds.

The goal is to develop an intuition for how thresholding changes the graph used for community detection and, consequently, the resulting network assignments.

We will examine thresholds ranging from extremely sparse graphs to increasingly dense graphs and compare the resulting network solutions.

**Topics covered:**

- What an Infomap threshold represents
- Network assignments at sparse thresholds
- Network assignments at increasingly dense thresholds
- How threshold choice influences the resulting network assignment

### Files and Resources

> **Workshop files:** [Infomap threshold resources](LINK_HERE)

---

## Comparing Networks with Raw Functional Connectivity

A network assignment should not be evaluated solely by looking at the network map itself.

We will overlay or compare identified networks with the participant's underlying functional connectivity patterns. This provides an important quality-assessment step for determining whether the assigned network organization is supported by the participant's actual connectivity data.

**Topics covered:**

- Viewing individual-specific network assignments
- Examining raw connectivity patterns
- Comparing network boundaries and assignments with connectivity
- Using raw connectivity as a PFM quality-assessment tool

### Files and Resources

> **Workshop files:** [Network/connectivity comparison resources](LINK_HERE)


---

## How Data Quantity Affects Network Identification

We will repeat the network-identification procedure using substantially less data.

For example, networks can be generated using only approximately 5–10 minutes of data and compared with networks generated using the participant's complete dataset.

Participants can then repeat the connectivity-overlap exercise above to determine whether network assignments derived from limited data remain well supported by the underlying connectivity patterns.

### Files and Resources

> **Workshop files:** [Limited-data Infomap resources](LINK_HERE)

---

## Single-Session Infomap

As an additional demonstration, we will rerun Infomap using data from only one session and compare the resulting network assignments with those obtained using the complete dataset.

> **Workshop development note:** Identify a participant/example with particularly clear full-data network organization for this exercise.

### Files and Resources

> **Workshop files:** [Single-session Infomap resources](LINK_HERE)




---

# Exercise 3: Quality Assessment

Precision functional mapping depends on the quality of the data used to generate individual-level estimates. Quality assessment therefore involves more than simply determining whether a processing pipeline completed successfully.

In this section, we will examine several approaches for evaluating data quality and explore how decisions about motion, individual runs, and surface alignment can influence PFM results.

## PFM Quality-Assessment Outputs

We will begin by reviewing example quality-assessment outputs and discussing how they can be used to evaluate individual-level data and results.

This section will include outputs from a tool developed by Chuck Lynch and examples of how these measures can be incorporated into a PFM workflow.

**Topics covered:**

- Interpreting PFM QA outputs
- Identifying potential problems in individual datasets
- Connecting QA metrics with the resulting functional connectivity and network estimates

### Files and Resources

> **Workshop files:** [PFM QA resources](LINK_HERE)

---

## Chuck's tool outputs

something about what the tool does here and the main outputs

- we should go through the outputs here. 

### Files and Resources

> **Workshop files:** [Border correctness resources](LINK_HERE)

---

## Motion and Individual Runs

Motion can vary substantially across runs within the same participant.

We will examine motion plots from individual runs and use **cPFM08** ??? as an example of a participant containing particularly noisy runs.

We will compare results generated from:

1. The complete dataset
2. The dataset after removing selected high-motion or otherwise poor-quality runs

The corresponding `dtseries` files will be provided so that participants can directly compare the effect of removing these runs on downstream results.

**Topics covered:**

- Reading run-level motion plots
- Identifying unusually noisy runs
- Comparing full-data results with results after run removal
- Determining when individual runs may meaningfully affect PFM estimates

### Files and Resources here??


---

## Framewise Displacement Thresholds and Motion Floors

Finally, we will discuss how framewise displacement (FD) thresholds are used when determining which data should be retained.

We will examine the consequences of different FD thresholds and discuss the concept of motion floors in the context of precision functional mapping.

**Topics covered:**

- Framewise displacement
- Choosing an FD threshold
- How censoring decisions affect the amount of usable data
- Motion floors
- Balancing data quantity and data quality in individual-level analyses

### Files and Resources

what files here???


---

# Workshop Resources

[cPFM Dataset](https://openneuro.org/datasets/ds007196)

[Connectome Workbench](https://www.humanconnectome.org/software/connectome-workbench)





we can put citations and maybe links or stuff that doesn't fit above here. 
