## P300 speller Code Repository

Introducing the P300 Speller Code Repository, born from the dynamic energy of the BCI Spring Hackathon on April 27, 2024. Here lies the digital archive of innovation, a testament to the collaborative showcased at the Hackathon 2024 Spring School. 

**Team:** 
> Puneet Tomar [tomarp@pm.me](mailto:tomarp@pm.me)  
> Diptyajit Das 



### Literature
1. **Overview.pdf**
   - Catalog-like overview of datasets.
   - Brief mentions of experimental setup per dataset.

2. **TVLDA_for_P300_Spellers.pdf**
   - Detailed study on the efficacy of TVLDA over LDA in P300 speller BCIs.
   - Comparison of dry and wet electrode performances.
   - Demonstrates significant improvements in training efficiency and accuracy with TVLDA.

### Data File Summaries
Each `.mat` file contains EEG data related to experiments with P300 spellers. Common variables include:
- **Sampling Rate (fs)**: Data captured at a specific frequency in Hz.
- **EEG Data (y)**: Matrix of EEG readings across different channels and samples.
- **Triggers (trig)**: Event markers indicating target vs. nontarget stimuli.

### Statistics for EEG Data Files

| Subject | Mean of EEG | SD of EEG | Max of EEG | Min of EEG | Mean of Triggers | SD of Triggers | 
|------|-------------|----------------|------------|------------|------------------|---------------------|
| S1   | -0.0037     | 14.1825        | 188.633    | -124.138   | -0.0148          | 0.1396              |
| S2   | -0.0072     | 10.0638        | 178.641    | -159.439   | -0.0148          | 0.1397              | 
| S3   | -0.0024     | 11.1392        | 169.020    | -1084.562  | -0.0148          | 0.1395              |
| S4   | 0.1322      | 22.5781        | 108.221    | -124.094   | -0.0148          | 0.1397              |
| S5   | 0.0233      | 17.9733        | 464.175    | -560.267   | -0.0148          | 0.1396              |

- **Mean of EEG**: Average value of the EEG data.
- **Std Dev of EEG**: Standard deviation, indicating the variability of EEG signal.
- **Max of EEG**: Maximum value in the EEG data.
- **Min of EEG**: Minimum value in the EEG data.
- **Mean of Triggers**: Average value of the trigger data.
- **Std Dev of Triggers**: Standard deviation of trigger data.
- **Max of Triggers**: Maximum value (1, indicating a target).
- **Min of Triggers**: Minimum value (-1, indicating a nontarget).


### Dimensions of Data in Each File

| Subject | Data Shape (samples x channels) | Length of Triggers |
|------|:-------------------------------------:|:--------------------:|
| S1   | 60871 x 8                           | 60871              |
| S2   | 60806 x 8                           | 60806              |
| S3   | 60955 x 8                           | 60955              |
| S4   | 60782 x 8                           | 60782              |
| S5   | 60855 x 8                           | 60855              |

> Each file contains data for 8 channels, with the number of samples indicating the length of recording time, which corresponds directly to the number of trigger points. This setup is typical for EEG recordings where each sample tagged with a trigger indicating different experimental conditions.

## Pipeline




## Results

