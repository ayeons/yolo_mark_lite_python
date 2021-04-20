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
