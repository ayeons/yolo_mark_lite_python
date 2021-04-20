# YOLO_MARK_LITE_PYTHON

## Marking images for Yolo_train_datas(.py) simple and light
---------------
### dependency

* absl-py==0.12.0  
* numpy==1.20.2  
* opencv-python==4.5.1.48  
* six==1.15.0

-------------------
```
$ pip install -r requirements.txt
```
### execute
-------------------
```
$ python mark.py [--images_path ./data/images] [--output_path ./data/train.txt]
```    
if omit --images_path or --output_path, uses paths in config.py that you can edit

you wanna config vars such as path,key,color and cache-size?
### see config.py  

### format
```
./data/images/ptoilet.jpg 405,325,552,548,2 557,294,682,501,2 422,23,565,147,1 
./data/images/street.jpg 222,303,305,388,5 78,124,167,308,6 413,177,441,240,7 323,193,341,233,7 125,345,156,427,0 
```
* Row format path box1 box2 ...
* Box format : startx,starty,endx,endy,class_num

--------
![st](https://user-images.githubusercontent.com/38782146/115362530-98a96180-a1fc-11eb-8219-43f4a36a59e0.jpg)
