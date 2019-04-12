import code.fileWriteUtils as fo
import code.fileLoadUtils as fl
import jieba
import codecs

dict=fl.loadDictAsMap("..\\data\\dict.txt")
jieba.load_userdict("..\\data\\dict.txt")

def loadAfterCutFile(filename):
    f=codecs.open(filename,'r','utf-8')
    data=[]
    for line in f.readlines():
        data.append(line)

    return data

data=loadAfterCutFile("..\\data\\wordsCutTest2.txt")

for line in data:
    line=line.replace('\t',' ')
    words=line.strip().split(' ')
    wordsFlag = set([])
    for i in range(1,len(words)):
        w=words[i]
        if (w in dict.keys()):
            dict[w][0] += 1
        else:
            dict[w] = [1, 0]
        if (w not in wordsFlag):
            dict[w][1] += 1
        wordsFlag.add(w)

fout=codecs.open("..\\result\\tfAfterStatisticOfficalData.txt",'w','utf-8')
for key in dict:
    line=key+" "+(str)(dict[key][0])+" "+(str)(dict[key][1])+"\n"
    fout.write(line)
    fout.flush()