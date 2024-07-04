import os,json
from Lib import *
from HanziReplacer import *

ori_text_path='ori_text\\'
trans_text_path='trans_json\\'
out_text_path='pack\p\\'
filelist=os.listdir(trans_text_path)

hanzireplacer=HanziReplacer()
transdict={}

print('reading trans……')
for f in filelist:
    f=open_json(trans_text_path+f)
    for dic in f:
        if '|' in dic['pre_jp'] and len(dic['pre_jp'].split('|'))==2:
            transdict[dic['pre_jp'].split('|')[0]]=dic["post_zh_preview"].split('|')[0]
            transdict[dic['pre_jp'].split('|')[1]]=dic["post_zh_preview"].split('|')[1]
        transdict[dic['pre_jp']]=dic["post_zh_preview"]

hanzireplacer.ReadTransAndGetHanzidict(replacement_dicts=[transdict])
print('creating font……')
hanzireplacer.ChangeFont('3rdEye_02_font.ttf','3rdEye_02_font.ttf','pack\\3rdEye_02_font.ttf')

i=0
l=len(filelist)
print('replacing text……')
for f in filelist:
    i+=1
    print(f'{i}\{l}',end='\r')
    f=f.replace('.json','')
    ori_f=open_file_b(ori_text_path+f+'.txt')
    ori_f=txtfile(ori_f)
    ori_f.trans(transdict,hanzireplacer)
    ori_f.save(out_text_path+f+'.txt')


out=[]
for i in errorlist:
    out.append({'message':i})
save_json('errorlist.json',out)