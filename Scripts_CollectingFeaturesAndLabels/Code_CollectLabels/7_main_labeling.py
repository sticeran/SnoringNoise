import pandas as pd
import os


# 这一步要在度量收集完成后进行
# 获得数据集标签
if __name__ == "__main__":

    list_projectName = ["shiro","maven","flume","mahout","calcite","pdfbox","iotdb","tika"];
    
    # "snoring_labels"用于读取snoring时间节点，以生成对应时间的标签数据
    list_labels_type = ["snoringTrain_labels","snoringTest_labels","groundtruth_labels"]
    
    # 读取路径
    path_common = "D:/workspace/DataFolder/labels_MASZZ/";
    path_common_metrics = "D:/workspace/DataFolder/features/changeMetrics/";
    path_common_versionReleaseDate = path_common + "versionReleaseDate/";
    # 读取文件名
    read_fileName_versionReleaseDate = "releaseDate.csv";
    
    
    for i_projectName in list_projectName:
        
        #获得打鼾时间点对应的版本标签
        path_versionReleaseDate = path_common_versionReleaseDate + i_projectName + '/' + read_fileName_versionReleaseDate;
        df_versionReleaseDate = pd.read_csv(path_versionReleaseDate);
        
        #===分别在截止时间点前（打鼾噪音数据集）和最新时间点（即干净数据集），收集缺陷标签===#
        for labels_type in list_labels_type:
            print(i_projectName,labels_type);
            
            if labels_type == "snoringTrain_labels":
                index_cutoff = df_versionReleaseDate[df_versionReleaseDate['cutoff']=='train'].index[0];
                df_targetVersions = df_versionReleaseDate[index_cutoff+1:]
                df_targetVersions = df_targetVersions.reset_index(drop=True)
            elif labels_type == "snoringTest_labels":
                index_cutoff = df_versionReleaseDate[df_versionReleaseDate['cutoff']=='test'].index[0];
                df_targetVersions = df_versionReleaseDate[index_cutoff+1:]
                df_targetVersions = df_targetVersions.reset_index(drop=True)
            else:
                df_targetVersions = df_versionReleaseDate
            
            #BIC和BFC
            path_buggyIntervals = "%s%s/bugIntroducingTime_and_bugFixingtime/%s/buggyLinesIntervals.csv"%(path_common,labels_type,i_projectName);
            df_buggyIntervals = pd.read_csv(path_buggyIntervals);
            #存储路径
            dir_path_saved = "%s%s/mappingBugsToVersions/%s/"%(path_common,labels_type,i_projectName);
            if not os.path.exists(dir_path_saved):
                os.makedirs(dir_path_saved);
            
            #为文件，以及BIC和BFC建立字典（哈希）
            dict_BIC_BFC = {}
            for i_row in range(len(df_buggyIntervals)):
                filename = df_buggyIntervals.loc[i_row,'bugFilename'];
                bugIntroducingTime = df_buggyIntervals.loc[i_row,'bugIntroducingTime'];
                bugFixingTime = df_buggyIntervals.loc[i_row,'bugFixingTime'];
                pair_BIC_BFC = (bugIntroducingTime,bugFixingTime);
                list_value = [pair_BIC_BFC];
                if filename in dict_BIC_BFC:
                    dict_BIC_BFC[filename].append(pair_BIC_BFC);
                else:
                    dict_BIC_BFC[filename] = list_value;
                
            # 为每个版本的数据生成bug标签
            for i_targetVersion in range(len(df_targetVersions)):
                version_current = df_targetVersions.loc[i_targetVersion,'version']
                start_idx = version_current.find('v_')+2;
                version_current = version_current[start_idx:];
                fileName_targetVersion = "%s-%s.csv"%(i_projectName,version_current)#已收集的度量文件名
                print(fileName_targetVersion)#打印当前文件名
                
                #当前版本日期
                releaseDate_current = df_targetVersions.loc[i_targetVersion,'releaseDate']
                
                # 读当前版本的度量文件（不含bug标签）
                path_metrics = "%s/%s/%s"%(path_common_metrics,i_projectName,fileName_targetVersion)
                df_metrics = pd.read_csv(path_metrics);
                
                # 判断bug标签
                bug_label = [False for x in range(len(df_metrics))]
                for i in range(len(df_metrics)):
                    filename = df_metrics.loc[i,'File']
                    print(filename)
                    if filename in dict_BIC_BFC:
                        list_value = dict_BIC_BFC[filename]
                        for i_pair_BIC_BFC in list_value:
                            bugIntroducingTime = i_pair_BIC_BFC[0]
                            bugFixingTime = i_pair_BIC_BFC[1]
                            if bugIntroducingTime <= releaseDate_current and releaseDate_current <= bugFixingTime:
                                bug_label[i] = True
                                break;
                
                # 获得bug标签列
                df_metrics['Actual'] = bug_label;
                
                # 存入文件
                path_saved_fileName = dir_path_saved + fileName_targetVersion;
                df_metrics.to_csv(path_saved_fileName,index=False);#不保存行索引
        #===end===#
        print("%s finish"%i_projectName);
    print("all project finish");
        
        
        

        
        
    

    
    
    
    
    