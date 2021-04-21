from cv2 import cv2
import numpy as np
import os
from absl import app, flags
import copy
import mark_object as ob
import config as cfg

flags.DEFINE_string('images_path','./data/images','image directory path')
flags.DEFINE_string('output_path','./data/train.txt','output data path')

clicked=False
tx=-1
ty=-1
mode='draw'
control=False
train_datas={}


def drawRect(e,x,y,flag,param):
    
    global clicked,tx,ty,mode
    if e==cv2.EVENT_LBUTTONDOWN:
        clicked=True
        tx,ty=x,y
        param.add([-1,-1,-1,-1,-1],copy.deepcopy(param.getImage()))
        
        
    elif e==cv2.EVENT_MOUSEMOVE:
        if clicked==True:
            
            cv2.rectangle(param.getImage(),(tx,ty),(x,y),cfg.BOX_COLOR,-1)
            cv2.addWeighted(param.getImage(),0.5,param.getPrevImage(),0.5,0,param.getImage())
            
    elif e==cv2.EVENT_LBUTTONUP:
        
        clicked=False
        w=abs(x-tx)
        h=abs(y-ty)
        x_start=min(tx,x)
        y_start=min(ty,y)
        pos=[x_start,y_start,w,h]
        param.setPosition(pos)
        mode='type'

    # elif flag & cv2.EVENT_FLAG_CTRLKEY:
    #     pass

def main(v):
    global mode,key_draw,key_type,key_draw,key_type
    dir_path=flags.FLAGS.images_path+'/'
    
    directory=os.listdir(dir_path)
    if len(directory)<=0:
        raise SystemError('dir empty')
    cache_num=cfg.CACHE_NUM
    if cache_num<10:
        cache_num=10
    if cache_num>len(directory):
        cache_num=len(directory)
    marks=[ob.Mark(dir_path+directory[i],cv2.imread(dir_path+directory[i])) for i in range(cache_num)]
    index=0
    
    key_draw=[[0 for i in range(400)] for i in range(300)]
    key_type=[[0 for i in range(400)] for i in range(300)]
    key_draw=np.uint8(key_draw)
    key_type=np.uint8(key_type)

    cv2.namedWindow('image')
    cv2.moveWindow('image',710,150)
    cv2.namedWindow('key')
    cv2.moveWindow('key',300,150)
    cv2.setWindowTitle('key',f'marked_data_count : {len(train_datas)}')
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
                if train_datas.__contains__(mark.getPath()):
                    new_title=new_title+' : marked'
                cv2.setWindowTitle('image',new_title)
                cv2.imshow('image',mark.getImage())
                key=cv2.waitKey(1)
                if key>=0:
                    if key==27:
                        raise SystemExit()
                    elif cfg.REMOVE.__contains__(chr(key)):
                        
                        if mark.getLenDatas()>0:
                            mark.remove()
                            train_datas[mark.getPath()]=mark.makeText()
                            if mark.getLenDatas()<=0:
                                train_datas.pop(mark.getPath())
                                cv2.setWindowTitle('key',f'marked_data_count : {len(train_datas)}')
                                
                    elif key == 13:
                        raise ob.SaveData()
                    elif cfg.PREV.__contains__(chr(key)):
                        
                        if index%cache_num!=0 or cache_num>=len(directory):
                            index-=1
                        else:
                            if index<=0:
                                index=len(directory)-1
                            elif index%cache_num==0:
                                index-=1
                            marks=[ob.Mark(dir_path+directory[i],cv2.imread(dir_path+directory[i])) for i in range(index-(index%cache_num),index+1)]
                            
                            
                    elif cfg.NEXT.__contains__(chr(key)):
                        if cache_num>=len(directory):
                            index+=1
                        else:
                            if index>=len(directory)-1:
                                index=0
                                if index+cache_num>len(directory):
                                    marks=[ob.Mark(dir_path+directory[i],cv2.imread(dir_path+directory[i])) for i in range(index,len(directory))]
                                else:    
                                    marks=[ob.Mark(dir_path+directory[i],cv2.imread(dir_path+directory[i])) for i in range(index,index+cache_num)]
                            elif index%cache_num==cache_num-1:
                                index+=1
                                if index+cache_num>len(directory):
                                    marks=[ob.Mark(dir_path+directory[i],cv2.imread(dir_path+directory[i])) for i in range(index,len(directory))]
                                else:    
                                    marks=[ob.Mark(dir_path+directory[i],cv2.imread(dir_path+directory[i])) for i in range(index,index+cache_num)]
                            else:
                                index+=1
                

        elif mode=='type':
            cv2.imshow('key',key_type)
            keys=''
            
            cv2.setMouseCallback('image',lambda e,x,y,f,p:None)
            
            temp=copy.deepcopy(mark.getImage())
            px,py,pw,ph=mark.getPosition()
            marker=cv2.MARKER_TRIANGLE_DOWN
            if py<=10:
                py=py+ph+10
                marker=cv2.MARKER_TRIANGLE_UP
            cv2.drawMarker(temp,(px+5,py-5),cfg.MARKER_COLOR,marker,8)
            
            cv2.putText(temp,'type class_num',(px+10,py),cv2.FONT_HERSHEY_COMPLEX,0.5,cfg.CLS_NUM_COLOR)
            cv2.imshow('image',temp)

            while(mode=='type'):
                
                key=cv2.waitKey(0)
                if key>=0:
                    if 48<=key<58:
                        temp=copy.deepcopy(mark.getImage())
                        keys+=chr(key)
                        
                        cv2.drawMarker(temp,(px+5,py-5),cfg.MARKER_COLOR,marker,8)
                        cv2.putText(temp,keys,(px+10,py),cv2.FONT_HERSHEY_PLAIN,1,cfg.CLS_NUM_COLOR)
                        cv2.imshow('image',temp)
                    elif key==8:
                        if len(keys)>0:
                            temp=copy.deepcopy(mark.getImage())
                            keys=keys[:-1]
                            cv2.drawMarker(temp,(px+5,py-5),cfg.MARKER_COLOR,marker,8)
                            cv2.putText(temp,keys,(px+10,py),cv2.FONT_HERSHEY_PLAIN,1,cfg.CLS_NUM_COLOR)
                            cv2.imshow('image',temp)
                    elif cfg.SAVE.__contains__(chr(key)):
                        if not keys=='':
                            cv2.drawMarker(mark.getImage(),(px+5,py-5),cfg.MARKER_COLOR,marker,8)
                            cv2.putText(mark.getImage(),keys,(px+10,py),cv2.FONT_HERSHEY_PLAIN,1,cfg.CLS_NUM_COLOR)
                            mark.setClassNum(keys)
                            train_datas[mark.getPath()]=mark.makeText()
                            cv2.setWindowTitle('key',f'marked_data_count : {len(train_datas)}')
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
    except ob.SaveData:
        if train_datas:
            f=open(flags.FLAGS.output_path,'w')
            for i in train_datas.values():
                f.write(i)
                f.write('\n')
            f.close()
        else :
            print("nothing set")



# 'C:/users/user/desktop/plants/'
