import os
import math
LTP_DATA_DIR = 'D:\Souhu\ltp_data_v3.4.0\ltp_data_v3.4.0'  # ltp模型目录的路径
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`

from pyltp import Postagger
postagger = Postagger() # 初始化实例
postagger.load(pos_model_path)  # 加载模型
# 重写TextRank算法
class TextRank(object):

    def __init__(self,span=5):
        self.span=span

    def textrank(self,wordList):
        pos=postagger.postag(wordList)
        pos=list(pos)
        sp={'j','n','nh','ni','nl','ns','nt','nz','ws'}
        nWords=[]
        for i in range(len(pos)):
            if pos[i] in sp and len(wordList[i])>1:
                nWords.append(wordList[i])
        g={}
        r=self.span
        for i in range(len(nWords)):
            w=nWords[i]
            if w not in g:
                g[w]={}
            s=e=i
            if i-r<0:
                s=0
            else:
                s=i-r
            if i+r>len(nWords)-1:
                e=len(nWords)-1
            else:
                e=i+r
            for p in range(s,e+1):
                if p==i:
                    continue
                ww=nWords[p]
                if ww not in g[w]:
                    g[w][ww]=1
                else:
                    g[w][ww]+=1
        # print (g)

        diff_limit=0.00001
        max_diff=1
        max_iter=100
        iter_times=0
        d=0.85
        ws={}
        for key in g:
            ws[key]=1-d
        while max_diff>diff_limit and iter_times<max_iter:
            iter_times+=1
            round_maxdiff=0
            for word in g:
                partScore=0
                for key in g:
                    if word in g[key]:
                        s=0
                        for sc in g[key].values():
                            s+=sc
                        partScore+=(float(g[key][word]/s)*ws[key])
                newscore=(1-d)+d*partScore
                diff=math.fabs(newscore-ws[word])
                ws[word]=newscore
                if diff>round_maxdiff:
                    round_maxdiff=diff
            if round_maxdiff<max_diff:
                max_diff=round_maxdiff
        scoreList=list(sorted(ws.items(), key = lambda x:x[1],reverse=True))
        # print (iter_times)

        return scoreList


    def standardScoreTextrank(self,wordList):
        pos=postagger.postag(wordList)
        pos=list(pos)
        sp={'j','n','nh','ni','nl','ns','nt','nz','ws'}
        nWords=[]
        for i in range(len(pos)):
            if pos[i] in sp and len(wordList[i])>1:
                nWords.append(wordList[i])
        g={}
        r=self.span
        for i in range(len(nWords)):
            w=nWords[i]
            if w not in g:
                g[w]={}
            s=e=i
            if i-r<0:
                s=0
            else:
                s=i-r
            if i+r>len(nWords)-1:
                e=len(nWords)-1
            else:
                e=i+r
            for p in range(s,e+1):
                if p==i:
                    continue
                ww=nWords[p]
                if ww not in g[w]:
                    g[w][ww]=1
                else:
                    g[w][ww]+=1
        # print (g)

        diff_limit=0.00001
        max_diff=1
        max_iter=100
        iter_times=0
        d=0.85
        ws={}
        for key in g:
            ws[key]=1-d
        while max_diff>diff_limit and iter_times<max_iter:
            iter_times+=1
            round_maxdiff=0
            for word in g:
                partScore=0
                for key in g:
                    if word in g[key]:
                        s=0
                        for sc in g[key].values():
                            s+=sc
                        partScore+=(float(g[key][word]/s)*ws[key])
                newscore=(1-d)+d*partScore
                diff=math.fabs(newscore-ws[word])
                ws[word]=newscore
                if diff>round_maxdiff:
                    round_maxdiff=diff
            if round_maxdiff<max_diff:
                max_diff=round_maxdiff
        scoreList=list(sorted(ws.items(), key = lambda x:x[1],reverse=True))
        m=float(1/scoreList[0][1])

        standardScoreList=[]
        for t in scoreList:
            standardScoreList.append([t[0],m*t[1]])

        return standardScoreList













