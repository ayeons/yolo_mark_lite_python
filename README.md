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
./data/images/ptoilet.jpg 419,9,148,134,2 397,315,162,233,1 561,294,116,202,1 
./data/images/street.jpg 124,342,31,90,7 97,324,29,107,7 221,307,80,79,3 81,127,84,175,4 409,172,34,66,5 325,195,17,38,5 
```
* Row format path box1 box2 ...
* Box format : x_start,y_start,box_width,box_height,class_num

--------
![st](https://user-images.githubusercontent.com/38782146/115362530-98a96180-a1fc-11eb-8219-43f4a36a59e0.jpg)
