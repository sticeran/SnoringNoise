# The replication toolkit for the paper "Don’t worry, we’ll get there: developing defect prediction models insensitive to snoring noise"

## Titile: Don’t worry, we’ll get there: developing defect prediction models insensitive to snoring noise

Our work aim to explore easy-to-use modeling techniques, instead of the training data refinement approach, to mitigate the negative influence of snoring noise in a training set. We propose simple modeling techniques to build five snoring-noise-insensitive defect prediction models: LOC, LOC-N, FEATURE, FEATURE-N, and FEATURE-LOC. In view of the effectiveness and simplicity of these models, we suggest using them as easy-to-implement baselines in future studies to demonstrate the usefulness of any newly proposed snoring-noise mitigation approaches.

## Quick Start

### (1) [`/DataSets/`](https://github.com/sticeran/SnoringNoise/tree/master/DataSets/) Our defect data sets consists of two groups, the first one is the open-source defect data sets from the literature [1], and the second one is our newly collected defect data set from 8 Apache projects. Please refer to the [`/DataSets/README.md`](https://github.com/sticeran/SnoringNoise/tree/master/DataSets/README.md) for details.

### (2) [`/Scripts_CollectingFeaturesAndLabels/`](https://github.com/sticeran/SnoringNoise/tree/master/Scripts_CollectingFeaturesAndLabels/) In this folder, the folder Code_CollectFeatures holds the feature collection scripts we implemented and the folder Code_CollectLabels holds the defect label collection scripts we implemented. Please refer to the [`/Scripts_CollectingFeaturesAndLabels/README.md`](https://github.com/sticeran/SnoringNoise/tree/master/Scripts_CollectingFeaturesAndLabels/README.md) for details.

### (3) [`/SnoringNoiseProgram/`](https://github.com/sticeran/SnoringNoise/tree/master/SnoringNoiseProgram/) This folder holds the experimental programs for reproducing the experimental results in RQ1, RQ2 and Discussions. Please refer to the [`/SnoringNoiseProgram/README.md`](https://github.com/sticeran/SnoringNoise/tree/master/SnoringNoiseProgram/README.md) to learn how to run the JAR program.


If you use the data set (our newly collected defect data sets for 8 Apache projects) or the program code, please cite our paper "Don’t worry, we’ll get there: developing defect prediction models insensitive to snoring noise", thanks.

## References
[1]	D. Falessi, A. Ahluwalia, M.D. Penta. The impact of dormant defects on defect prediction: a study of 19 apache projects. ACM Transactions on Software Engineering and Methodology, 31 (4), 2022: 1–26.
