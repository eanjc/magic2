import codecs
import json

kickout=(set)(['.','。','，','-','+',':','：','“','/','*','—','…'])

f=codecs.open("coreEntityEmotion_train.txt",'r','utf-8')
fout=codecs.open("lexiconAndNerDictWithInfo.txt",'w','utf-8')
dic={}
# 1在训练集实体 2 在nerDict  3既在训练集实体又在nerDict
i1=0
for line in f.readlines():
    jsLine=json.loads(line)
    cee=jsLine["coreEntityEmotions"]
    for d in cee:
        if d['entity'] in dic:
            continue
        else:
            dic[d['entity']]=1
    i1+=1
    print(i1)

f=codecs.open("nerDict.txt",'r','utf-8')
i2=0
for line in f.readlines():
    line=line.strip()
    ff=0
    if len(line)<=1:
        continue
    for k in kickout:
        if k in line:
            ff=1
            break;
    if ff==1:
        continue
    if line in dic:
        dic[line]=3
    else:
        dic[line]=2
    i2+=1
    print(i2)

i3=0
for key in dic:
    outline=key+","+str(dic[key])+"\n"
    fout.write(outline)
    fout.flush()
    i3+=1
    print(i3)



