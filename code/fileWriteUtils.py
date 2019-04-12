import codecs

# {词:[词频,出现文章数,IDF值]}
def writeIdfDictToFile(dict,filename):
    fout=codecs.open(filename,'w','utf-8')
    for key in dict:
        line = (str)(key) + " " + (str)(dict[key][0]) + " " + (str)(dict[key][1]) + " " + (str)(dict[key][2]) + "\n"
        fout.write(line)
        fout.flush()
    print ("WRITE DICT TO FILE SUCCESSFULLY")
    return

def writeDataToFile(data,filename):
    fout = codecs.open(filename, 'w', 'utf-8')
    for line in data:
        fout.write(line)
        fout.flush()
    print("WRITE DATA TO FILE SUCCESSFULLY")
    return