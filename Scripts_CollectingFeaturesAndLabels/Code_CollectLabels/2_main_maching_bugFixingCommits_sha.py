# -*- coding: utf-8 -*-
#文件原名maching_id_sha

import pandas as pd
import copy
import os 
import re
import datetime

#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth',200);#设置value的显示长度为200，默认为50

#分别从打鼾数据集和非打鼾数据集，根据项目的问题报告和git_log.csv匹配BFC的commitsha
#打鼾数据集，问题报告的解决时间不能早于分界点，否则是在未来解决的
#获取修复bug的提交号（这一步不用获得修复时间，因为很多修复提交不是对文件bug的修复）
#存bug报告时间和修复bug时间，后面步骤就不用那么乱了
if __name__ == "__main__":

#     direct = {'shiro':'SHIRO-',
#               'maven':'MNG-',
#               'flume':'FLUME-',
#               'mahout':'MAHOUT-',
#               'calcite':'CALCITE-',
#               'pdfbox':'PDFBOX-',
#               'iotdb':'IOTDB-',
#               'tika':'TIKA-',
#             }
    direct = {
            'shiro':'SHIRO-',
            }#调试用
    
    #"snoring_labels"用于读取snoring时间节点前的提交日志，以及读取解决时间在snoring时间节点前的问题报告
    list_labels_type = ["snoringTrain_labels","snoringTest_labels","groundtruth_labels"]
    
    path_common = "D:/workspace/DataFolder/ThirdResearchPoint";
    
    for project in direct:
    
        for labels_type in list_labels_type:
        
            print(project,labels_type)
            #对于打鼾噪音数据集，获得测试集截止时间点：50%版本对应的创建时间
            if labels_type != "groundtruth_labels":
                #获得打鼾时间点
                path_versionReleaseDate = '%s/labels_MASZZ/versionReleaseDate/%s/releaseDate.csv'%(path_common,project);
                df_versionReleaseDate = pd.read_csv(path_versionReleaseDate);
                if labels_type == "snoringTrain_labels":
                    time_versionCutoff = df_versionReleaseDate[df_versionReleaseDate['cutoff']=='train']['releaseDate'].values[0];
                elif labels_type == "snoringTest_labels":
                    time_versionCutoff = df_versionReleaseDate[df_versionReleaseDate['cutoff']=='test']['releaseDate'].values[0];
            
            bug_name = direct[project]
            
            project_dir = '%s/issue_reports/%s'%(path_common,project)
            
            #---获取bugID和问题报告的创建时间---#
            df_issueReports_all = pd.DataFrame();
            fileNames_issueReports = os.listdir(project_dir);
            for str_i_filename in fileNames_issueReports:
                filePath_issueReports = project_dir + "/" + str_i_filename;#文件路径
                df_issueReports = pd.read_csv(filePath_issueReports);
                df_issueReports_all = df_issueReports_all.append(df_issueReports);
    #         df_issueReports_all = df_issueReports_all[(df_issueReports_all['type'] == 'Bug') & (df_issueReports_all['resolution'] == 'Fixed')];
            df_issueReports_all = df_issueReports_all[(df_issueReports_all['type'] == 'Bug')];
            df_issueReports_all = df_issueReports_all[(df_issueReports_all['resolution'] == 'Fixed')
                                                      | (df_issueReports_all['resolution'] == 'Resolved')
                                                      | (df_issueReports_all['resolution'] == 'Done')
                                                      | (df_issueReports_all['resolution'] == 'Implemented')];
            df_issueReports_all = df_issueReports_all[(df_issueReports_all['status'] == 'Closed') | (df_issueReports_all['status'] == 'Resolved')];
            if labels_type != "groundtruth_labels":
                df_issueReports_all = df_issueReports_all[df_issueReports_all['resolvedDateEpoch'] <= time_versionCutoff];
            list_bugID = df_issueReports_all['issueKey'].tolist();
            list_createdDate = df_issueReports_all['createdDateEpoch'].tolist();#list_createdDate需要按标准日期做进一步转化
            list_createdDate = [str(datetime.datetime.strptime(i_date,'%Y-%m-%d %H:%M:%S')) for i_date in list_createdDate];
            dict_bug_date = dict(zip(list_bugID,list_createdDate));#创建字典
            #---end---#
            
            #---获取git log---#
            filePath_gitLog = '%s/labels_MASZZ/%s/git_log_from_GitRepository/%s/git_log.csv'%(path_common,labels_type,project)#git log切换到对应版本，问题报告信息可能不用动。问题报告可以规定个时间，如只用9月份之前的
            df_versionReleaseDate = pd.read_csv(filePath_gitLog);
            #---end---#
            
            # read csv and get the summary which contain Project-ID or fix
            commit_sum = len(df_versionReleaseDate)
            selectedRows = []
            for index, row in df_versionReleaseDate.iterrows():
                line = row['message']
                line = line.lower()
                if line.find('Remove avatica from the tree')!=-1:
                    print('Exclude:',line)
                    continue;
                if line.find("%s"%(bug_name.lower()))!=-1:
                    selectedRows.append(row)
                elif re.findall(r"^fix(ed|es)?([ _-])+|([ _-])+fix(ed|es)?([ _-])+|([ _-])+fix(ed|es)?$",line) and re.findall(r"\d{1,5}",line):
                    selectedRows.append(row)
                elif re.findall(r"^fix(ed|es)?([ _-])+|([ _-])+fix(ed|es)?([ _-])+|([ _-])+fix(ed|es)?$",line) and re.findall(r"bug|issue|problem|error",line):
                    selectedRows.append(row)
                elif re.findall(r"bugfix|fixbug",line):
                    selectedRows.append(row)
            
            #match bug id and commit through summary
            vbugid = []
            vcommit = []
            vcreatedDate = []
            vfixingDate = []
            nobugid = []
        
            rename = copy.deepcopy(list_bugID)
            bug_sum = len(list_bugID)
        
            for series_oneRow in selectedRows:
                commitSHA = series_oneRow['commitSHA']
                fixingDate = series_oneRow['createDate']
                summary = series_oneRow['message'].lower()
                
                i_id = 0;
                for i_id in range(len(rename)):
                    bugNameID = rename[i_id];
                    bugNameID_ID = bugNameID.split('-',1)[1];#only bugId
                    if summary.find('%s'%bugNameID.lower())!=-1:
                        if(re.findall(r"%s(.*?)\D"%bug_name.lower(), summary)):
                            summary_bugid = re.findall(r"%s(.*?)\D"%bug_name.lower(), summary)
                        else:
                            summary_bugid = re.findall(r"%s(.*?)$"%bug_name.lower(), summary)
                        tmp = ('%s'%bug_name)+summary_bugid[0]
                        if bugNameID == tmp:
                            if fixingDate >= dict_bug_date[bugNameID]:#过滤修复时间比问题报告创建时间小的情况
#                                 print (bugNameID, tmp, "correct");
                                com_res = commitSHA;
                                vbugid.append(bugNameID);
                                vcommit.append(com_res);
                                vcreatedDate.append(dict_bug_date[bugNameID]);
                                vfixingDate.append(fixingDate);
    #                             del dict_bug_date[bugNameID];
    #                             rename.remove(bugNameID);
                            else:
                                pass
#                                 print (bugNameID, tmp, "error");
                            break;
                    elif summary.find('%s'%bugNameID.lower())==-1:#必须写全，因为else是就近原则
                        #summary删除[项目名-XXX]后，是否包含fix和bug id号
                        summary_remain = re.sub("\[?%s\d{1,5}\]?"%bug_name.lower(),"",summary)
    #                     summary_remain = "fix #1 apache"#调试用
    #                     summary_remain = "abc fix bug 456"#调试用
                        if re.findall(r"^fix(ed|es)?([ _-])+|([ _-])+fix(ed|es)?([ _-])+|([ _-])+fix(ed|es)?$",summary_remain) and re.findall(r"#%s"%bugNameID_ID,summary_remain):
    #                         summary_remain = "#1 apache"#调试用
                            if re.findall(r"^#%s[ .-]+"%bugNameID_ID,summary_remain):
                                summary_bugid = re.findall(r"^#%s[ .-]+"%bugNameID_ID,summary_remain)
                            elif re.findall(r"[ .-]+#%s[ .-]+"%bugNameID_ID,summary_remain):
                                summary_bugid = re.findall(r"[ .-]+#%s[ .-]+"%bugNameID_ID,summary_remain)
                            elif re.findall(r"[ .-]+#%s$"%bugNameID_ID,summary_remain):
                                summary_bugid = re.findall(r"[ .-]+#%s$"%bugNameID_ID,summary_remain)
                            summary_bugid = "".join(summary_bugid)#列表转字符串
                            summary_bugid = summary_bugid.replace(' ', '')#替换空格
                            summary_bugid = summary_bugid.replace('#', '')#替换井号
                            if summary_bugid == bugNameID_ID:
                                if fixingDate >= dict_bug_date[bugNameID]:#过滤修复时间比问题报告创建时间小的情况
#                                     print (bugNameID_ID, summary_bugid, "correct");
                                    com_res = commitSHA;
                                    vbugid.append(bugNameID);
                                    vcommit.append(com_res);
                                    vcreatedDate.append(dict_bug_date[bugNameID]);
                                    vfixingDate.append(fixingDate);
    #                                 del dict_bug_date[bugNameID];
    #                                 rename.remove(bugNameID);
                                else:
                                    pass
#                                     print (bugNameID_ID, summary_bugid, "error");
                                break;
                
                if i_id == (len(rename)-1) and not (re.findall(r"([ ])+merge |([ ])+revert |([ ])+license |spelling|formatting|refactoring| doc([ ])+|document", summary)) and not (re.findall(r"%s(.*?)\D"%bug_name.lower(), summary)):
                    #if not find "Project-ID" or "fix #ID" or "fix ID", try to find "fix bug"
                    if re.findall(r"^fix(ed|es)?([ _-])+|([ _-])+fix(ed|es)?([ _-])+|([ _-])+fix(ed|es)?$",summary) and re.findall(r"bug|issue|problem|error",summary):
#                         print ("find",summary);
                        vbugid.append(None);
                        vcommit.append(commitSHA);
                        vcreatedDate.append(None);
                        vfixingDate.append(fixingDate);
                    elif re.findall(r"bugfix|fixbug",line):
#                         print ("find",summary);
                        vbugid.append(None);
                        vcommit.append(commitSHA);
                        vcreatedDate.append(None);
                        vfixingDate.append(fixingDate);
                    
            bug_sum = len(list_bugID)
            set_vcommit = set(vcommit)
            match_vcommit = len(set_vcommit)
            set_vbugid = set(vbugid)
            if None in set_vbugid:
                match_vbugid = len(set_vbugid) - 1
            else:
                match_vbugid = len(set_vbugid)
            set_rename=set(rename)
            nobugid = set_rename-set_vbugid#nobugid等于rename移除被修复的bugid后剩下的bugid
            nobugid = list(nobugid)
            otherFixedBugs = sum(x is None for x in vbugid)
            
            
            if bug_sum != 0:
                recall =  float(match_vbugid)/float(bug_sum)
            else:
                recall = 0
            print ('%-9s%-16s%-8s%-15s%-8s%-21s' % ('commits','matchedCommits','issues','matchedIssues','recall','matchedOtherFixedBugs'))
            print ('%-9s%-16s%-8s%-15s%-8s%-21s' % (commit_sum, match_vcommit, bug_sum, match_vbugid, round(recall,4), otherFixedBugs))
            
            dic_temp={"bugID" : vbugid,
                      "createdDate" : vcreatedDate,
                      "commitSHA" : vcommit,
                      "fixingDate" : vfixingDate,}
            df_bug_commit=pd.DataFrame(dic_temp)#将字典转换成为数据框
            dic_temp={"bugID" : nobugid}
            df_nobug_commit=pd.DataFrame(dic_temp)#将字典转换成为数据框
            
            dir_path_saved = 'D:/workspace/DataFolder/labels_MASZZ/' + labels_type + '/matching_bugid_fixingsha/';
            if not os.path.exists(dir_path_saved):
                os.makedirs(dir_path_saved);
            path_saved_fileName_bug_commit = dir_path_saved + project + '_bug_commit_all.csv';
            path_saved_fileName_nobug_commit = dir_path_saved + project + '_nocommit_all.csv';
            df_bug_commit.to_csv(path_saved_fileName_bug_commit,index=False);#不保存行索引
            df_nobug_commit.to_csv(path_saved_fileName_nobug_commit,index=False);#不保存行索引
            

    
    
