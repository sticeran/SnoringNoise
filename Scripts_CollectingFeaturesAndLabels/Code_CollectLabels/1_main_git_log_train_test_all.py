import Class_basic.GitRepositoryClass as GRC
import pandas as pd
import os



# 设定所有版本中的第50%个版本为分界点，前50%版本中，设定train，test时间点，从本地git仓库获取git_log.csv
if __name__ == "__main__":

    list_projectName = ["shiro","maven","flume","mahout","calcite","pdfbox","iotdb","tika"];
    
    # 读取路径
    path_common_versionReleaseDate = "D:/workspace/DataFolder/features/versionReleaseDate/";
    path_common_gitRepository = "D:/workspace/DataFolder/GitRepository/";
    path_common_github = "https://github.com/apache/";
    # 读取文件名
    read_fileName_versionReleaseDate = "releaseDate.csv";
    
    # 存储路径
    path_saved_common_versionReleaseDate = "D:/workspace/DataFolder/labels_MASZZ/versionReleaseDate/";
    path_saved_common_log_snoring_train = "D:/workspace/DataFolder/labels_MASZZ/snoringTrain_labels/git_log_from_GitRepository/";
    path_saved_common_log_snoring_test = "D:/workspace/DataFolder/labels_MASZZ/snoringTest_labels/git_log_from_GitRepository/";
    path_saved_common_log_groundtruth = "D:/workspace/DataFolder/labels_MASZZ/groundtruth_labels/git_log_from_GitRepository/";
    # 存储文件列名
    list_columns = ['commitSHA', 'createDate', 'message'];
    
    for i_projectName in list_projectName:
        print(i_projectName);
        #获得版本数
        path_versionReleaseDate = path_common_versionReleaseDate + i_projectName + '/' + read_fileName_versionReleaseDate;
        df_versionReleaseDate = pd.read_csv(path_versionReleaseDate);
        #计算打鼾数据集和非打鼾数据集的截止点。噪音版本数<=50%总版本数，假设 1 2 3 4 5共五个版本，3 4 5是未来版本，问题报告的解决时间不能早于3的创建时间
        #在截止点之前的版本，按2：1的版本比例生成训练集和测试集
        df_versionReleaseDate["cutoff"] = '';
        num_versions = len(df_versionReleaseDate);
        cutoff_test = round(num_versions/2+0.01);
        cutoff_train = cutoff_test + round((num_versions - cutoff_test) * (1/3));#因为是降序
        df_versionReleaseDate.loc[cutoff_test-1,"cutoff"] = "test";
        versionTag_snoring_test = df_versionReleaseDate.loc[cutoff_test-1,"versionTag"];
        start_idx = versionTag_snoring_test.find('v_')+2;
        versionTag_snoring_test = versionTag_snoring_test[start_idx:];
        df_versionReleaseDate.loc[cutoff_train-1,"cutoff"] = "train";
        versionTag_snoring_traing = df_versionReleaseDate.loc[cutoff_train-1,"versionTag"];
        start_idx = versionTag_snoring_traing.find('v_')+2;
        versionTag_snoring_traing = versionTag_snoring_traing[start_idx:];
        #存储时间截止点，下一步收集标签需要
        dir_path_saved = path_saved_common_versionReleaseDate + i_projectName + '/';
        if not os.path.exists(dir_path_saved):
            os.makedirs(dir_path_saved);
        path_saved_fileName = dir_path_saved + read_fileName_versionReleaseDate;
        df_versionReleaseDate.to_csv(path_saved_fileName,index=False);#不保存行索引
        
        #===分别在截止时间点前（打鼾噪音数据集）和最新时间点（即干净数据集），使用git log===#
        
        #git本地仓库路径
        local_path_gitRepository = path_common_gitRepository + i_projectName + '/';
        #github下载路径。如果本地仓库为空，则从github上下载
        github_path_gitRepository = path_common_github + i_projectName + '.git';
        #操作git仓库的命令类
        repo = GRC.GitRepositoryClass(local_path_gitRepository, github_path_gitRepository);
        #使用git log获得最新git仓库HEAD对应的commitSHA，用于回退版本（tag）之后再返回最新版本
        #git log -1 --pretty=format:'%H'
        command = ['-1','--pretty=%H']#'--pretty={"%H"}'等价于'--pretty=format:%H'
        commitSHA_initial = repo.git_log_command(command)
         
        #干净数据集：获得当前最新时间点所有提交日志，并存储
        command = ['--pretty=%H#SEP#%cd#SEP#%s','--date=format:%Y-%m-%d %H:%M:%S',]
        str_gitLogs = repo.git_log_command(command)#存下来仅为查阅使用
        list_gitLogs = str_gitLogs.split('\n')
        list_gitLogs = [ i.split('#SEP#') for i in list_gitLogs]
        df_gitLogs = pd.DataFrame(list_gitLogs,columns=list_columns);
        dir_path_saved = path_saved_common_log_groundtruth + i_projectName + '/';
        if not os.path.exists(dir_path_saved):
            os.makedirs(dir_path_saved);
        path_saved_fileName = dir_path_saved + 'git_log.csv';
        df_gitLogs.to_csv(path_saved_fileName,index=False);#不保存行索引
         
        #噪音测试集：获得截止时间点前所有提交日志，并存储
        #使用git reset --hard tag回退到目标版本（tag）
        repo.reset_to_tag(versionTag_snoring_test);#轻易不要运行，因为会造成永久改变
        command = ['--pretty=%H#SEP#%cd#SEP#%s','--date=format:%Y-%m-%d %H:%M:%S',]
        str_gitLogs = repo.git_log_command(command)#存下来仅为查阅使用
        list_gitLogs = str_gitLogs.split('\n')
        list_gitLogs = [ i.split('#SEP#') for i in list_gitLogs]
        df_gitLogs = pd.DataFrame(list_gitLogs,columns=list_columns);
        dir_path_saved = path_saved_common_log_snoring_test + i_projectName + '/';
        if not os.path.exists(dir_path_saved):
            os.makedirs(dir_path_saved);
        path_saved_fileName = dir_path_saved + 'git_log.csv';
        df_gitLogs.to_csv(path_saved_fileName,index=False);#不保存行索引
        #返回到最新git仓库原HEAD位置
        repo.reset_to_tag(commitSHA_initial);#轻易不要运行，因为会造成永久改变
          
        #噪音训练集：获得截止时间点前所有提交日志，并存储
        #使用git reset --hard tag回退到目标版本（tag）
        repo.reset_to_tag(versionTag_snoring_traing);#轻易不要运行，因为会造成永久改变
        command = ['--pretty=%H#SEP#%cd#SEP#%s','--date=format:%Y-%m-%d %H:%M:%S',]
        str_gitLogs = repo.git_log_command(command)#存下来仅为查阅使用
        list_gitLogs = str_gitLogs.split('\n')
        list_gitLogs = [ i.split('#SEP#') for i in list_gitLogs]
        df_gitLogs = pd.DataFrame(list_gitLogs,columns=list_columns);
        dir_path_saved = path_saved_common_log_snoring_train + i_projectName + '/';
        if not os.path.exists(dir_path_saved):
            os.makedirs(dir_path_saved);
        path_saved_fileName = dir_path_saved + 'git_log.csv';
        df_gitLogs.to_csv(path_saved_fileName,index=False);#不保存行索引
        #返回到最新git仓库原HEAD位置
        repo.reset_to_tag(commitSHA_initial);#轻易不要运行，因为会造成永久改变
        
        print("%s finish"%i_projectName);
    print("all project finish");
        
        
        

        
        
    

    
    
    
    
    