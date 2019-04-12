import code.fileWriteUtils as fo
import code.fileLoadUtils as fl
import codecs

dict=fl.loadFullIdfDictAsMap("..\\data\\idfDict.txt")
# fout=codecs.open("..\\result\\ReducedIdf.txt",'w','utf-8')

reducedDict={}
for key in dict:
    if dict[key][0]==1 and dict[key][1]==1:
        continue
    else:
        reducedDict[key]=dict[key]

fo.writeIdfDictToFile(reducedDict,"..\\result\\ReducedIdf.txt")



