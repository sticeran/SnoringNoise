import os
import re
import pandas as pd
from collections import OrderedDict


#获得每个引入buggy line的提交号和引入时间，修复提交号和修复时间，问题报告的创建时间。并过滤引入时间大于创建时间的引入提交。
if __name__ == "__main__":
    
    projectName_list = ["shiro","maven","flume","mahout","calcite","pdfbox","iotdb","tika"];
    
    #"snoring_labels"用于读取snoring时间节点前的提交日志
    list_labels_type = ["snoringTrain_labels","snoringTest_labels","groundtruth_labels"]
    
    path_common = "D:/workspace/DataFolder/labels_MASZZ";
    
    for project in projectName_list:
        for labels_type in list_labels_type:
            
            path_common_bugid_fixingsha =  '%s/%s/matching_bugid_fixingsha'%(path_common,labels_type);
            path_common_blame = '%s/%s/git_blame_l_from_buggyFileAndLineNum'%(path_common,labels_type);
            path_common_saved = '%s/%s/bugIntroducingTime_and_bugFixingtime'%(path_common,labels_type);
            
            wcsv_list_bugFilename = [];
            wcsv_list_bugIntroducingTime = [];
            wcsv_list_bugFixingTime = [];
            wcsv_list_bugIntroducingCommitsSha = [];
            wcsv_list_bugFixingCommitsSha = [];
            wcsv_list_buggyLine = [];
            wcsv_list_issueReportsCreatedDate = [];
            
            print(project,labels_type,"begin")
            
            path_bugid_fixingsha = path_common_bugid_fixingsha+'/%s_bug_commit_all.csv'%project;
            df_bugid_fixingsha = pd.read_csv(path_bugid_fixingsha);#所有潜在的修复bug的commits号和修复时间，以及问题报告的创建时间
            df_bugid_fixingsha.fillna('-1',inplace=True)
            allLine_fixingsha = df_bugid_fixingsha['commitSHA'].tolist();
            project_dir = path_common_blame+'/%s'%project;
            fileNames_bugIntroducingCommits = os.listdir(project_dir);#所有包含有效修改行的修复bug的commits对应的有效修改行信息的文件名
            for str_i_filename in fileNames_bugIntroducingCommits:
                print(str_i_filename)
                tempList = str_i_filename.split('_');
                bugFixingCommits_sha = tempList[0];#修复bug的提交号
                path_i_filename = project_dir + '/%s'%str_i_filename;
                allLine_filename = open(path_i_filename,'r',encoding='UTF-8').readlines();#一个修复bug的commit对应的所有buggy line对应的潜在的引入bug的commits号和引入时间
                for oneLine_filename in allLine_filename:#一行buggy line对应的潜在的引入bug的commits号和引入时间
                    if oneLine_filename == "\n":
                        continue;
                    list_oneLine = oneLine_filename.split(' ');
                    bugIntroducingCommits_sha = list_oneLine[0];#引入bug的提交号
                    bugIntroducingCommits_filename = list_oneLine[1];#引入bug的文件名
                    index_buggyLine = oneLine_filename.index(')');
                    buggyLine = oneLine_filename[index_buggyLine+2:];#buggy line,+2是为了去掉)和一个间隔空格
                    buggyLine = re.sub("(\r|\n)", '', buggyLine)#去掉末尾的换行符
                    index_authorAndTime = oneLine_filename.index('(');
                    authorAndTime = oneLine_filename[index_authorAndTime:index_buggyLine+1];
                    #===过滤引入时间大于创建时间的引入提交===#
                    index_connector = authorAndTime.index('-');
                    authorAndTime = authorAndTime[index_connector-4:];#去掉圆括号里面的作者信息
                    temp_list = authorAndTime.split(' ');
                    time_bugIntroduing = temp_list[0:2];#引入bug的时间
                    str_time_bugIntroduing = ' '.join(time_bugIntroduing)
                    #获取修复bug的commits的修复bug时间，以及问题报告的创建时间
                    index_target = allLine_fixingsha.index(bugFixingCommits_sha);
                    str_time_createdDate = df_bugid_fixingsha.loc[index_target,'createdDate'];#问题报告创建时间
                    str_time_bugFixing = df_bugid_fixingsha.loc[index_target,'fixingDate'];#修复bug的时间
                    if str_time_bugIntroduing <= str_time_createdDate or str_time_createdDate == '-1':
                        wcsv_list_bugFilename.append(bugIntroducingCommits_filename)
                        wcsv_list_bugIntroducingTime.append(str_time_bugIntroduing)
                        wcsv_list_bugFixingTime.append(str_time_bugFixing)
                        wcsv_list_bugIntroducingCommitsSha.append(bugIntroducingCommits_sha)
                        wcsv_list_bugFixingCommitsSha.append(bugFixingCommits_sha)
                        wcsv_list_buggyLine.append(buggyLine)
                        wcsv_list_issueReportsCreatedDate.append(str_time_createdDate)
                    #===end===#
            wcsv_columns = OrderedDict([('bugFilename',wcsv_list_bugFilename),
                            ('bugIntroducingTime',wcsv_list_bugIntroducingTime),
                            ('bugFixingTime',wcsv_list_bugFixingTime),
                            ('bugIntroducingCommitsSha',wcsv_list_bugIntroducingCommitsSha),
                            ('bugFixingCommitsSha',wcsv_list_bugFixingCommitsSha),
                            ('buggyLine',wcsv_list_buggyLine),
                            ('issueReportsCreatedDate',wcsv_list_issueReportsCreatedDate)]);
            df_saved = pd.DataFrame.from_dict(wcsv_columns);
            dir_path_saved = '%s/%s/'%(path_common_saved,project)
            if not os.path.exists(dir_path_saved):
                os.makedirs(dir_path_saved);
            df_saved.to_csv(dir_path_saved + 'buggyLinesIntervals.csv',index=False);#不保存行索引
            print(project+" finish")






