import Class_basic.GitRepositoryClass as GRC
import os



# git_blame_l由bug-fixing的commitsha的前一次提交(^)，获得bug-introducing的commitsha，文件名，作者，引入时间，引入bug的代码行。projectName_commitsha_pre.txt
#经常会遇到莫名其妙的问题，git.exc.GitCommandError: Cmd('git') failed due to: exit code(3221225794)
#报错后，单独执行报错的commit，又可以执行
if __name__ == "__main__":
    
    list_projectName = ["shiro","maven","flume","mahout","calcite","pdfbox","iotdb","tika"];
    
    #"snoring_labels"用于读取snoring时间节点前的提交日志
    list_labels_type = ["snoringTrain_labels","snoringTest_labels","groundtruth_labels"]
    
    #读取路径
    path_common = "D:/workspace/DataFolder/labels_MASZZ/";
    path_common_versionReleaseDate = "D:/workspace/DataFolder/labels_MASZZ/versionReleaseDate/";
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
        
        #===分别在截止时间点前（打鼾噪音数据集）和最新时间点（即干净数据集），使用git blame===#
        for labels_type in list_labels_type:
            print(i_projectName,labels_type);
            
            #存储路径
            dir_path_saved = "%s%s/git_blame_l_from_buggyFileAndLineNum/%s/"%(path_common,labels_type,i_projectName);
            if not os.path.exists(dir_path_saved):
                os.makedirs(dir_path_saved);
            #获得每个BFC被识别的buggy lines
            folderName_BFC = "%s%s/buggyFileAndLineNum_from_git_show/%s/"%(path_common,labels_type,i_projectName);
            commitList = os.listdir(folderName_BFC);
            for i_commit in commitList:
                commitsha = i_commit[i_commit.rfind("_")+1:i_commit.rfind(".")];
                path_i_commit = folderName_BFC + i_commit;
                with open(path_i_commit, 'r', encoding='UTF-8', errors='ignore') as txt:
                    allLine_i_commit = txt.readlines();
                gitBlame_allLine = '';
                for i_line_i_commit in allLine_i_commit:
                    array = i_line_i_commit.split(" ")
                    blameline = array[0]
                    commitsha_pre = array[1]
                    targetFile = array[2].replace('\n', '').replace('\r', '');
#                     blameline = "153,153"
#                     commitsha_pre = "b4d9cc8be1c7440bbfba8473ec1dd7feaf207daa^"
#                     targetFile = "math/src/main/java/org/apache/mahout/math/AbstractVector.java"
                    command = ['-l','-f','-L',blameline,commitsha_pre,targetFile]
                    commit_blame = repo.git_blame_command(command)                
                    gitBlame_allLine += commit_blame + '\n';
                path_saved_fileName = '%s%s_pre.txt'%(dir_path_saved,commitsha)
                with open(path_saved_fileName, 'w', encoding='UTF-8') as wtxt:
                    wtxt.write(gitBlame_allLine);
            
        #===end===#
        print("%s finish"%i_projectName);
    print("all project finish");
        

        

        
        
    

    
    
    
    
    