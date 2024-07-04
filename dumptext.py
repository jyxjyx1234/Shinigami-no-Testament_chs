import os,json
from Lib import *
from HanziReplacer import *

ori_text_path='ori_text\\'
out_path='ori_text_json\\'
filelist=os.listdir(ori_text_path)

for file in filelist:
    path=ori_text_path+file
    f=open_file_b(path)
    f=txtfile(f)
    out=[]
    dic={}
    for l in f.lines:
        if l.type=='name':
            dic['name']=l.content
        if l.type=='msg':
            dic['message']=dic.get('message','')+l.content
        if l.type=='n' and 'message' in dic:
            out.append(dic.copy())
            dic={}
    save_json(out_path+file.replace('TXT','json'),out)
