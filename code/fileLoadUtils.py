import codecs

# 加载原始词典及词频词典
def loadDictAsMap(filename):
    dict={}
    i=0
    f=codecs.open(filename,'r','utf-8')
    for line in f.readlines():
        info=line.strip().split(' ')
        dict[info[0]] = [(int)(info[1]), (int)(info[1])]

    print("LOAD DICT SUCCESSFULLY")
    return dict

# 加载IDF词典 格式 {词:[词频,出现文章数,IDF值]} 输出{词:IDF值}
def loadIdfDictAsMap(filename):
    dict={}
    f = codecs.open(filename, 'r', 'utf-8')
    for line in f.readlines():
        info = line.strip().split(' ')
        dict[info[0]]=(float)(info[3])
    print ("LOAD IDF DICT SUCCESSFULLY")
    return dict

def loadFullIdfDictAsMap(filename):
    dict={}
    f = codecs.open(filename, 'r', 'utf-8')
    for line in f.readlines():
        info = line.strip().split(' ')
        dict[info[0]]=[(int)(info[1]),(int)(info[2]),(float)(info[3])]
    print ("LOAD IDF DICT SUCCESSFULLY")
    return dict

# 按行加载数据 输出List
def loadData(filename):
    data=[]
    f = codecs.open(filename, 'r', 'utf-8')
    for line in f.readlines():
        data.append(line)

    print ("LOAD DATA AS LIST SUCCESSFULLY")
    return data


