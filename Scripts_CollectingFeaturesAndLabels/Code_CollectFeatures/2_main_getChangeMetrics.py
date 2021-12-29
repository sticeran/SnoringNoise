import Class_basic.GitRepositoryClass as GRC
import Class_basic.ChangeMetricsClass as CMC
import pandas as pd
import os
import time
import datetime
import re


#根据commits信息计算提交级度量
def FUN_getChangeMetrics(projectName,instanceName,allLine_commits,createDate_currentVersion):
    #提交集度量类。依据固定格式获取
    metrics_class = CMC.ChangeMetricsClass();#Churn = 0;#要不要绝对值
    metrics_class.instanceName = instanceName;
    LOC = allLine_commits[0];
    LOC = LOC[4:].replace('\n', '').replace('\r', '');
    metrics_class.LOC = int(LOC);
    
    fileCreateDate = allLine_commits[1];
    fileCreateDate = fileCreateDate[15:].replace('\n', '').replace('\r', '');
    list_commitSHA = [];#存储所有的commitSHA
    list_author = [];
    list_createDate = [];
    list_message = [];
    list_stat = [];
    len_allLine = len(allLine_commits);#总行数
    len_allLine_commits = len_allLine - 2;
#     num_commits = int(len_allLine/8);#获得的每个commit有固定格式8行，所以获得8的倍数
    #获得commit个数
#     if (len_allLine-1) % 8 == 0:
#         num_commits = int ((len_allLine-1) / 8);#不安全，可能会出现多个commit的Stat为空，出现巧合。
#     else:
    num_commits = 0;
    for i_line in allLine_commits:
        if len(i_line) > 7:
            if i_line[0:7] == "Commit:":
                num_commits += 1;
    
    #最开始两行信息存储了LOC和文件创建日期
    num_headerLines = 2;
    idx_startLines = num_headerLines;
    if len_allLine_commits != 0:
        for i in range(num_commits):  # @UnusedVariable
            commitSHA_current = allLine_commits[idx_startLines];
            commitSHA_current = commitSHA_current[7:].replace('\n', '').replace('\r', '');
            author_current = allLine_commits[idx_startLines+1];
            author_current = author_current[7:].replace('\n', '').replace('\r', '');
            createDate_current = allLine_commits[idx_startLines+2];
            createDate_current = createDate_current[11:].replace('\n', '').replace('\r', '');
            message_current = allLine_commits[idx_startLines+3];
            stat_current = '';
            if idx_startLines+5 < len_allLine:#是从0开始的，不能加=号
                #Stat:后面可能出现无信息和空行的情况，因此需要特殊判断
                temp_JudgeSpecialCase = allLine_commits[idx_startLines+5][:7];
                if temp_JudgeSpecialCase != "Commit:":
                    stat_current = allLine_commits[idx_startLines+6];
                    idx_startLines = idx_startLines + 8;
                else:#出现了Stat:后面无信息和空行的情况。
                    idx_startLines = idx_startLines+5;#下一次commitSHA的位置
            list_commitSHA.append(commitSHA_current);
            list_author.append(author_current);
            list_createDate.append(createDate_current);
            list_message.append(message_current);
            list_stat.append(stat_current);
    
        FUN_getAuthors(metrics_class,list_author);
        FUN_getFixCount(metrics_class,projectName,list_message);
        FUN_getChangeSet(metrics_class,list_commitSHA);
        judgeEmpty = ''.join(list_stat)
        if judgeEmpty == '':
            pass
        else:
            list_touched = FUN_getModifiedLineInfo(metrics_class,list_stat);
            FUN_getWeightedReleaseLength(metrics_class,createDate_currentVersion,list_createDate,list_touched);
    FUN_getReleaseLength(metrics_class,fileCreateDate,createDate_currentVersion);
    list_oneInstance = metrics_class.metrics2list();
    return list_oneInstance;

#计算两个日期相差天数，自定义函数名，和两个日期的变量名。
def Caltime(date1,date2):
    #%Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。
    date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S") 
    date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
#     date1=time.strptime(date1,"%Y-%m-%d")
#     date2=time.strptime(date2,"%Y-%m-%d")
    #根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...
    date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
#     date1=datetime.datetime(date1[0],date1[1],date1[2])
#     date2=datetime.datetime(date2[0],date2[1],date2[2])
    #返回两个变量相差的值，就是相差天数
    return date2-date1

#判断日期是否为合法输入，正确返回True，错误返回False，注意大小写。
def is_date(str):  # @ReservedAssignment
    try:
        time.strptime(str,"%Y-%m-%d")
        return True
    except:
        return False

def FUN_getReleaseLength(metrics_class,fileCreateDate,createDate_currentVersion):
    interval = Caltime(fileCreateDate,createDate_currentVersion);
    num_days_diff = interval.days;
    metrics_class.Release_Length = round(num_days_diff/7,2);#该度量最原始的文献是指weeks，而TOSEM-2021数据集中的含义不明，数值过大，所以按最原始文献的定义
        
def FUN_getWeightedReleaseLength(metrics_class,createDate_currentVersion,list_createDate,list_touched):
    sum_molecule = 0;
    for i in range(len(list_createDate)):
        i_createDate_commit = list_createDate[i];
        i_insertion = list_touched[i];
        interval = Caltime(i_createDate_commit,createDate_currentVersion);
        num_days_diff = interval.days;
        num_weeks = num_days_diff/7;
        sum_molecule += num_weeks * i_insertion;
    metrics_class.Weighted_Release_Length = round(sum_molecule/sum(list_touched),2);

def FUN_getChangeSet(metrics_class,list_commitSHA):
    list_Change_Set = [];
    for i_commitSHA in list_commitSHA:
        #获取和每个文件同一提交的文件数量。
        #git log -1 --stat fc3abc231ddde796c19eaa8db699bf614d7dc29e
        command = ['-1','--stat',i_commitSHA];
        commit_log = repo.git_log_command(command);
        log_list = commit_log.split("\n")
        lastLine = log_list[len(log_list)-1];
        if lastLine.find("file changed,") != -1:
            idx_end = lastLine.find("file changed,") - 1;
            num_changedFile = lastLine[1:idx_end];
        elif lastLine.find("files changed,") != -1:
            idx_end = lastLine.find("files changed,") - 1;
            num_changedFile = lastLine[1:idx_end];
        else:
            idx_end = 0;
            num_changedFile = 0;
        list_Change_Set.append(int(num_changedFile));

    
    len_commits = len(list_commitSHA);
    metrics_class.Change_Set_Size = sum(list_Change_Set);
    metrics_class.Max_Change_Set_Size = max(list_Change_Set);
    metrics_class.Average_Change_Set_Size = round(metrics_class.Change_Set_Size/len_commits,2);

def FUN_getModifiedLineInfo(metrics_class,list_stat):
    list_insertions = [];
    list_deletions = [];
    list_churns = [];
    list_touched = [];
    for i_stat in list_stat:
        idx_insertion = i_stat.find("insertion");
        idx_deletion = i_stat.find("deletion");
        if idx_insertion != -1:
            str_temp = i_stat[:idx_insertion];
            idx_start = str_temp.rfind(",") + 1;
            num_insertion = int(i_stat[idx_start:idx_insertion-1]);
        else:
            num_insertion = 0;
        if idx_deletion != -1:
            str_temp = i_stat[:idx_deletion];
            idx_start = str_temp.rfind(",") + 1;
            num_deletion = int(i_stat[idx_start:idx_deletion-1]);
        else:
            num_deletion = 0;
        num_churn = abs(num_insertion - num_deletion);#要不要绝对值？
        num_touched = abs(num_insertion + num_deletion);
        list_insertions.append(num_insertion);
        list_deletions.append(num_deletion);
        list_churns.append(num_churn);
        list_touched.append(num_touched);
    
    metrics_class.Number_of_Revisions = len(list_stat);
    metrics_class.LOC_added = sum(list_insertions);
    metrics_class.Max_LOC_added = max(list_insertions);
    metrics_class.Average_LOC_added = round(metrics_class.LOC_added/metrics_class.Number_of_Revisions,2);
    metrics_class.LOC_touched = sum(list_touched);
    metrics_class.Churn = sum(list_churns);
    metrics_class.Max_Churn = max(list_churns);
    metrics_class.Average_Churn = round(metrics_class.Churn/metrics_class.Number_of_Revisions,2);
    return list_touched;
    
def FUN_getAuthors(metrics_class,list_author):
    Authors = len(set(list_author));
    metrics_class.Authors = Authors;
    
def FUN_getFixCount(metrics_class,projectName,list_message):
    projectName_fixedFormat = (projectName + '-').lower();
    keyword_fix = "fix";
#     i_message = "##0 ([AAA-123";
    
    Fix_Count = 0;
    for i_message in list_message:
        i_message = i_message.lower();
        if i_message.find('%s'%projectName_fixedFormat)!=-1:#先匹配一次过滤掉不合适的，可以加速
            if (re.findall(r"^([ #_-])?|([ #_-])?%s([0-9]{1,5})+"%projectName_fixedFormat, i_message)):
                Fix_Count += 1;
        elif i_message.find('%s'%keyword_fix)!=-1:#先匹配一次过滤掉不合适的，可以加速
            if (re.findall(r"^fix(ed|es)?([ _-])+|([ _-])+fix(ed|es)?([ _-])+|([ _-])+fix(ed|es)?$",i_message)) and re.findall(r"bug|issue|problem|error",i_message) and not (re.findall(r"([ ])+merge |([ ])+revert |([ ])+license |spelling|formatting|refactoring| doc([ ])+|document", i_message)):
                Fix_Count += 1;
        else:
            pass;#failed
    metrics_class.Fix_Count = Fix_Count;

        


# 从抽取的提交日志信息求16种提交集度量
if __name__ == "__main__":
    
    list_projectName = ["shiro","maven","flume","mahout","calcite","pdfbox","iotdb","tika"];
    
    #Change the path to the path where your file is located
    #读取路径
    path_common = "D:/workspace/DataFolder/features/commit_logs/";
    path_common_versionReleaseDate = "D:/workspace/DataFolder/features/versionReleaseDate/";
    path_common_gitRepository = "D:/workspace/DataFolder/GitRepository/";
    path_common_github = "https://github.com/apache/";
    # 读取文件名
    read_fileName_versionReleaseDate = "releaseDate.csv";
    
    # 存储路径
    path_saved_common = "D:/workspace/DataFolder/features/changeMetrics/";
    # 存储文件列名
    list_columns = ["File","LOC","LOC touched","Number of Revisions","Fix Count","Authors",
                    "LOC added","Max LOC added","Average LOC added","Churn","Max Churn","Average Churn",
                    "Change Set Size","Max Change Set Size","Average Change Set Size","Release Length",
                    "Weighted Release Length"];
    
    for i_projectName in list_projectName:
        print(i_projectName);
        #已收集的版本发布日期信息
        path_versionReleaseDate = path_common_versionReleaseDate + i_projectName + '/' + read_fileName_versionReleaseDate;
        df_versionReleaseDate = pd.read_csv(path_versionReleaseDate);
        #已收集的每个版本的提交信息
        path_project = path_common + i_projectName + '/';
        folderList = os.listdir(path_project);#每个版本是一个文件夹
        
        #git本地仓库路径
        local_path_gitRepository = path_common_gitRepository + i_projectName + '/';
        #github下载路径。如果本地仓库为空，则从github上下载
        github_path_gitRepository = path_common_github + i_projectName + '.git';
        #操作git仓库的命令类
        repo = GRC.GitRepositoryClass(local_path_gitRepository, github_path_gitRepository);
        
        for i_folder in folderList:
            print(i_folder)
            list_allRows = [];
            #===获得当前版本的提交级度量===#
            #获得当前版本的创建时间
            start_idx = i_folder.rfind('-');
            currentVersion = i_folder[start_idx+1:];
            v_currentVersion = "v"+i_folder;
            idx_currentVersion = df_versionReleaseDate[df_versionReleaseDate['version']==v_currentVersion].index.tolist()[0];
            createDate_currentVersion = df_versionReleaseDate.loc[idx_currentVersion,'releaseDate'];
            #获得当前版本下每个文件的提交级度量
            path_project_version = path_project + i_folder + '/';
            fileList = os.listdir(path_project_version);
            for i_file in fileList:
#                 i_file = "linq4j#src#test#java#com#example#Linq4jExample.java.txt"
                print(i_file)
                path_commits = path_project_version + i_file;
                with open(path_commits, 'r', encoding='UTF-8', errors='ignore') as txt:
                    allLine_commits = txt.readlines();
                #实例名
                instanceName = i_file.replace("#", "/");
                instanceName = instanceName[:len(instanceName)-4];
                #根据commits信息计算提交级度量
                # param i_projectName 计算Fix_Count需要
                # param instanceName 实例名
                # param allLine_commits 每个实例涉及的所有的提交
                # param createDate_currentVersion 当前版本的创建时间，计算Release_Length和Weighted_Release_Length需要
                list_oneRow = FUN_getChangeMetrics(i_projectName,instanceName,allLine_commits,createDate_currentVersion);
                list_allRows.append(list_oneRow);
            #===end===#
            
            saved_fileName = i_projectName + '-' + currentVersion + '.csv';
            df_allRows = pd.DataFrame(list_allRows,columns=list_columns);
            dir_path_saved = path_saved_common + i_projectName + '/';
            if not os.path.exists(dir_path_saved):
                os.makedirs(dir_path_saved);
            path_saved_fileName = dir_path_saved + saved_fileName;
            df_allRows.to_csv(path_saved_fileName,index=False);#不保存行索引
            print("%s finish"%currentVersion);
    print("all project finish");
        
        
        
        
        
    
    
    
    
    
    