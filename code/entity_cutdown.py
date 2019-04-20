import codecs

filename="predict_test3_pyltp_v3_3.txt"
outname=filename.strip().split(".")[0]+"_cutdownTo2Entities.txt"
f=codecs.open(filename,'r','utf-8')
fout=codecs.open(outname,'w','utf-8')

for line in f.readlines():
    info=line.strip().split("\t")
    outline=info[0]+"\t"
    entity=info[1].split(",")
    outline+=entity[0]+","+entity[1]+"\t"
    pos=info[2].strip().split(",")
    outline+=pos[0]+","+pos[1]+"\n"
    fout.write(outline)
    fout.flush()