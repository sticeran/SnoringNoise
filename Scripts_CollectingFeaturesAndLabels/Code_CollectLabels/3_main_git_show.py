import Class_basic.GitRepositoryClass as GRC
import pandas as pd
import os


# 获得BFC的commitsha所对应的详细修改信息commitsha.txt
#git log --pretty=format:'%cd' commitsha和git log commitsha显示的日期不同，原因不明。
if __name__ == "__main__":

    list_projectName = ["shiro","maven","flume","mahout","calcite","pdfbox","iotdb","tika"];
    
    #"snoring_labels"用于读取snoring时间节点前的提交日志，以及读取解决时间在snoring时间节点前的问题报告
    list_labels_type = ["snoringTrain_labels","snoringTest_labels","groundtruth_labels"]
    
    #读取路径
    path_common = "D:/workspace/DataFolder/labels_MASZZ/";
    path_common_gitRepository = "D:/workspace/DataFolder/GitRepository/";
    path_common_github = "https://github.com/apache/";
    # 读取文件名
    read_fileName_versionReleaseDate = "releaseDate.csv";
    
    
    for i_projectName in list_projectName:
        
        #git本地仓库路径
        local_path_gitRepository = path_common_gitRepository + i_projectName + '/';
        #github下载路径。如果本地仓库为空，则从github上下载
        github_path_gitRepository = path_common_github + i_projectName + '.git';
        #操作git仓库的命令类
        repo = GRC.GitRepositoryClass(local_path_gitRepository, github_path_gitRepository);
        
        #===分别在截止时间点前（打鼾噪音数据集）和最新时间点（即干净数据集），使用git show===#
        for labels_type in list_labels_type:
            print(i_projectName,labels_type);
            
            #存储路径
            dir_path_saved = "%s%s/git_show_bugFixingCommitsID/%s/"%(path_common,labels_type,i_projectName);
            if not os.path.exists(dir_path_saved):
                os.makedirs(dir_path_saved);
            #获得BFC
            path_BFC = "%s%s/matching_bugid_fixingsha/%s_bug_commit_all.csv"%(path_common,labels_type,i_projectName);
            df_BFC = pd.read_csv(path_BFC);
            list_commitsha_BFC = df_BFC['commitSHA'].tolist();
            for i_commitsha_BFC in list_commitsha_BFC:
#                 i_commitsha_BFC = "797e0716858d95a54a91297cce43b23a5fa47fac"
#                 print(i_commitsha_BFC)
                command = [i_commitsha_BFC]
                commit_show = repo.git_show_command(command)
                commit_show = commit_show.encode('UTF-8', 'ignore').decode('UTF-8')#一些字符无法被utf-8解码，把无法转化为utf-8格式的字符‘ignore’掉，再进行解码
                path_saved_fileName = '%s%s.txt'%(dir_path_saved,i_commitsha_BFC)
                with open(path_saved_fileName, 'w', encoding='UTF-8') as wtxt:
                    wtxt.write(commit_show);
            
        #===end===#
        print("%s finish"%i_projectName);
    print("all project finish");
        
        
        

        
        
    

    
    
    
    
    