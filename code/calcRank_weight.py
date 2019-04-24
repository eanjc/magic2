import codecs
import json

train_name="coreEntityEmotion_train.txt"
res_name="entityOutPut_originCut-pyltp_full_v3_datacache.txt"

output_name="rankweight_v2.txt"
keywords_perNews=20
list_train=codecs.open(train_name,'r','utf-8').readlines()
list_res=fr=codecs.open(res_name,'r','utf-8').readlines()
fout=codecs.open(output_name,'w','utf-8')
step=0.05
max_top3_f1=0
top3_f1_rank=[]
max_top2_f1=0
top2_f1_rank=[]

a=0
ccc=0
while a<1:
    b=0
    while b<1-a:
        c=0
        while c<1-a-b:
            d=1-a-b-c
            ccc+=1
            res_line_num=0
            f1_top3_sum=0
            f1_top2_sum=0
            for i in range(0, len(list_train) ):
                # print(i)
                news_line_raw = list_train[i]
                news_json = json.loads(news_line_raw)
                entity = set()
                newsId = news_json["newsId"]
                eec = news_json["coreEntityEmotions"]
                for key in eec:
                    entity.add(key["entity"])
                keywords_scoreDict = {}
                for p in range(keywords_perNews):
                    data_line = list_res[res_line_num].strip()
                    res_line_num+=1
                    data_info = data_line.split(" ")
                    keywords_scoreDict[data_info[0]] = a* float(data_info[1]) + b * float(data_info[2]) + c* float(data_info[3]) + d* float(data_info[4])
                sortedScore = sorted(keywords_scoreDict.items(), key=lambda x: x[1], reverse=True)

                # top3
                tp_top3 = 0
                fp_top3 = 0
                fn_top3 = 0
                res_top3 = set()
                res_top3.add(sortedScore[0][0])
                res_top3.add(sortedScore[1][0])
                res_top3.add(sortedScore[2][0])
                for w in res_top3:
                    if w in entity:
                        tp_top3 += 1
                    else:
                        fp_top3 += 1
                for e in entity:
                    if e not in res_top3:
                        fn_top3 += 1
                p_top3 = float(tp_top3) / float(tp_top3 + fp_top3)
                r_top3 = float(tp_top3) / float(tp_top3 + fn_top3)
                if p_top3 != 0 or r_top3 != 0:
                    f1_top3_sum = f1_top3_sum + (2 * p_top3 * r_top3) / float(p_top3 + r_top3)

                # top2
                tp_top2 = 0
                fp_top2 = 0
                fn_top2 = 0
                res_top2 = set()
                res_top2.add(sortedScore[0][0])
                res_top2.add(sortedScore[1][0])
                for w in res_top2:
                    if w in entity:
                        tp_top2 += 1
                    else:
                        fp_top2 += 1
                for e in entity:
                    if e not in res_top2:
                        fn_top2 += 1
                p_top2 = float(tp_top2) / float(tp_top2 + fp_top2)
                r_top2 = float(tp_top2) / float(tp_top2 + fn_top2)
                if p_top2 != 0 or r_top2 != 0:
                    f1_top2_sum = f1_top2_sum + (2 * p_top2 * r_top2) / float(p_top2 + r_top2)

            f1_top3 = f1_top3_sum / len(list_train)
            f1_top2 = f1_top2_sum / len(list_train)

            if f1_top3>max_top3_f1:
                max_top3_f1=f1_top3
                top3_f1_rank=[a,b,c,d]
            if f1_top2>max_top2_f1:
                max_top2_f1=f1_top2
                top2_f1_rank=[a,b,c,d]
            outputline=str(a)+"\t"+str(b)+"\t"+str(c)+"\t"+str(d)+"\t"+str(f1_top3)+"\t"+str(f1_top2)+"\n"
            fout.write(outputline)
            if ccc%10==0:
                print (ccc)
                fout.flush()
                print(outputline)

            c=c+step
        b=b+step
    a=a+step

