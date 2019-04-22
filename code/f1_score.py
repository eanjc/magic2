import codecs
import json

rank_weight={"tfidf":0.3,"tr":0.2,"intl":0.3,"pos":0.2}
newsNum=100
keywords_perNews=10
train_name="coreEntityEmotion_train.txt"
res_name="entityOutPut_originCut-pyltp_10001_datacache.txt"
ft=codecs.open(train_name,'r','utf-8')
fr=codecs.open(res_name,'r','utf-8')

f1_top3_sum=0
f1_top2_sum=0

for i in range(1,newsNum+1):
    print(i)
    news_line_raw=ft.readline()
    news_json=json.loads(news_line_raw)
    entity=set()
    newsId=news_json["newsId"]
    eec=news_json["coreEntityEmotions"]
    for key in eec:
        entity.add(key["entity"])
    keywords_scoreDict = {}
    for p in range(keywords_perNews):
        data_line=fr.readline().strip()
        data_info=data_line.split(" ")
        keywords_scoreDict[data_info[0]]=rank_weight["tfidf"]*float(data_info[1])+rank_weight["tr"]*float(data_info[2])+rank_weight["intl"]*float(data_info[3])+rank_weight["pos"]*float(data_info[4])
    sortedScore=sorted(keywords_scoreDict.items(), key = lambda x:x[1],reverse=True)

    # top3
    tp_top3=0
    fp_top3=0
    fn_top3=0
    res_top3=set()
    res_top3.add(sortedScore[0][0])
    res_top3.add(sortedScore[1][0])
    res_top3.add(sortedScore[2][0])
    for w in res_top3:
        if w in entity:
            tp_top3+=1
        else:
            fp_top3+=1
    for e in entity:
        if e not in res_top3:
            fn_top3+=1
    p_top3=float(tp_top3)/float(tp_top3+fp_top3)
    r_top3=float(tp_top3)/float(tp_top3+fn_top3)
    if p_top3!=0 or r_top3!=0:
        f1_top3_sum=f1_top3_sum+(2*p_top3*r_top3)/float(p_top3+r_top3)



    # top2
    tp_top2=0
    fp_top2=0
    fn_top2=0
    res_top2=set()
    res_top2.add(sortedScore[0][0])
    res_top2.add(sortedScore[1][0])
    for w in res_top2:
        if w in entity:
            tp_top2+=1
        else:
            fp_top2+=1
    for e in entity:
        if e not in res_top2:
            fn_top2+=1
    p_top2=float(tp_top2)/float(tp_top2+fp_top2)
    r_top2=float(tp_top2)/float(tp_top2+fn_top2)
    if p_top2!=0 or r_top2!=0:
        f1_top2_sum=f1_top2_sum+(2*p_top2*r_top2)/float(p_top2+r_top2)


f1_top3=f1_top3_sum/newsNum
f1_top2=f1_top2_sum/newsNum

print("******************************result******************************")
print("f1_top3= %f"%f1_top3)
print("f1_top2= %f"%f1_top2)




