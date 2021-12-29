To run this jar you must hava java and jdk 1.8.0_102 installed on your system.

# Program execution instruction:
java -jar SnoringNoiseProgram.jar Parameter1: DatasetPath Parameter2: DatasetType Parameter3(optional): true or false

Note that the first two parameters are required when running SnoringNoiseProgram.jar.  
The first parameter is the common folder path of all data sets, and the second parameter is the type of data sets (**old** represents the original data sets of the literature [1], and **new** represents our newly collected data sets). The third parameter (optional) is a binary control variable indicating whether to rebalance the training set (**false** means no rebalancing, **true** means rebalancing, default is **false**).

## Directory form of program and required libraries:
![File directory form](https://raw.githubusercontent.com/sticeran/InconsistentLabels/master/RQ2%20and%20RQ3%20experimental%20data%20and%20program/img/File%20directory%20form.png)

## Example of program operation:
![Run command](https://raw.githubusercontent.com/sticeran/InconsistentLabels/master/RQ2%20and%20RQ3%20experimental%20data%20and%20program/img/Run%20command.png)

## References
[1]	D. Falessi, A. Ahluwalia, M.D. Penta. The impact of dormant defects on defect prediction: a study of 19 apache projects. ACM Transactions on Software Engineering and Methodology, 31 (4), 2022: 1–26.