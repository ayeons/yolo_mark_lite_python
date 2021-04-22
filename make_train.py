from absl import app,flags
import os
import config as cfg

flags.DEFINE_string('i',cfg.IMG_PATH,'image directory path')
flags.DEFINE_string('o',cfg.TRAIN_TXT_PATH,'train.txt file path')

def main(v):
    path=flags.FLAGS.i+'/'
    count=0
    o_path=flags.FLAGS.o
    f=open(o_path,'w')
    d=os.listdir(path)
    for i in range(len(d)):
        if not d[i].endswith('txt') and os.path.isfile(path+d[i][:d[i].rfind('.')]+'.txt'):
            if i!=0:
                f.write('\n')
            f.write(path+d[i])
            count+=1
    f.close()
    print(f'save {count} items')
    if count==0:
        os.remove(o_path)

if __name__=='__main__':
    app.run(main)
