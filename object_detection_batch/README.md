# Object Detection Batch

This library can be used to run object detections on videos and images stored in a directory. The user needs to provide the path to a directory containing videos and images. Supported default object classes for detection can be found [here](https://github.com/ultralytics/yolov5/blob/master/data/coco.yaml) under the title `names`. If you want to detect custom objects you will need to provide the path to the weights file trained using the train blueprint.

Supported video formats are:
- .mov
- .avi
- .mp4
- .mpg
- .mpeg
- .m4v
- .wmv
- .mkv

Supported image formats are:
- bmp
- jpg
- jpeg
- png
- tif
- tiff
- dng
- webp
- mpo
  
The user will find video/image outputs in the output artifacts. For every single input video/image processed, a single output video/image with the same name will be produced. Each video/image will contain bounding box detections drawn on the detected objects.

# Input Arguments:

- `--source` : The path to the directory containing videos to be processed.
- `--weights` : If you want to use your custom weights that you trained using the train blueprint, provide the path to weights file in this argument. If you wish to go with default weights leave this argument empty.

# Command to run

```
cnvrg run  --datasets='[{id:"{dataset_id}",commit:"{commit_id}"}]' --machine="{compute_template}" --image={docker_image} --sync_before=false python3 batch_predict.py --source {path_to_dir}
```

# Sample Command

```
cnvrg run  --datasets='[{id:"object",commit:"2e01e17467891f7c933dbaa00e1459d23db3fe4f"}]' --machine="AWS-ON-DEMAND.large" --image=cnvrg/cnvrg:v5.0 --sync_before=false python3 batch_predict.py --source /data/object
```

# Refrence

https://github.com/ultralytics/yolov5

