import Class_basic.GitRepositoryClass as GRC
import CollectFeatures.getFileList as GFL
import pandas as pd
import sys
import os
# import csv

#遍历java文件列表，使用git log，获得为收集每个文件提交级度量所需信息，存入特定文件
def FUN_getCommitInformation(pathName_project,fileList,versionTag_pre,versionTag_current,path_saved_currentVersion):
    for i_file in fileList:
#         i_file="linq4j/src/test/java/com/example/Linq4jExample.java"
        print(i_file);#存储文件名，数据集实例名
        #获取每个文件的创建时间
        #git log -1 --diff-filter=A --pretty=format:'%cd' --date=format:'%Y-%m-%d %H:%M:%S' -- 2/b1.txt
        command = ['-1','--diff-filter=A','--pretty=format:%cd','--date=format:%Y-%m-%d %H:%M:%S','--',i_file];
        fileCreateDate = repo.git_log_command(command);
        if fileCreateDate == '':#如果没有创建时间（提交），则用版本库中最早的提交代替
            command = ['--reverse','--pretty=format:%cd','--date=format:%Y-%m-%d %H:%M:%S','--',i_file];
            temp = repo.git_log_command(command);
            fileCreateDate = temp.split("\n")[0];
        #获取每个文件提交级度量所需信息
        #git log --stat tag1..tag2 --pretty=format:‘%H,%an,%ae,%cd’ --date=format:'%Y-%m-%d %H:%M:%S' -- filename.java
        command = ['--stat',versionTag_pre+'..'+versionTag_current,'--pretty=format:Commit:%H%nAuthor:%an,%ae%nCreateDate:%cd%nMessage:%s%nStat:',
                   '--date=format:%Y-%m-%d %H:%M:%S','--',i_file];
        commit_log = repo.git_log_command(command);
        
        path_i_file = pathName_project + '/' + i_file;
        #获取代码行
        with open(path_i_file, 'r', encoding='UTF-8', errors='ignore') as file:
            allLines_i_file = file.readlines();
            num_allLines = len(allLines_i_file);
        
        dir_path_saved = path_saved_currentVersion;
        if not os.path.exists(dir_path_saved):
            os.makedirs(dir_path_saved);
        fileName = i_file.replace("/", "#");
        path_saved_fileName = dir_path_saved + fileName + '.txt';
        with open(path_saved_fileName, 'w', encoding='UTF-8') as wtxt:
            wtxt.write('LOC:'+str(num_allLines)+'\n');#记录每个文件的创建时间
            wtxt.write('FileCreateDate:'+fileCreateDate+'\n');#记录每个文件的创建时间
            wtxt.write(commit_log);
        


# 从git仓库获取抽取提交级度量所需的日志信息
if __name__ == "__main__":

    list_projectName = ["shiro","maven","flume","mahout","calcite","pdfbox","iotdb","tika"];
    
    #Change the path to the path where your file is located
    #读取路径
    path_common = "D:/workspace/DataFolder/features/versionTag/";
    fileName_versionTag = "versionTag.txt";#需要提前把选取的目标版本，记录到文件
    path_common_gitRepository = "D:/workspace/DataFolder/GitRepository/";
    path_common_github = "https://github.com/apache/";
    
    # 存储路径
    path_saved_common_versionReleaseDate = "D:/workspace/DataFolder/features/versionReleaseDate/";
    path_saved_common_commit_logs = "D:/workspace/DataFolder/features/commit_logs/";
    # 存储文件名
    saved_fileName_versionReleaseDate = "releaseDate.csv";
    list_columns = ['versionTag', 'version', 'releaseDate'];
    
    for i_projectName in list_projectName:
        print(i_projectName);
        #预收集的版本信息路径
        path_versionTag = path_common + i_projectName + '/' + fileName_versionTag;
        txt = open(path_versionTag,'r');#所有版本tag
        allLine_versionTag = txt.readlines();
        txt.close();
        #git本地仓库路径
        local_path_gitRepository = path_common_gitRepository + i_projectName + '/';
        #github下载路径。如果本地仓库为空，则从github上下载
        github_path_gitRepository = path_common_github + i_projectName + '.git';
        #操作git仓库的命令类
        repo = GRC.GitRepositoryClass(local_path_gitRepository, github_path_gitRepository);
        #使用git tag获得git repository中所有标签，查看目标版本是否存在于所有标签中
        tag_list = repo.tags();
        #使用git log获得最新git仓库HEAD对应的commitSHA，用于回退版本（tag）之后再返回最新版本
        #git log -1 --pretty=format:'%H'
        command = ['-1','--pretty=%H']#'--pretty={"%H"}'等价于'--pretty=format:%H'
        commitSHA_initial = repo.git_log_command(command)#1c97815737fee587729b1d3827814f3f58d2b6ec
        
        #===获取当前版本下git仓库中的java文件名（实例）列表所需信息===#
        pathName_project = path_common_gitRepository + i_projectName;
        level = 1;#目录层级
        path_initial = path_common_gitRepository + i_projectName + '/';#在递归时需要计算减去，和csv文件路径名一致
        #===end===#
        
        #收集每个版本的发布时间，存入tag_commitSHA_releaseDate.csv
        list_createDate_allVersions = []
#         allLine_versionTag.reverse()#逆序
        for i_versionTag in range(0,len(allLine_versionTag)-1):
            print('\n'+allLine_versionTag[i_versionTag]);
            #当前版本和前一个版本
            versionTag_current = allLine_versionTag[i_versionTag].replace('\n', '').replace('\r', '');
            versionTag_pre = allLine_versionTag[i_versionTag+1].replace('\n', '').replace('\r', '');
            #获取当前版本下git仓库中的java文件名（实例）列表所需信息
            fileList = [];#储存不包括path_initial相对路径的文件名
            fileList_fileName = [];#存储绝对路径的文件名
            allFileNum=[0];
            if versionTag_current in tag_list and versionTag_pre in tag_list:
                #使用git reset --hard tag回退到目标版本（tag）
                repo.reset_to_tag(versionTag_current);#轻易不要运行，因为会造成永久改变
                
                #===获得版本创建时间，打标签时需要该信息===#
                #git log -1 --pretty=format:'%cd' '--date=format:%Y-%m-%d %H:%M:%S'
                command = ['-1','--pretty=format:%cd','--date=format:%Y-%m-%d %H:%M:%S'];
                createDate_currentVersion = repo.git_log_command(command);
                start_idx = versionTag_current.rfind('-');#如果没找到，返回-1
                start_idx_underline = versionTag_current.rfind('_');#如果没找到，返回-1
                start_idx_v = versionTag_current.rfind('v');#如果没找到，返回-1
                start_idx_oblique = versionTag_current.rfind('/');#如果没找到，返回-1
                versionNum = 0;
                if start_idx != -1:
                    versionNum = versionTag_current[start_idx+1:];
                elif start_idx_underline != -1:
                    versionNum = versionTag_current[start_idx_underline+1:];
                elif start_idx_v != -1:
                    versionNum = versionTag_current[start_idx_v+1:];
                elif start_idx_oblique != -1:
                    versionNum = versionTag_current[start_idx_oblique+1:];
                if versionNum == 0:
                    versionNum = versionTag_current
                #加'v_'是为了避免1.20存入csv只会被csv、excel软件保留为1.2，所有项目只有tika中的1.20有这个问题，但为了统一，所有项目统一更改。
                list_createDate_allVersions.append(['v_'+versionTag_current,'v_'+versionNum,createDate_currentVersion]);
                #===end===#
                
                #递归获取当前版本的java文件列表
                GFL.getFileList_java(level, pathName_project, path_initial, fileList, fileList_fileName, allFileNum);
                print ('总文件数 =', allFileNum);
                #存储路径
                saved_versionTag_current = versionNum;
                path_saved_currentVersion = path_saved_common_commit_logs + i_projectName + '/' + saved_versionTag_current + '/';
                #遍历java文件列表，使用git log，获得收集每个文件提交级度量所需信息，存入特定文件
                FUN_getCommitInformation(pathName_project,fileList,versionTag_pre,versionTag_current,path_saved_currentVersion);
                #返回到最新git仓库原HEAD位置
                repo.reset_to_tag(commitSHA_initial);#轻易不要运行，因为会造成永久改变
            else:
                print("error")
                sys.exit(1)
            
        df_allRows = pd.DataFrame(list_createDate_allVersions,columns=list_columns);
        dir_path_saved = path_saved_common_versionReleaseDate + i_projectName + '/';
        if not os.path.exists(dir_path_saved):
            os.makedirs(dir_path_saved);
        path_saved_fileName = dir_path_saved + saved_fileName_versionReleaseDate;
        df_allRows.to_csv(path_saved_fileName,index=False);
        print("finish");
        
        
    print("all finish");

    
    
    
    
    