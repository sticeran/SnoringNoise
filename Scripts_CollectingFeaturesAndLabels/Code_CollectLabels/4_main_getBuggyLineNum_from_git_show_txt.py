# -*- coding: utf-8 -*-
"""
Created on Tue Dec 07 15:44:51 2019

@author:
"""

#要忽略非java文件，忽略文件中空行、格式更改的修改

import codecs
import os
import re
import traceback



#过滤每个文件的修改区域中的修改多行注释和格式变更
def filterEmptyAndFormatChange(list_preModifiedLines,list_nowModifiedLines,list_preModifiedLinesPosition_onePairField):#两个参数均已去除空行和//单行注释
    #那种段落注释没法完全避免，因为git只显示一小段，所以有时只能去除段落注释修改的第一行*/和最后一行*/
    paragraphAnnotation_pre_startPosition = -1;
    paragraphAnnotation_pre_endPosition = -1;
    paragraphAnnotation_now_startPosition = -1;
    paragraphAnnotation_now_endPosition = -1;
    
    #去除'-'号区域段落注释，如果有的话。不考虑多层注释里嵌套多层注释。已知在此之前已去掉了单行中多行注释符包裹的语句。
    #存在这种类型的，所以要再想办法。不能简单的记录'*/'和'/*'出现的位置。
#     list_preModifiedLines = ['aaa','/*aaa','bbb','ccc*/','*paragraphId', '*/', 'aaa{', '*/',
#                              'StringnoteId=interpreterContext.getNoteId();','/*aaa','bbb','ccc*/', '}', '/**', 
#                              '*Runparagraphbyid', '*noteId','/*aaa','bbb','ccc*/','ggg']#调试用
    num_left = 0;#/*次数
    num_right = 0;#*/次数
    i = 0;
    len_list_preModifiedLines = len(list_preModifiedLines);
    while i < len_list_preModifiedLines:
        if len(list_preModifiedLines[i])>=2:
            temp_oneLine_start = list_preModifiedLines[i][0:2];
            temp_oneLine_end = list_preModifiedLines[i][-2:];
            if temp_oneLine_start == "/*":
                if num_left <= num_right:
                    paragraphAnnotation_pre_startPosition = i;
                num_left += 1;
            if temp_oneLine_end == "*/":
                paragraphAnnotation_pre_endPosition = i+1;
                num_right += 1;
            if paragraphAnnotation_pre_startPosition!= -1 and paragraphAnnotation_pre_endPosition != -1:
                if num_left == num_right:
                    if paragraphAnnotation_pre_startPosition <= paragraphAnnotation_pre_endPosition:
                        del list_preModifiedLines[paragraphAnnotation_pre_startPosition:paragraphAnnotation_pre_endPosition];
                        del list_preModifiedLinesPosition_onePairField[paragraphAnnotation_pre_startPosition:paragraphAnnotation_pre_endPosition];
                        i = i - (paragraphAnnotation_pre_endPosition - paragraphAnnotation_pre_startPosition);
                        len_list_preModifiedLines = len_list_preModifiedLines - (paragraphAnnotation_pre_endPosition - paragraphAnnotation_pre_startPosition);
                        paragraphAnnotation_pre_startPosition = -1;
                        paragraphAnnotation_pre_endPosition = -1;
                        num_left -= 1;
                        num_right -= 1;
                    else:
                        del list_preModifiedLines[0:paragraphAnnotation_pre_endPosition];
                        del list_preModifiedLinesPosition_onePairField[0:paragraphAnnotation_pre_endPosition];
                        i -= paragraphAnnotation_pre_endPosition - 0;
                        len_list_preModifiedLines -= paragraphAnnotation_pre_endPosition - 0;
                        paragraphAnnotation_pre_startPosition -= paragraphAnnotation_pre_endPosition - 0;
                        paragraphAnnotation_pre_endPosition = -1;
                        num_right -= 1;
                elif num_right > num_left:
                    del list_preModifiedLines[0:paragraphAnnotation_pre_endPosition];
                    del list_preModifiedLinesPosition_onePairField[0:paragraphAnnotation_pre_endPosition];
                    i -= paragraphAnnotation_pre_endPosition - 0;
                    len_list_preModifiedLines -= paragraphAnnotation_pre_endPosition - 0;
                    paragraphAnnotation_pre_startPosition -= paragraphAnnotation_pre_endPosition - 0;
                    paragraphAnnotation_pre_endPosition = -1;
                    num_right = 0;
        i += 1;
    if num_left > 0:
        del list_preModifiedLines[paragraphAnnotation_pre_startPosition:];
        del list_preModifiedLinesPosition_onePairField[paragraphAnnotation_pre_startPosition:];
    
    #去除'+'号区域段落注释，如果有的话。不考虑多层注释里嵌套多层注释。已知在此之前已去掉了单行中多行注释符包裹的语句。
    num_left = 0;#/*次数
    num_right = 0;#*/次数
    i = 0;
    len_list_nowModifiedLines = len(list_nowModifiedLines);
    while i < len_list_nowModifiedLines:
        if len(list_nowModifiedLines[i])>=2:
            temp_oneLine_start = list_nowModifiedLines[i][0:2];
            temp_oneLine_end = list_nowModifiedLines[i][-2:];
            if temp_oneLine_start == "/*":
                if num_left <= num_right:
                    paragraphAnnotation_now_startPosition = i;
                num_left += 1;
            if temp_oneLine_end == "*/":
                paragraphAnnotation_now_endPosition = i+1;
                num_right += 1;
            if paragraphAnnotation_now_startPosition!= -1 and paragraphAnnotation_now_endPosition != -1:
                if num_left == num_right:
                    if paragraphAnnotation_now_startPosition <= paragraphAnnotation_now_endPosition:
                        del list_nowModifiedLines[paragraphAnnotation_now_startPosition:paragraphAnnotation_now_endPosition];
                        i = i - (paragraphAnnotation_now_endPosition - paragraphAnnotation_now_startPosition);
                        len_list_nowModifiedLines = len_list_nowModifiedLines - (paragraphAnnotation_now_endPosition - paragraphAnnotation_now_startPosition);
                        paragraphAnnotation_now_startPosition = -1;
                        paragraphAnnotation_now_endPosition = -1;
                        num_left -= 1;
                        num_right -= 1;
                    else:
                        del list_nowModifiedLines[0:paragraphAnnotation_now_endPosition];
                        i -= paragraphAnnotation_now_endPosition - 0;
                        len_list_nowModifiedLines -= paragraphAnnotation_now_endPosition - 0;
                        paragraphAnnotation_now_startPosition -= paragraphAnnotation_now_endPosition - 0;
                        paragraphAnnotation_now_endPosition = -1;
                        num_right -= 1;
                elif num_right > num_left:
                    del list_nowModifiedLines[0:paragraphAnnotation_now_endPosition];
                    i -= paragraphAnnotation_now_endPosition - 0;
                    len_list_nowModifiedLines -= paragraphAnnotation_now_endPosition - 0;
                    paragraphAnnotation_now_startPosition -= paragraphAnnotation_now_endPosition - 0;
                    paragraphAnnotation_now_endPosition = -1;
                    num_right = 0;
        i += 1;
    if num_left > 0:
        del list_nowModifiedLines[paragraphAnnotation_now_startPosition:];
    
    #去除'-'号区域修改行中的开头是/*或*/的行（此时/*或*/不成双）
    #list_preModifiedLines = ['ggg','*','{','ccc*/','ggg','/*ccc','ddd','eee*/','ggg'];#调试用
    i = 0;
    len_list_preModifiedLines = len(list_preModifiedLines);
    while i < len_list_preModifiedLines:
        if len(list_preModifiedLines[i])>=2:
            temp_oneLine_start = list_preModifiedLines[i][0:2];
            temp_oneLine_end = list_preModifiedLines[i][-2:];
            if temp_oneLine_start == "/*" or temp_oneLine_start[0] == "*":#如果每一行前面都是/*或*也是多层注释，需要删掉
                del list_preModifiedLines[i];
                del list_preModifiedLinesPosition_onePairField[i];
                i = i - 1;
                len_list_preModifiedLines = len_list_preModifiedLines - 1;
                i += 1;
                continue;
            if temp_oneLine_end == "*/":
                del list_preModifiedLines[i];
                del list_preModifiedLinesPosition_onePairField[i];
                i = i - 1;
                len_list_preModifiedLines = len_list_preModifiedLines - 1;
        elif len(list_preModifiedLines[i])<2:
            if list_preModifiedLines[i] == "*":
                del list_preModifiedLines[i];
                del list_preModifiedLinesPosition_onePairField[i];
                i = i - 1;
                len_list_preModifiedLines = len_list_preModifiedLines - 1;            
        i += 1;

    #去除'+'号区域修改行中的开头是/*或*/的行（此时/*或*/不成双）
    i = 0;
    len_list_nowModifiedLines = len(list_nowModifiedLines);
    while i < len_list_nowModifiedLines:
        if len(list_nowModifiedLines[i])>=2:
            temp_oneLine_start = list_nowModifiedLines[i][0:2];
            temp_oneLine_end = list_nowModifiedLines[i][-2:];
            if temp_oneLine_start == "/*" or temp_oneLine_start[0] == "*":#如果每一行前面都是/*或*也是多层注释，需要删掉:
                del list_nowModifiedLines[i];
                i = i - 1;
                len_list_nowModifiedLines = len_list_nowModifiedLines - 1;
                i += 1;
                continue;
            if temp_oneLine_end == "*/":
                del list_nowModifiedLines[i];
                i = i - 1;
                len_list_nowModifiedLines = len_list_nowModifiedLines - 1;
        elif len(list_nowModifiedLines[i])<2:
            if list_nowModifiedLines[i] == "*":
                del list_nowModifiedLines[i];
                i = i - 1;
                len_list_nowModifiedLines = len_list_nowModifiedLines - 1;
        i += 1;

    #去除{}和换行符，然后判断是否只是格式更改
    str_preModifiedLines = ''.join(list_preModifiedLines);
    str_preModifiedLines = re.sub("({|})", '', str_preModifiedLines);
    str_nowModifiedLines = ''.join(list_nowModifiedLines);
    str_nowModifiedLines = re.sub("({|})", '', str_nowModifiedLines);
    if str_preModifiedLines == str_nowModifiedLines:#说明只是格式更改
        list_preModifiedLinesPosition_onePairField.clear();

#对于一个git show中的一个修改文件的一个修改区域(@@到另一个@@或文件结束位置为止)，先分对儿，'-''+'号一对儿，或只有'-'号，为了便于后续去掉多行注释/**/和格式变更
def dividedIntoPairOfModifiedLines(rep,i_position_start,i_position_end):
    list_preModifiedLinesPosition_allPairField = [];#记录当前修改文件的一个完整的修改区域(@@到另一个@@或文件结束位置为止)中，所有成对儿的区域中有效的被修改行的位置
    
    #获得当前@@后面-号后的在原文件中的起始位
    start1 = int(rep[i_position_start].index('-'))+1
    end1 = int(rep[i_position_start].index(','))
    minus_start_line = rep[i_position_start][start1:end1]#显示原文件被修改的范围的起始行号
    j_underAtAt = -1;#记录@@下第几行，minus_start_line + j_underAtAt = 在原文件中的正确行号
    
    i = i_position_start+1;
    while i < i_position_end:
        list_preModifiedLines = [];#记录一个成对儿的区域中，在上一次提交中被修改的文件中被修改的行，即'-'行。之所以用list是为了之后好处理单行注释
        list_nowModifiedLines = [];#记录一个成对儿的区域中，在当前提交中被修改的文件中被修改后的行，即'+'行。之所以用list是为了之后好处理单行注释
        list_preModifiedLinesPosition_onePairField = [];#记录一个成对儿的区域中，被修改的行的位置的
        flagPair_minus = 0;#如果flagPair_minus和flagPair_plus两个都是1表示'+'之前有紧接着的'-'，只有一个1表示'-'之后没有紧接着的'+'，都是0表示'+'之前没有紧接着的'-'或'-'已在之前成对儿。
        flagPair_plus = 0;
        
        #import是否需要过滤掉？不能过滤
#         #截取字符串前8个字符，看是否包含import
#         if rep[i][0:8].find('import')!=-1:
#             continue;#跳过文件头的import语句
        
        #判断在前面没有'-'号的情况下，一行的最前面是否有'+'号，如果有则是新增行，需要不计入修改前文件行数
        if flagPair_minus == 0 and rep[i][0] == '+':
            i += 1;
            continue;
        
        if rep[i] == '\r\n':#原文件和git show中均没有，由于存文件的特殊格式导致多余的空行。不算做原文件行数。
            i += 1;
            continue;
        
        #记录在修改前文件行数
        if rep[i][0] != '+' and rep[i][0] != '-' and rep[i] != '\r\n':
            j_underAtAt += 1;
        
        #判断每一行最前面是否有'-'号
        if rep[i][0] == '-':
            while i < i_position_end:
                if rep[i][0] == '-':
                    j_underAtAt += 1;
#                     rep[i] = "- 123 /* abc */ 456 /* abc */ 789 //123 \r\n";
                    rep[i] = rep[i][1:];#去最前面的'-号'
                    rep[i] = re.sub("/[*](.*?)[*]/", '', rep[i], re.S);#去掉一行中的/**/包裹起来的注释。假设/**/无嵌套。
                    rep[i] = re.sub("//.*", '', rep[i], re.S);#去掉一行中的//引导的注释
                    rep[i] = re.sub("@(\S)*|@(\S)*$", '', rep[i], re.S);#去掉@引导的注解
                    rep[i] = re.sub("\t", '', rep[i], re.S);#去横向制表符
                    rep[i] = rep[i].replace(' ', '');#去空格
                    rep[i] = re.sub("(\r|\n)", '', rep[i], re.S);#去掉末尾的换行符，不然干扰由多行注释符包裹/**/的单行注释行的判断
                    if rep[i] == "":#空行中不用额外去换行符。去换行符是为了上面的目的。
#                         j_underAtAt += 1;
                        i+=1;
                        continue;
                    else:
                        flagPair_minus = 1;#构成可成对儿条件的一半
                        list_preModifiedLines.append(rep[i]);#记录去掉'-'号单行内注释空格换行符后的语句
                        theCorrectLinePosition = int(minus_start_line) + j_underAtAt;#在原文件中正确行号
                        list_preModifiedLinesPosition_onePairField.append(theCorrectLinePosition);#记录正确行号
                elif rep[i][0] == '+':
                    flagPair_plus = 1;#构成可成对儿条件的一半
                    break;
                elif rep[i] == '\r\n':
                    i+=1;
                    continue;
                else:#前面既没减号也没加号，即未修改的语句
                    break;
#                 j_underAtAt += 1;
                i+=1;
        
        #如果前面有'-'号且后面无连续的'+'号
        if flagPair_minus == 1 and flagPair_plus == 0:
            list_nowModifiedLines.append('');#赋值为空，表示该'-'号后面成对儿的'+'号是空
        
        #判断每一行最前面是否有'+'号
        if flagPair_minus == 1 and flagPair_plus == 1 and rep[i][0] == '+':
            while i < i_position_end:
                if rep[i][0] == '+':
                    rep[i] = rep[i][1:];#去最前面的'+号'
                    rep[i] = re.sub("/[*](.*?)[*]/", '', rep[i], re.S);#去掉一行中的/**/包裹起来的注释。假设/**/无嵌套。
                    rep[i] = re.sub("//.*", '', rep[i], re.S);#去掉一行中的//引导的注释
                    rep[i] = re.sub("@(\S)*|@(\S)*$", '', rep[i], re.S);#去掉@引导的注解
                    rep[i] = re.sub("\t", '', rep[i], re.S);#去横向制表符
                    rep[i] = rep[i].replace(' ', '');#去空格
                    rep[i] = re.sub("(\r|\n)", '', rep[i], re.S);#去掉末尾的换行符，不然干扰由多行注释符包裹/**/的单行注释行的判断
                    if rep[i] == "":#空行中不用额外去换行符。去换行符是为了上面的目的。
#                         j_underAtAt += 1;
                        i+=1;
                        continue; 
                    else:
                        list_nowModifiedLines.append(rep[i]);#记录去掉'+'号单行内注释空格换行符后的语句
                elif rep[i][0] == '-':
                    j_underAtAt += 1;
                    flagPair_minus = 0;#已到连续的'+'号最后一行的后一行，成对儿标志重新置0
                    flagPair_plus = 0;
#                     j_underAtAt -= 1;
                    i-=1;#因为当前i已加了1但没做处理'-'号，而'-'号需要另外处理，所以需要重新减1
                    break;
                elif rep[i] == '\r\n':
                    i+=1;
                    continue;
                else:#前面既没减号也没加号，即未修改的语句
                    j_underAtAt += 1;
                    flagPair_minus = 0;#已到连续的'+'号最后一行的后一行，成对儿标志重新置0
                    flagPair_plus = 0;
                    break;
#                 j_underAtAt += 1;
                i+=1;
        
        if list_preModifiedLines:
            #调用过滤多行注释和格式更改的函数。去除多行注释和格式更改的行后，记录行位置的列表也需要做相应的变更。
            filterEmptyAndFormatChange(list_preModifiedLines,list_nowModifiedLines,list_preModifiedLinesPosition_onePairField);
            #一个'-'号'+'号成对儿的区域中，有效的行修改位置附加到总列表中去
            list_preModifiedLinesPosition_allPairField.extend(list_preModifiedLinesPosition_onePairField);
        i += 1;
#         j_underAtAt += 1;
    return list_preModifiedLinesPosition_allPairField;
        
#获得每个被修改的文件的所有'@@'行的位置
def getModifiedLinePosition(rep,i_line):
    list_atatPosition = [];#'@@'行的位置，记录一个文件下的所有@@位置。去空等不在这里判断，避免一个方法写得太大太复杂。
    
    start1 = int(rep[i_line].index('-'))+1
    end1 = int(rep[i_line].index(','))+1
    start2 = end1
    end2 = int(rep[i_line].index('+'))-1
    minus_start_line = rep[i_line][start1:end1]#显示原文件被修改的范围的起始行号
    minus_end_line = rep[i_line][start2:end2]#显示原文件被修改的范围的结束行号
    
    if minus_start_line == 0 and minus_end_line == 0:#说明是纯新增的，无修改行
        print (minus_start_line,minus_end_line);
    else:
        list_atatPosition.append(i_line);
    
    for i in range(i_line+1,len(rep)):
#         print(rep[i])
        if rep[i][0:2] == '@@':
            start1 = int(rep[i].index('-'))+1
            end1 = int(rep[i].index(','))+1
            start2 = end1
            end2 = int(rep[i].index('+'))-1
            minus_start_line = rep[i][start1:end1]#显示原文件被修改的范围的起始行号
            minus_end_line = rep[i][start2:end2]#显示原文件被修改的范围的结束行号
            
            if minus_start_line == 0 and minus_end_line == 0:#说明是纯新增的，无修改行
                continue;
            else:
                list_atatPosition.append(i);#@@在当前rep中的位置

        if rep[i][0:10] == 'diff --git':
            list_atatPosition.append(i);#对于最后一个@@,后面的修改区域的结束范围
            i-=1;#因为当前i已加了1但没做处理，所以需要重新减1
            return list_atatPosition,i;#到另一个文件了，返回
    list_atatPosition.append(i);#对于最后一个文件的最后一个@@,后面的修改区域的结束范围
    return list_atatPosition,i;#该git show内容读完了，返回    


#在这一步得到时间，空文件不写。
# 使用MA-SZZ算法获取有效的被修复的java文件名，有效的被修改的行的行号
if __name__ == "__main__":
    
    projectName_list = ["shiro","maven","flume","mahout","calcite","pdfbox","iotdb","tika"];
    
    #"snoring_labels"用于读取snoring时间节点前的提交日志
    list_labels_type = ["snoringTrain_labels","snoringTest_labels","groundtruth_labels"]
    
    for project in projectName_list:
        for labels_type in list_labels_type:
            print("\n",project,labels_type,);
            fileNames_commits = os.listdir(r'D:\workspace\DataFolder\ThirdResearchPoint\labels_MASZZ\%s\git_show_bugFixingCommitsID\%s'%(labels_type,project))
            for str_i_filename in fileNames_commits:
#                 str_i_filename = "2fbaf8957318e45ac54089f60aae8a396c614b17.txt";#调试用
                try:
                    txt = codecs.open(r'D:\workspace\DataFolder\ThirdResearchPoint\labels_MASZZ\%s\git_show_bugFixingCommitsID\%s\%s'%(labels_type,project,str_i_filename),'r','utf-8')
#                     txt = codecs.open(r'D:\workspace\DataFolder\ThirdResearchPoint\labels_MASZZ\%s\git_show_bugFixingCommitsID\%s\%s'%(labels_type,project,str_i_filename),'rb','utf_16_le')#UTF-16LE，其后缀是 LE 即 little-endian，小端的意思。小端就是将高位的字节放在高地址表示。
        #             txt = codecs.open(r'D:\workspace\mixed-workspace\mySZZ\git_show_bugFixingCommitsID\%s\%s'%(project,str_i_filename),'r')
                    rep = txt.readlines()
                    
                    wtxt_contents = '';#要往文件中写的内容
                    
                    print (str_i_filename)
                    end = str_i_filename.index('.')
                    commitsha = str_i_filename[:end]
        #             print (commitsha)
                    
    #                 time_fixingBug_commit = '';
    #                 #获取修复Bug的提交时间。commit中第二行不一定是date,也可能是author
    #                 if rep[2][0:4] == "Date":
    #                     time_fixingBug_commit = rep[2][8:-8];#在show信息中，第三行是时间，且时间有固定格式
    #                     time_fixingBug_commit = datetime.datetime.strptime(time_fixingBug_commit,'%a %b %d %H:%M:%S %Y');
    #                     time_fixingBug_commit = str(time_fixingBug_commit);
    #                 elif rep[3][0:4] == "Date":
    #                     time_fixingBug_commit = rep[3][8:-8];#在show信息中，第三行是时间，且时间有固定格式
    #                     time_fixingBug_commit = datetime.datetime.strptime(time_fixingBug_commit,'%a %b %d %H:%M:%S %Y');
    #                     time_fixingBug_commit = str(time_fixingBug_commit);
    #                 if rep[2][0:4] != "Date" and rep[3][0:4] != "Date":
    #                     print("error");
                    
                    #rep要读两遍，第一遍判断修改的有无修改的java文件，过滤非java文件和新增文件。并且获得每个被修改的文件的所有'@@'行的位置。
                    #第二遍，记录每个被修改的java文件名下有效的修改行的正确行号。有效的修改行指的是被空格空行格式修改的修改行。正确行号指的是被修改的区域的起始行号加'-'号的位置。
        
                    #对于@@下面的修改行：首先去掉空行、空格和//单行注释行。
                    #然后对于连续的成对的减号区域和加号区域，去除多行注释行，以及只包含（/* */）一侧的单行。
                    #最后将剩余代码合并成一行，判断是否仅仅是格式更改。
                    #如果不是格式修改，则将去掉空行、空格和注释的减号位置记录到文件中去。
                    
                    #不一定先出现减号再出现加号，有实例。所以只有判断到有减号时，才判断之后是否有加号，无加号赋值为""，然后进行上面的处理。
                    
                    list_modifiedFile = [];#存修改的java文件名
                    list_allAtAtPosition = [];#存list，每个list内容是一个文件下所有@@位置
                    list_buggyLineNum_oneFile_inPre = [];#存list，每个list内容是一个文件下两个@@位置之间所有有效的正确修改行位置
                    
                    len_rep = len(rep)#文件长
                    #===记录修改的java文件名和被修改的@@行号位置===#
                    bool_existModifiedJavaFile = False;#是否存在修改的java文件，需要True
                    i = -1;
                    while i < len_rep:
                        i += 1;
                        if i>= len_rep:
                            break;
        #                 print (rep[i])#打印当前语句
                        
                        #===判断是否存在修改的java文件，相当于过滤非java文件===#经测试文件名可以不等，路径可以不等。
                        #需要判断'diff --git'下面语句是否有similarity index 100%，避免仅仅是路径或文件名的变化。
                        if rep[i][0:10] == 'diff --git':
                            rep[i] = rep[i].replace('"','')#去掉文件名前可能存在的引号
                            fstart = int(rep[i].index(' a/'))+3
                            fend = int(rep[i].index(' b/'))
                            filename_a = rep[i][fstart:fend].strip()
                            fstart_b = fend+3
                            filename_b = rep[i][fstart_b:].strip()
                            filename_a_suffix = filename_a[-5:]#截取后缀.java的长度
                            filename_b_suffix = filename_b[-5:]
                            if filename_a_suffix == ".java" and filename_b_suffix == ".java":
                                if rep[i+1].find("similarity index 100%")!=-1:
                                    bool_existModifiedJavaFile = False;
                                else:
                                    bool_existModifiedJavaFile = True;#暂时赋值为true，后续再靠"--- /dev/null"判断
                            continue;#跳过后续if
                        #===end===#
                        
                        #===判断修改的java文件是否不是新增的文件，如果不是获得在上一次提交中被修改的文件名和所有@@位置===#
                        if bool_existModifiedJavaFile:
                            if rep[i][0:2] == '@@':
                                #需要判断'@@'上面两行语句是否存在--- /dev/null和+++ b/xxx.txt的形式。避免纯新增文件。
                                #需要判断'@@'上面一行语句是否存在--- a/xxx.txt和+++ /dev/null的形式。避免纯删除文件，因为没有修改代码行。
                                if rep[i-2].find("--- /dev/null")==-1 and rep[i-1].find("+++ /dev/null")==-1:#没找到
                                    #记录修改的文件名和该文件名下所有@@位置，以便进一步去掉格式更改
                                    list_modifiedFile.append(filename_a);
                                    #调用获得每个被修改的文件的所有'@@'行的位置函数
                                    tempList,i = getModifiedLinePosition(rep,i);#一个文件下所有@@位置
                                    list_allAtAtPosition.append(tempList);##存列表，每个列表中内容是一个文件下所有@@位置
                                    bool_existModifiedJavaFile = False;#一个文件下所有@@位置已经处理完了，重新赋值为false
                                else:
                                    bool_existModifiedJavaFile = False;#是新增文件
                        #===end===#
                    #===end===#
                    
                    #===记录每个被修改的java文件名下被非空格空行格式修改的修改的行的行号===#
                    len_list_modifiedFile = len(list_modifiedFile);#一次提交中被修改的java文件数
                    for i_modifiedFile in range(len_list_modifiedFile):
                        list_buggyLineNum_oneFile_inPre.clear();
                        list_atAtPosition_oneFile = list_allAtAtPosition[i_modifiedFile];#list_atAtPosition_oneFile是一个文件下所有@@位置
                        for j in range(0,len(list_atAtPosition_oneFile)-1,1):#已知list_atAtPosition_oneFile一定大于等于2
                            i_position_start = list_atAtPosition_oneFile[j];#第一个@@位置
                            i_position_end = list_atAtPosition_oneFile[j+1];#后一个@@位置或文件结束位置
                            #调用函数：获得一个@@到另一个@@为止，有效的行修改位置
                            temp_list_correctPositionOfValidModified = dividedIntoPairOfModifiedLines(rep,i_position_start,i_position_end);#函数返回一个文件下两个@@位置之间所有有效的正确修改行位置
                            #把一个文件下所有@@到另一个@@区域中，有效的行修改位置附加到总列表中去
                            list_buggyLineNum_oneFile_inPre.extend(temp_list_correctPositionOfValidModified);#记录一个文件下所有两个@@位置之间所有有效的正确修改行位置
                        
                        #把有效修改行位置写入文件
                        if list_buggyLineNum_oneFile_inPre:
                            for ex_line in list_buggyLineNum_oneFile_inPre:
                                exd_line = ex_line;
                                filename_modified = list_modifiedFile[i_modifiedFile];
                                wtxt_contents += str(ex_line)+','+str(exd_line)+' '+commitsha+'^'+' '+filename_modified+'\n';
    #                             wtxt.write(str(ex_line)+','+str(exd_line)+' ')
    #                             wtxt.write(commitsha+'^'+' ')
    #                             wtxt.write(filename_modified)
    # #                             wtxt.write(filename_modified+' ')
    # #                             wtxt.write(time_fixingBug_commit);#获取修复时间，修复bug的提交的时间
    #                             wtxt.write('\n')
                    
                    txt.close()
                    if wtxt_contents != '':
                        dir_path_saved = r'D:\workspace\DataFolder\ThirdResearchPoint\labels_MASZZ\%s\buggyFileAndLineNum_from_git_show\%s'%(labels_type,project);
                        if not os.path.exists(dir_path_saved):
                            os.makedirs(dir_path_saved);
                        path_saved_fileName = '%s/buggyFileAndLineNum_%s'%(dir_path_saved,str_i_filename);
                        wtxt = open(path_saved_fileName,'w')
                        wtxt.write(wtxt_contents)
                        wtxt.close()
                    #===end===#
                    
                    
                except Exception as e:
                    print ("******"+repr(e)+"******")
                    traceback.print_exc();
                    print (str_i_filename)
