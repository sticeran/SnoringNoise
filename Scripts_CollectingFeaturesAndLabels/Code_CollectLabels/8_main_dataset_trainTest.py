import pandas as pd
import os


# 在CVDP场景下，为每个项目生成干净的训练集测试集，噪音的训练集测试集
if __name__ == "__main__":

    list_projectName = ["shiro","maven","flume","mahout","calcite","pdfbox","iotdb","tika"];
    
    # "snoring_labels"用于读取snoring时间节点，以生成对应时间的数据集
    
    # 读取路径
    path_common = "D:/workspace/DataFolder/labels_MASZZ/";
    path_common_versionReleaseDate = path_common + "versionReleaseDate/";
    # 读取文件名
    read_fileName_versionReleaseDate = "releaseDate.csv";
    # 存储路径
    path_saved_common = "D:/workspace/DataFolder/data_csv/dataset_new/";
    # 存储文件名,除去项目名外的文件名
    fileName_train_clean = "_train_clean.csv";
    fileName_train_noise = "_train_noise.csv";
    fileName_test_clean = "_test_clean.csv";
    fileName_test_noise = "_test_noise.csv";
    
    
    for i_projectName in list_projectName:
        
        #获得打鼾时间点对应的版本标签
        path_versionReleaseDate = path_common_versionReleaseDate + i_projectName + '/' + read_fileName_versionReleaseDate;
        df_versionReleaseDate = pd.read_csv(path_versionReleaseDate);
        
        #===分别在截止时间点前（打鼾噪音数据集）和最新时间点（即干净数据集），收集缺陷标签===#
        print(i_projectName);
        
        index_cutoff_train = df_versionReleaseDate[df_versionReleaseDate['cutoff']=='train'].index[0];
        index_cutoff_test = df_versionReleaseDate[df_versionReleaseDate['cutoff']=='test'].index[0];
        df_targetVersions_train = df_versionReleaseDate[index_cutoff_train+1:]
        df_targetVersions_train = df_targetVersions_train.reset_index(drop=True)
        df_targetVersions_test = df_versionReleaseDate[index_cutoff_test+1:index_cutoff_train+1]
        df_targetVersions_test = df_targetVersions_test.reset_index(drop=True)
        
        #读取路径
        path_train_clean = "%s/groundtruth_labels/mappingBugsToVersions/%s/"%(path_common,i_projectName);
        path_test_clean = "%s/groundtruth_labels/mappingBugsToVersions/%s/"%(path_common,i_projectName);
        path_train_noise = "%s/snoringTrain_labels/mappingBugsToVersions/%s/"%(path_common,i_projectName);
        path_test_noise = "%s/snoringTest_labels/mappingBugsToVersions/%s/"%(path_common,i_projectName);

        #读取目标版本的标签,生成训练集
        df_train_clean_all = pd.DataFrame();
        df_train_noise_all = pd.DataFrame();
        for i_targetVersion in range(len(df_targetVersions_train)):
            version_current = df_targetVersions_train.loc[i_targetVersion,'version'];
            start_idx = version_current.find('v_')+2;
            version_current = version_current[start_idx:];
            fileName_targetVersion = "%s-%s.csv"%(i_projectName,version_current);#已收集的度量文件名
            print(fileName_targetVersion);#打印当前文件名
            path_train_clean_targetVersion = path_train_clean + fileName_targetVersion;
            path_train_noise_targetVersion = path_train_noise + fileName_targetVersion;
            df_train_clean_targetVersion = pd.read_csv(path_train_clean_targetVersion);
            df_train_noise_targetVersion = pd.read_csv(path_train_noise_targetVersion);
            df_train_clean_targetVersion['Release Number'] = version_current;
            df_train_noise_targetVersion['Release Number'] = version_current;
#             df_train_clean_all = df_train_clean_all.append(df_train_clean_targetVersion);
#             df_train_noise_all = df_train_noise_all.append(df_train_noise_targetVersion);
            df_train_clean_all = pd.concat([df_train_clean_all, df_train_clean_targetVersion], axis=0);
            df_train_noise_all = pd.concat([df_train_noise_all, df_train_noise_targetVersion], axis=0);
        #调整列顺序
        cols = df_train_clean_targetVersion.columns.tolist();
        cols.remove('Release Number');
        cols.insert(1,'Release Number');
        df_train_clean_all = df_train_clean_all[cols];#把'Release Number'列放到第2列
        df_train_noise_all = df_train_noise_all[cols];
        
        #读取目标版本的标签,生成测试集
        df_test_clean_all = pd.DataFrame();
        df_test_noise_all = pd.DataFrame();
        for i_targetVersion in range(len(df_targetVersions_test)):
            version_current = df_targetVersions_test.loc[i_targetVersion,'version'];
            start_idx = version_current.find('v_')+2;
            version_current = version_current[start_idx:];
            fileName_targetVersion = "%s-%s.csv"%(i_projectName,version_current);#已收集的度量文件名
            print(fileName_targetVersion);#打印当前文件名
            path_test_clean_targetVersion = path_test_clean + fileName_targetVersion;
            path_test_noise_targetVersion = path_test_noise + fileName_targetVersion;
            df_test_clean_targetVersion = pd.read_csv(path_test_clean_targetVersion);
            df_test_noise_targetVersion = pd.read_csv(path_test_noise_targetVersion);
            df_test_clean_targetVersion['Release Number'] = version_current;
            df_test_noise_targetVersion['Release Number'] = version_current;
#             df_test_clean_all = df_test_clean_all.append(df_test_clean_targetVersion);
#             df_test_noise_all = df_test_noise_all.append(df_test_noise_targetVersion);
            df_test_clean_all = pd.concat([df_test_clean_all, df_test_clean_targetVersion], axis=0);
            df_test_noise_all = pd.concat([df_test_noise_all, df_test_noise_targetVersion], axis=0);
        #调整列顺序
        cols = df_test_clean_targetVersion.columns.tolist();
        cols.remove('Release Number');
        cols.insert(1,'Release Number');
        df_test_clean_all = df_test_clean_all[cols];#把'Release Number'列放到第2列
        df_test_noise_all = df_test_noise_all[cols];
        
        #存储路径
        dir_path_saved = path_saved_common;
        if not os.path.exists(dir_path_saved):
            os.makedirs(dir_path_saved);
        path_saved_fileName_train_clean = "%s%s%s"%(dir_path_saved,i_projectName,fileName_train_clean);
        path_saved_fileName_train_noise = "%s%s%s"%(dir_path_saved,i_projectName,fileName_train_noise);
        path_saved_fileName_test_clean = "%s%s%s"%(dir_path_saved,i_projectName,fileName_test_clean);
        path_saved_fileName_test_noise = "%s%s%s"%(dir_path_saved,i_projectName,fileName_test_noise);
        df_train_clean_all.to_csv(path_saved_fileName_train_clean,index=False);#不保存行索引
        df_train_noise_all.to_csv(path_saved_fileName_train_noise,index=False);#不保存行索引
        df_test_clean_all.to_csv(path_saved_fileName_test_clean,index=False);#不保存行索引
        df_test_noise_all.to_csv(path_saved_fileName_test_noise,index=False);#不保存行索引
        #===end===#
        print("%s finish"%i_projectName);
    print("all project finish");
        
        
        

        
        
    

    
    
    
    
    