import json,re
from HanziReplacer import *

errorlist=[]
def open_file_b(path)->bytes:
    return open(path,'rb').read()

def from_bytes(b:bytes)->int:
    return int.from_bytes(b, byteorder='little', signed=False)

def save_file_b(path,data)->None:
    with open(path,'wb') as f:
        f.write(data)

def save_json(path:str,data)->None:
    with open(path,'w',encoding='utf8') as f:
        json.dump(data,f,ensure_ascii=False,indent=4)

def open_json(path:str):
    f = open(path,'r',encoding='utf8')
    return json.load(f)

def to_bytes(num:int,length:int)->bytes:
    return num.to_bytes(length,byteorder='little')

class txtfile(object):
    def __init__(self,data) -> None:
        self.data=data
        self.content=data.split(b'\x0d\x0a')
        self.decode()
        
    def decode(self):
        self.lines=[]
        for l in self.content:
            self.lines.append(line(l))
            
    
    def trans(self,transdict:dict,hanzireplacer:HanziReplacer):
        self.content=[line.create_ZHUSHI_line().to_bytes()]*30
        l=line.create_empty_msg()
        for new_l in self.lines:
            if new_l.type=='msg':
                l.add(new_l)
            else:
                if l.content!=b'':
                    l.trans(transdict,hanzireplacer)
                    self.content.append(l.to_bytes())
                    l=line.create_empty_msg()
                self.content.append(new_l.to_bytes())
        if l.content!=b'':
            l.trans(transdict,hanzireplacer)
            self.content.append(l.content)
            

    def save(self,path):
        self.data=b'\x0d\x0a'.join(self.content)
        save_file_b(path,self.data)

class line(object):
    def __init__(self,b:bytes) -> None:
            self.content=b
            self.text=''
            self.classify()
            self.get_plain_text()
            
    
    def classify(self):
        try:
            texts=self.content.decode(encoding='sjis')
        except:
            self.type='bytes'
            return
        if texts=='':
            self.type='n'
        elif texts[0]=='【':
            self.type='name'
            self.text=texts
        elif re.match(r'[;$]',texts):
            self.type='other'
        else:
            self.type='msg'
            self.text=texts
    
    def trans(self,transdict:dict,hanzireplacer:HanziReplacer):
        if self.type=='msg':
            try:
                trans=transdict[self.text]
                self.content=hanzireplacer.hanzitihuan(trans).encode(encoding='sjis')
            except KeyError:
                global errorlist
                errorlist.append(self.text)

    def to_bytes(self):
        return self.content
       
    
    def get_plain_text(self):
        zhuyin=re.compile(r'_t!(.*?),(.*?),(.*?),(.*?)/')
        if self.type=='msg':
            self.content=re.sub(zhuyin,'',self.content.decode(encoding='sjis')).encode(encoding='sjis')
    
    def add(self,another_line):
        if self.type==another_line.type:
            self.content=self.content+another_line.content
            texts=self.content.decode(encoding='sjis')
            self.text=texts
        else:
            raise TypeError()
    
    def create_empty_msg():
        _=line(b'')
        _.type='msg'
        return _
    
    def create_ZHUSHI_line():
        _=line(';--------------------------------------------'.encode(encoding='sjis'))
        _.type='other'
        return _
