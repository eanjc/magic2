import code.fileWriteUtils as fo
import code.fileLoadUtils as fl
import math
import codecs
toCheckDictName=""

def loadDictAsMap(filename):
    dict={}
    f=codecs.open(filename,'r','utf-8')
    i=0
    for line in f.readlines():
        info=line.strip().split(' ')
        if(len(info)<3):
            continue
        dict[info[0]] = [(int)(info[1]), (int)(info[2])]
        # dict[info[0]]=[(int)(info[1]),(int)(info[1])]
        if dict[info[0]][1]>dict[info[0]][0]:
            dict[info[0]][0]=dict[info[0]][1]
        dict[info[0]].append(math.log(N/(dict[info[0]][1]+1)))
        i=i+1
        if i%100==0 :
            print (i)
    return dict

afterCheckedDict=loadDictAsMap(toCheckDictName)