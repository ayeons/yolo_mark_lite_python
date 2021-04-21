from cv2 import cv2
import numpy as np
import os
from absl import app, flags
import copy
import mark_object as ob
import config as cfg
import glob

flags.DEFINE_string('images_path','./data/images','image directory path')
flags.DEFINE_string('output_path','./data/train.txt','output data path')

clicked=False
sx=-1
sy=-1
th=-1

mode='draw'
control=False
marks=[]
font=cv2.FONT_HERSHEY_COMPLEX
font_size=0.5

def drawRect(e,x,y,flag,param):
    
    global clicked,sx,sy,th,mode
    if e==cv2.EVENT_LBUTTONDOWN:
        clicked=True
        sx,sy=x,y
        param.add([-1,-1,-1,-1,-1],copy.deepcopy(param.getImage()))
        
        
    elif e==cv2.EVENT_MOUSEMOVE:
        if clicked==True:
            
            cv2.rectangle(param.getImage(),(sx,sy),(x,y),cfg.BOX_COLOR,-1)
            cv2.addWeighted(param.getImage(),0.5,param.getPrevImage(),0.5,0,param.getImage())
            
    elif e==cv2.EVENT_LBUTTONUP:
        img=param.getImage()
        clicked=False
        w=abs(sx-x)
        th=abs(sy-y)
        sx=min(sx,x)
        sy=min(sy,y)
        
        x_center=(sx+(w/2))/len(img[0])
        y_center=(sy+(th/2))/len(img)
        pos=[x_center,y_center,w/len(img[0]),th/len(img)]
        param.setPosition(pos)
        mode='type'

    # elif flag & cv2.EVENT_FLAG_CTRLKEY:
    #     pass

def makeMark(path):
    img=cv2.imread(path)
    mark=ob.Mark(path,img)
    txt_path=path[:path.rfind('.')]+'.txt'
    if os.path.isfile(txt_path):
        f=open(txt_path)
        boxes=f.readlines()
        for i in boxes:
            timg=copy.deepcopy(mark.getImage())
            n,x,y,w,h=i.split(' ')
            x=float(x)
            y=float(y)
            w=float(w)
            h=float(h)
            rx=int(x*len(timg[0]))
            ry=int(y*len(timg))
            rw=int(w*len(timg[0]))
            rh=int(h*len(timg))
            x_start=rx-(rw//2)
            y_start=ry-(rh//2)
            dy=y_start
            marker=cv2.MARKER_TRIANGLE_DOWN
            if y_start<=10:
                dy=y_start+rh+10
                marker=cv2.MARKER_TRIANGLE_UP
            cv2.rectangle(timg,(x_start,y_start),(x_start+rw,y_start+rh),cfg.BOX_COLOR,-1)
            cv2.addWeighted(timg,0.5,mark.getImage(),0.5,0,timg)
            cv2.drawMarker(timg,(x_start+5,dy-5),cfg.MARKER_COLOR,marker,8)
            cv2.putText(timg,n,(x_start+10,dy),font,font_size,cfg.CLS_NUM_COLOR)
            mark.add([n,x,y,w,h],timg)
    return mark        

def saveData():
    for i in marks:
        path=i.getPath()
        txt_path=path[:path.rfind('.')]+'.txt'
        if i.getLenDatas()<=0:
            
            if os.path.isfile(txt_path):
                os.remove(txt_path)
        else:
            f=open(txt_path,'w')
            f.write(i.makeText())
            f.close()

def main(v):
    global mode,key_draw,key_type,key_draw,key_type,sx,sy,th,marks
    dir_path=flags.FLAGS.images_path+'/'
    
    directory=[i for i in os.listdir(dir_path) if not i.endswith('txt')]
    
    if len(directory)<=0:
        raise SystemError('dir empty')
    cache_num=cfg.CACHE_NUM
    if cache_num<10:
        cache_num=10
    if cache_num>len(directory):
        cache_num=len(directory)
    marks=[makeMark(dir_path+directory[i]) for i in range(cache_num)]
    index=0
    
    key_draw=[[0 for i in range(400)] for i in range(300)]
    key_type=[[0 for i in range(400)] for i in range(300)]
    key_draw=np.uint8(key_draw)
    key_type=np.uint8(key_type)

    cv2.namedWindow('image')
    cv2.moveWindow('image',710,150)
    cv2.namedWindow('key')
    cv2.moveWindow('key',300,150)
    cv2.putText(key_draw,'Draw boxes',(10,30),cv2.FONT_HERSHEY_TRIPLEX,1,200,2)
    cv2.putText(key_draw,'mouse_drag : draw_box',(10,70),cv2.FONT_HERSHEY_TRIPLEX,0.8,150,2)
    cv2.putText(key_draw,f'{cfg.PREV} : prev',(10,100),cv2.FONT_HERSHEY_TRIPLEX,0.8,150,2)
    cv2.putText(key_draw,f'{cfg.NEXT} : next',(10,130),cv2.FONT_HERSHEY_TRIPLEX,0.8,150,2)
    cv2.putText(key_draw,f'{cfg.REMOVE} : remove',(10,160),cv2.FONT_HERSHEY_TRIPLEX,0.8,150,2)
    cv2.putText(key_draw,'enter : write and exit',(10,190),cv2.FONT_HERSHEY_TRIPLEX,0.8,150,2)
    cv2.putText(key_draw,'esc : exit',(10,220),cv2.FONT_HERSHEY_TRIPLEX,0.8,150,2)
    
    cv2.putText(key_type,'Type class_num',(10,30),cv2.FONT_HERSHEY_TRIPLEX,1,200,2)
    cv2.putText(key_type,'number : class_num',(10,70),cv2.FONT_HERSHEY_TRIPLEX,0.8,150,2)
    cv2.putText(key_type,'back_space : delete num',(10,100),cv2.FONT_HERSHEY_TRIPLEX,0.8,150,2)
    cv2.putText(key_type,f'{cfg.SAVE} : save',(10,130),cv2.FONT_HERSHEY_TRIPLEX,0.8,150,2)
    cv2.putText(key_type,f'{cfg.REMOVE} : remove',(10,160),cv2.FONT_HERSHEY_TRIPLEX,0.8,150,2)
    cv2.putText(key_type,'esc : exit',(10,190),cv2.FONT_HERSHEY_TRIPLEX,0.8,150,2)
    
    mark=marks[index%cache_num]
    cv2.setMouseCallback('image',drawRect,mark)
    while(1):
        if mode=='draw':
            cv2.imshow('key',key_draw)
            while(mode=='draw'):
                mark=marks[index%cache_num]
                cv2.setMouseCallback('image',drawRect,mark)
                new_title=mark.getPath()
                cv2.setWindowTitle('image',new_title)
                cv2.imshow('image',mark.getImage())
                key=cv2.waitKey(1)
                if key>=0:
                    if key==27:
                        raise SystemExit()
                    elif cfg.REMOVE.__contains__(chr(key)):
                        
                        if mark.getLenDatas()>0:
                            mark.remove()
                                
                    elif key == 13:
                        raise ob.SaveAndExit()
                    elif cfg.PREV.__contains__(chr(key)):
                        
                        if index%cache_num!=0 or cache_num>=len(directory):
                            index-=1
                        else:
                            if index<=0:
                                index=len(directory)-1
                            elif index%cache_num==0:
                                index-=1
                            marks=[makeMark(dir_path+directory[i]) for i in range(index-(index%cache_num),index+1)]
                            
                            
                    elif cfg.NEXT.__contains__(chr(key)):
                        if cache_num>=len(directory):
                            index+=1
                        else:
                            if index>=len(directory)-1:
                                index=0
                                if index+cache_num>len(directory):
                                    saveData()
                                    marks=[makeMark(dir_path+directory[i]) for i in range(index,len(directory))]
                                else:
                                    saveData()    
                                    marks=[makeMark(dir_path+directory[i]) for i in range(index,index+cache_num)]
                            elif index%cache_num==cache_num-1:
                                index+=1
                                if index+cache_num>len(directory):
                                    saveData()
                                    marks=[makeMark(dir_path+directory[i]) for i in range(index,len(directory))]
                                else:    
                                    saveData()
                                    marks=[makeMark(dir_path+directory[i]) for i in range(index,index+cache_num)]
                            else:
                                index+=1
                

        elif mode=='type':
            cv2.imshow('key',key_type)
            keys=''
            
            cv2.setMouseCallback('image',lambda e,x,y,f,p:None)
            
            temp=copy.deepcopy(mark.getImage())
            px=sx
            py=sy
            marker=cv2.MARKER_TRIANGLE_DOWN
            if py<=10:
                py=py+th+10
                marker=cv2.MARKER_TRIANGLE_UP
            cv2.drawMarker(temp,(px+5,py-5),cfg.MARKER_COLOR,marker,8)
            
            cv2.putText(temp,'type class_num',(px+10,py),font,font_size,cfg.CLS_NUM_COLOR)
            cv2.imshow('image',temp)

            while(mode=='type'):
                
                key=cv2.waitKey(0)
                if key>=0:
                    if 48<=key<58:
                        temp=copy.deepcopy(mark.getImage())
                        keys+=chr(key)
                        
                        cv2.drawMarker(temp,(px+5,py-5),cfg.MARKER_COLOR,marker,8)
                        cv2.putText(temp,keys,(px+10,py),font,font_size,cfg.CLS_NUM_COLOR)
                        cv2.imshow('image',temp)
                    elif key==8:
                        if len(keys)>0:
                            temp=copy.deepcopy(mark.getImage())
                            keys=keys[:-1]
                            cv2.drawMarker(temp,(px+5,py-5),cfg.MARKER_COLOR,marker,8)
                            cv2.putText(temp,keys,(px+10,py),font,font_size,cfg.CLS_NUM_COLOR)
                            cv2.imshow('image',temp)
                    elif cfg.SAVE.__contains__(chr(key)):
                        if not keys=='':
                            cv2.drawMarker(mark.getImage(),(px+5,py-5),cfg.MARKER_COLOR,marker,8)
                            cv2.putText(mark.getImage(),keys,(px+10,py),font,font_size,cfg.CLS_NUM_COLOR)
                            mark.setClassNum(keys)
                            mode='draw'
                        else:
                            print('type class_num')
                    elif cfg.REMOVE.__contains__(chr(key)):
                        if mark.getLenDatas()>0:
                            mark.remove()
                            mode='draw'
                                
                    elif key==27:
                        raise SystemExit()

    
    
if __name__=='__main__':
    try:    
        app.run(main)
    except SystemExit as e:
        print(e)
    except ob.SaveAndExit:
        saveData()

# 'C:/users/user/desktop/plants/'
