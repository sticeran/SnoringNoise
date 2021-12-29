import os
# allFileNum = 0
#该函数有递归，改动时需注意
#    得到所有文件类型的文件
def getFileList(level, path, path_initial, fileList, fileList_fileName, allFileNum):#使用堆上的匿名参数来实现一个累加器
#     global allFileNum
    '''
    打印一个目录下的所有文件夹和文件 
    '''   
    # 所有文件
    fileList_onlyFileName = []
    # 返回一个列表，其中包含在目录条目的名称
    files = os.listdir(path)
    for f in files:
        temp = path + '/' + f
        if(os.path.isdir(temp)):         
            if(f[0] != '.'):    # 排除隐藏文件夹。因为可能会有隐藏文件夹
                print ('-' * level, f)
                # 打印目录下的所有文件夹和文件，目录级别+1
                getFileList((level + 1), temp, path_initial, fileList, fileList_fileName, allFileNum)  #recursion
        if(os.path.isfile(temp)):
            # 添加文件
            fileList_onlyFileName.append(f)
            fileList_fileName.append(f)
            filefullName = temp.replace(path_initial, "" ,1)
            fileList.append(filefullName)
    for fl in fileList_onlyFileName:
        # 打印文件
        print ('-' * level, fl)
        # 顺便计算一下有多少个文件
        allFileNum[0] = allFileNum[0] + 1
        #int(allFileNum[0])


#    得到java类型的文件
def getFileList_java(level, path, path_initial, fileList, fileList_fileName, allFileNum):#使用堆上的匿名参数来实现一个累加器
#     global allFileNum
    '''
    打印一个目录下的所有文件夹和文件 
    '''   
    # 所有文件
    fileList_onlyFileName = []
    # 返回一个列表，其中包含在目录条目的名称
    files = os.listdir(path)
    for f in files:
        temp = path + '/' + f
        if(os.path.isdir(temp)):         
            if(f[0] != '.'):    # 排除隐藏文件夹。因为可能会有隐藏文件夹
#                 print ('-' * level, f)
                # 打印目录下的所有文件夹和文件，目录级别+1
                getFileList_java((level + 1), temp, path_initial, fileList, fileList_fileName, allFileNum)  #recursion
        if(os.path.isfile(temp)):
            if '.java' == os.path.splitext(temp)[-1]:
                # 添加文件
                fileList_onlyFileName.append(f)
                fileList_fileName.append(temp)
                filefullName = temp.replace(path_initial, "" ,1)
                fileList.append(filefullName)
    for fl in fileList_onlyFileName:  # @UnusedVariable
        # 打印文件
#         print ('-' * level, fl)
        # 顺便计算一下有多少个文件
        allFileNum[0] = allFileNum[0] + 1
        #int(allFileNum[0])

# # 文件过滤
# def flieFiltering(pathName_project, fileList,dic_dataset):
#     num=0;
#     for fl in fileList:
#         #这里判断是否是用户打分的java类，如果是，读内容，计算overlap和stasis
#         if dic_dataset.__contains__(fl):
#             num+=1;
#             filePath = pathName_project + "/" + fl;
#             fopen = open(filePath, 'r');
# #             fileread = fopen.read();
#             fopen.close();
#     print(num);
#

# if __name__ == '__main__':
#     pathName_codeCommon = "D:/";
#     pathName_project = pathName_codeCommon + "testA";
#     level = 1;#目录层级
#     path_initial = pathName_project+"/";#在递归时需要计算减去，和csv文件路径名一致
#     fileList = [];#储存读出的文件
#     fileList_fileName = [];#存储不包括路径的文件名
#     allFileNum=[0];
#     
#     getFileList(level, pathName_project, path_initial, fileList, fileList_fileName, allFileNum)
#     print ('总文件数 =', allFileNum)