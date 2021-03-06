
class SaveAndExit(Exception):
    def __init__(self,msg=None):
        self.msg=msg
    def __str__(self):
        return self.msg

class Mark:
    
    def __init__(self,path,image):
        self._path=path
        self._datas=[]
        self._images=[image]
    
    def getPath(self):
        return self._path

    def getImage(self):
        return self._images[-1]

    def getPrevImage(self):
        return self._images[-2]

    def remove(self):
        self._datas.pop()
        self._images.pop()
    
    def add(self,data,image):
        if len(data)!=5:
            raise SystemError('len of data is not 5')
        self._datas.append(data)
        self._images.append(image)

    def setPosition(self,position):
        self._datas[-1][1]=position[0]
        self._datas[-1][2]=position[1]
        self._datas[-1][3]=position[2]
        self._datas[-1][4]=position[3]

    def setClassNum(self,class_num):
        self._datas[-1][0]=class_num

    def makeText(self):
        result=''
        
        for j in range(len(self._datas)):
            if j!=0:
                result+='\n'
            result+=f'{self._datas[j][0]} {self._datas[j][1]} {self._datas[j][2]} {self._datas[j][3]} {self._datas[j][4]}'

        return result
    
    def getLenDatas(self):
        return len(self._datas)
