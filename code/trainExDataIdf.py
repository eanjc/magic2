import code.fileWriteUtils as fo
import code.fileLoadUtils as fl
import jieba
import codecs

dict=fl.loadDictAsMap("..\\data\\dict.txt")
jieba.load_userdict("..\\data\\dict.txt")

def wordsCut(news):
    title=news["title"]
    content=news["content"]
    content=content.replace('\n',' ')
    content=content.replace('\r\n', ' ')
    words=jieba.cut(title+'\t'+content)
    return list(words)

textNum=0;
print("load dict successfully")
for filename in os.listdir(".\\data\\data_hdfs"):
    f=codecs.open("..\\data\\data_hdfs\\"+filename,"r","utf-8")
    for line in f.readlines():
        textNum+=1
        content=line.strip().split('\t')
        wordsFlag=set([])
        fullSentence=""
        for i in range(9,len(content)-5):
            sentence = content[i].replace(' ',"")
            sentence = sentence.replace('\n',' ')
            sentence = sentence.replace('\r\n', ' ')
            sentence = sentence.replace('\t', " ")
            fullSentence=fullSentence+sentence
        words = jieba.cut(fullSentence)
        for w in words:
            if (w in dict):
                dict[w][0]+=1
            else:
                dict[w]=[1,0]
            if(w not in wordsFlag):
                dict[w][1]+=1
            wordsFlag.add(w)

    print (filename)
print(textNum)

fout=codecs.open("..\\result\\tfAfterStatisticExData.txt",'w','utf-8')
for key in dict:
    line=key+" "+(str)(dict[key][0])+" "+(str)(dict[key][1])+"\n"
    fout.write(line)
    fout.flush()