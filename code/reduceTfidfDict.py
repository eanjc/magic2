import codecs
def loadDictAsMap(filename):
    dict={}
    f=codecs.open(filename,'r','utf-8')
    i=0
    for line in f.readlines():
        info=line.strip().split(' ')
        if len(info)<4:
            continue
        if (len(info[0])>1):
            dict[info[0]] = [(int)(info[1]), (int)(info[2]),(float)(info[3])]
        # dict[info[0]]=[(int)(info[1]),(int)(info[1])]
        i=i+1
        if i%100==0:
            print (i)
    return dict

def dictReduce(dict):
    reducedDict={}
    for key in dict:
        if dict[key]==[1,1,1]:
            continue
        else:
            reducedDict[key]=dict[key]
    return reducedDict

dict=loadDictAsMap("idfValueAfterStatisticExData.txt")
reducedDict=dictReduce(dict)
fout=codecs.open("ReducedIdfDict_test1.txt",'w','utf-8')
for key in reducedDict:
    line=key+" "+(str)(reducedDict[key][0])+" "+(str)(reducedDict[key][1])+" "+(str)(reducedDict[key][2])+"\n"
    fout.write(line)
    fout.flush()