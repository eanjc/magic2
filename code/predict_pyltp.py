import codecs
import json
import jieba
import jieba.analyse
import math
import pyltp
import os
from pyltp import Segmentor
import data.TextRank

# 定义映射函数
def sigmoid(x):
    x=float(x)
    y = 1 / (1 + math.exp((-x)))
    return y

# 加载并设置pyltp
LTP_DATA_DIR='D:\Souhu\ltp_data_v3.4.0\ltp_data_v3.4.0'
cws_model_path=os.path.join(LTP_DATA_DIR,'cws.model')
segmentor=Segmentor()
# segmentor.load(cws_model_path)
segmentor.load_with_lexicon(cws_model_path, 'ExDictForCut_without_JiebaDefault.txt')

# 评价分数的比例
rank={'tfidf':0.4,'tr':0.25,'it':0.2,'pos':0.15}

# 加载用户词典
# jieba.load_userdict("ReducedDict_test3.txt")

# 名词性词性加分列表
sp=(set) (['an','Ng','n','nr','ns','nt','nz','vn','j'])
kickout=(set)(['.','。','，','-','+',':','：','“','/','*','—','…'])

# 加载IDF数据字典
def loadIdfDictAsMap(filename):
    dict={}
    f = codecs.open(filename, 'r', 'utf-8')
    for line in f.readlines():
        info = line.strip().split(' ')
        dict[info[0]]=(float)(info[3])
    print ("LOAD IDF DICT SUCCESSFULLY")
    return dict

idfDict= loadIdfDictAsMap("ReducedIdfDict_test1.txt")

# 加载词性词典
def loadWordsPartOfSpeech(filename):
    dict={}
    f=codecs.open(filename, 'r', 'utf-8')
    for line in f.readlines():
        info=line.strip().split(" ")
        dict[info[0]]=info[2]
    return dict

# 加载实体预训练词典
def loadPreTrainEntityDict(filename):
    dic={}
    f=codecs.open(filename, 'r', 'utf-8')
    for line in f.readlines():
        info=line.strip().split(",")
        dic[info[0]]=int(info[1])
    return dic

# 加载pyltp中的ner名词
def loadNerDictFromPyltp(filename):
    dic={}
    f=codecs.open(filename, 'r', 'utf-8')
    for line in f.readlines():
        info=line.strip().split(" ")
        if len(info)<3:
            continue
        if len(info[0])>1 and info[2]=='is_ner':
            dic[info[0]]=info[1]
    return dic

nerInPyltp=  loadNerDictFromPyltp('pyltp_savebox.txt')

partOfSpeechDict=loadWordsPartOfSpeech("spdict.txt")
nerDict=loadPreTrainEntityDict('lexiconAndNerDictWithInfo.txt')



# 打开训练数据集
f=codecs.open("coreEntityEmotion_test_stage1.txt",'r','utf-8')

# 设置输出文件
fout=codecs.open("predict_test3_pyltp_v3_3.txt",'w','utf-8')

#加载TextRank
trDemo = data.TextRank.TextRank()

# 分析过程
print ('Start Calculating Score.')
i = 0
for rawline in f.readlines():
    # 按行分析
    rawline_json=json.loads(rawline)
    # 获取标题行
    titleline=rawline_json['title']
    # 获取标题分词
    titleWords=segmentor.segment(titleline)
    # 创建标题集合（不重集合）
    titleWordsSet = (set)([])
    # 标题行输出
    # titleCut = "TitleCut="
    for w in titleWords:
        flag=0
        for sep in kickout:
            if sep in w:
                flag=1
        if flag==1:
            continue
        # 读入长度大于1的词
        if len((str)(w))>1:
            titleWordsSet.add(w)
            # titleCut+=w+" "
    # 获取内容行
    SC=rawline_json["content"].strip()
    content=rawline_json["title"].strip()+' '+rawline_json["content"].strip()
    content=content.replace("\r\n"," ")
    content = content.replace("\n", " ")
    # 创建内容行词典
    lineWordsDic = {}
    # 分词
    words = segmentor.segment(content)
    wordsForTR = list(words)
    # 总词数
    wordNum = 0
    # 创建内容分词输出行
    # contentCut = "Content = "
    # 统计词频 TF
    for w in words:
        flag=0
        for sep in kickout:
            if sep in w:
                flag=1
        if flag==1:
            continue
        if len(w)<=1:
            continue
        # contentCut=contentCut+w+" "
        if w in lineWordsDic:
            lineWordsDic[w]+=1
        else:
            lineWordsDic[w]=1
        wordNum+=1
    # 创建TFIDF词典
    tfidf = {}
    # TFIDF 评分
    for w in lineWordsDic:
        if (w  in idfDict):
            idf = idfDict[w]*(1+sigmoid(idfDict[w]-6))
        else:
            idfDict[w]=idf =1
            if len(w)>3:
                idfDict[w] = idf = 6
        tfidf[w]=(lineWordsDic[w]/wordNum)*idf  #MJ：wordNum不用除吧，每个词同除一个整数？idf下次来看看你怎么统计的。P
    # TextRank评分
    textRank = trDemo.standardScoreTextrank(wordsForTR)    # 创建TR评分词典
    trDict = {}
    for l in textRank:
        trDict[l[0]]=l[1]
    # 排序TFIDF评分
    sortTfidf=sorted(tfidf.items(), key = lambda x:x[1],reverse=True)
    sortTfidf=(list)(sortTfidf)
    # TFIDF分数归一化
    maxTfidf=sortTfidf[0][1]
    mutil=1/maxTfidf
    standardTfidf={}
    for key in tfidf:
        standardTfidf[key]=tfidf[key]*mutil
    # 创建InTitleLine词典
    itlDict={}
    # 创建词性词典
    posDict={}
    # 创建总分词典
    totalScore = {}
    # 评分并记录
    # 附加判断
    addition=0
    for k in tfidf:
        partOfSpeechRank = 0
        inTitleRank = 0
        if k not in trDict:
            trDict[k]=0
            tr=0
            if standardTfidf[k]>0.4:
                tr=trDict[k]=standardTfidf[k]/4
        else:
            tr=trDict[k]
        # if k in titleWordsSet:  #MJ：不是词在title的cut_all出现了，而是title的词被content的词包含。比如title的"数据","时代","数据时代"可以给content里的"数据时代","大数据"分别加3次，1次权重。另外，我的一个想法是，加的时候,同时可以乘上一个idf值。稀有的次出现在title理应比常见词出现在title中贡献大。
        #     itlDict[k]=1
        #     inTitleRank=1
        # else:
        #     itlDict[k] = 0
        for w in titleWordsSet:
            if w in k:
                if w not in idfDict:
                    idfDict[w]=1
                inTitleRank+=1+idfDict[w]*1.2
        inTitleRank=math.tanh(0.15*inTitleRank)
        itlDict[k]=inTitleRank
        if k in nerDict:
            tp=nerDict[k]
            if tp==3:
                partOfSpeechRank=posDict[k]=0.9
            if tp==2:
                partOfSpeechRank = posDict[k] = 0.5
            if tp==1:
                partOfSpeechRank = posDict[k] = 0.7
        else:
            if k in partOfSpeechDict and partOfSpeechDict[k] in sp:
                partOfSpeechRank = posDict[k] = 0.35
            else:
                partOfSpeechRank = posDict[k] = 0
        if k in nerInPyltp:
                if partOfSpeechRank+0.25>1:
                    partOfSpeechRank= posDict[k]=1
                else:
                    partOfSpeechRank += 0.25
                    posDict[k]=partOfSpeechRank

        totalScore[k] = rank['tfidf'] * standardTfidf[k] + rank['tr']  * tr + rank['it']  * inTitleRank + rank['pos']  * partOfSpeechRank
    # 对总分排序
    sortedScore = sorted(totalScore.items(), key=lambda x: x[1], reverse=True)
    entityNum=len(list(sortedScore))

    # 整理获取输出信息
    i=i+1
    # 输出编号信息
    # outPutLine="No= "+(str)(i)+"\t" +"NewsId= "+rawline_json["newsId"]+"\tTotalWordsNum= "+(str)(wordNum)+"\n"
    # # 输出可能的实体信息
    # sz=20
    # if wordNum<sz:
    #     sz=wordNum
    # for p in range(sz):
    #     key=sortedScore[p][0]
    #     wl="("+(str)(sortedScore[p][0])+" TotalScore= " +(str)(sortedScore[p][1])+" TfidfScore= "+(str)(standardTfidf[key])+" TextRankScore= "+(str)(trDict[key])+" InTitleScore= "+(str)(itlDict[key])+" PartOFSPeechScore= "+(str)(posDict[key])+")\t"
    #     outPutLine+=wl
    # outPutLine+="\n"
    # # 输出标题行
    # outPutLine+="title = "+titleline+"\t"
    # # 输出标题分词
    # outPutLine+="titlecut= "+titleCut+"\n"
    # # 输出原文分词
    # outPutLine+=contentCut+"\n"
    # # 输出原文      #MJ：原文和分词最好对调一下，分词处于承上启下的位置。P
    # outPutLine+=SC+"\n"
    if entityNum<3:
        outPutLine = rawline_json["newsId"] + "\t"
        for pp in range(entityNum):
            outPutLine+=(str)(sortedScore[pp][0])
            if pp<entityNum-1:
                outPutLine += ","
        outPutLine+="\t"
        for pp in range(entityNum):
            outPutLine+="POS"
            if pp<entityNum-1:
                outPutLine += ","
        outPutLine+="\n"
    else:
        outPutLine=rawline_json["newsId"]+"\t"+(str)(sortedScore[0][0])+","+(str)(sortedScore[1][0])+","+(str)(sortedScore[2][0])+"\tPOS,POS,POS\n"


    # 监视
    print(i)
    # 输出到文件
    fout.write(outPutLine)
    fout.flush()





