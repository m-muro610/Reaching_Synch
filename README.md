# Reaching_Synch
This repository contains the analysis code used in a paper **"Cooperation Enhances Social Presence Despite Reduced Movement Synchrony."**
The code computes the following synchrony measures from time serise of movements recorded from two particpants.

## Requirements
To run this code, you need to install the `sklearn-learn` (`sklearn`) and `pingouin` packages. Several other commonly used Python packages are also required. Please refer to the import statements in the source code for the complete list of dependencies.

## Synchrony measures used in this analysis
- Pearson’s correlation
- Cross-correlation
- Coherence
- Phase-Locking Value (PLV)
- Circular correlation coefficient ($\rho$)
- Mutual information

## Data Structure
This code assumes the directory structre of the shared dataset described below.  
Synchrony measures are computed from two time series stores in two columns of each CSV file, specified in lines 59 and 60 if the source code. The computations are performed for every combination of **dyad $\times$ block $\times$ trial**. You can modify the ranges of the three `for` loops to change the numbers of dyads, blocks, and trials to be processed. The input file name and path can be modified in line 57.

# Data Availability
The dataset used in this study is available on figshare:  
*[The URL will be added after the paper is accepted.]*

## General Information
- **Contact:** Miki Matsumuro (miki.matsumuro@jp.honda-ri.com)
- **Institution:** Research Organization of Open Innovation and Collaboration, Ritsumeikan University, Ibaraki, 567-8570 JAPAN<br>
Honda Research Institute Japan Co., Ltd., Wako, 351-0188, Japan

## Sharing & Reuse Conditions
- **License:** MIT
- **Citation:** *Will be updated after the paper is accepted*