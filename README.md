# YOLO_MARK_LITE_PYTHON

## Marking images for Yolo_train_datas(.py) simple and light  
---------------
### dependency

* absl-py==0.12.0  
* numpy==1.20.2  
* opencv-python==4.5.1.48  
* six==1.15.0

```
$ pip install -r requirements.txt
```  
-------------------

### marking
```
$ python mark.py [-i ./data/images]
```

### make_train_list  
> list images that have its own boxes(.txt)
```
$ python make_train.py [-i ./data/images] [-o ./data/train.txt]
```

if omit -i(image_path) or -o(output_train_path), uses paths in config.py that you can edit  
you wanna config vars such as keys,colors and paths?
> ### see config.py   
------------------

* Box format : label_num x_center y_center box_width box_height
```
1 0.6451822916666666 0.12413194444444445 0.17838541666666666 0.234375
2 0.806640625 0.6805555555555556 0.16015625 0.3541666666666667
```  
-----------
![st](https://user-images.githubusercontent.com/38782146/115654953-2ad07780-a36d-11eb-8377-8ba1485779c2.jpg)

