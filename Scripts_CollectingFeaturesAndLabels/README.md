## [`/Code_CollectFeatures/`](https://github.com/sticeran/SnoringNoise/tree/master/Scripts_CollectingFeaturesAndLabels/Code_CollectFeatures/)
is the program code for collecting data set metrics.  
we use the same 16 well-defined product and project metrics as in the literature [1].

### Note that
[`/versionTag/`](https://github.com/sticeran/SnoringNoise/tree/master/Scripts_CollectingFeaturesAndLabels/versionTag/)
this folder stores the release numbers to be collected for each project.  
Before collecting a data set, it is needed to set the target release numbers in a target project to be collected.
For each project, the set target release numbers is stored in the versionTag.txt under the "versionTag" folder.  
Product and project metrics are not collected for the initial (minimum) release in the versionTag.txt of each project.
The initial release serves as a cutoff point, and the release time is used to collect metrics for the next release.

## [`/Code_CollectLabels/`](https://github.com/sticeran/SnoringNoise/tree/master/Scripts_CollectingFeaturesAndLabels/Code_CollectLabels/)
is the program code for collecting data set labels.  
For our newly collected 8 Apache projects, we used our reproduced MA-SZZ [2] approach , the state-of-the-art SZZ variant, to collect defect labels.
Because previous studies reported that defect labels collected by the MA-SZZ approach had the highest (higher) accuracy and generated fewer mislabels.

### Note that
[`/issue_reports/`](https://github.com/sticeran/SnoringNoise/tree/master/Scripts_CollectingFeaturesAndLabels/issue_reports/)
this folder stores the issue reports downloaded for each project.

## References
[1]	D. Falessi, A. Ahluwalia, M.D. Penta. The impact of dormant defects on defect prediction: a study of 19 apache projects. ACM Transactions on Software Engineering and Methodology, 31 (4), 2022: 1–26.
[2]	D.A. Costa, S. McIntosh, W. Shang, U. Kulesza, R. Coelho, A.E. Hassan. A framework for evaluating the results of the SZZ approach for identifying bug-introducing changes. IEEE Transactions on Software Engineering, 43(7), 2017: 641-657.  