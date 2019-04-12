import jieba
import code.fileLoadUtils as fl
import code.fileWriteUtils as fo
import codecs
import json

# 对training训练集进行分词
jieba.load_userdict("..\\data\\dict.txt")

trainingFile="..\\data\\coreEntityEmotion_train.txt"

rawdata=fl.loadData(trainingFile)

def standardTrainingData(raw):
    data=[]
    for line in raw:
        news=json.loads(line.strip())
        data.append(news)
    return data

def wordsCut(news):
    title=news["title"]
    content=news["content"]
    content=content.replace('\n',' ')
    content=content.replace('\r\n', ' ')
    words=jieba.cut(title+'\t'+content)

    return list(words)

def getNewsId(news):
    id=news["newsId"]
    return id

def progress(data):
    result=[]
    for news in data:
        id=getNewsId(news)
        words=wordsCut(news)
        content=""
        outline=""
        for w in words:
            content=content+w+" "
            content=content.replace('\n','')
        outline=(str)(id)+'\t'+content+'\n'
        result.append(outline)
    return result

data=standardTrainingData(rawdata)
result=progress(data)

fo.writeDataToFile(data,"..\\result\\wordCutResult.txt")
