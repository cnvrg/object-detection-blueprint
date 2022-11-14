Use this batch blueprint to run in batch mode a pretrained tailored model with your custom data which detects object elements in images and videos stored in a directory. To run this blueprint, provide the S3 Connector path to a directory folder containing videos and images.

Click [here](https://github.com/ultralytics/yolov5/blob/master/data/coco.yaml) to view under the title names the supported default object classes for detection. To detect custom objects, the path to the weights file is required. Run this counterpart’s [training blueprint](https://metacloud.cloud.cnvrg.io/marketplace/blueprints/object-detection-training), and then upload the trained model weights to the S3 Connector.

Click [here]() to view this blueprint's supported video and image formats.

Complete the following steps to run this object-detector blueprint in batch mode:
1. Click the **Use Blueprint** button. The cnvrg Blueprint Flow page displays.
2. Click the **S3 Connector** task to display its dialog.
   - Within the **Parameters** tab, provide the following Key-Value pair information:
     - Key: `bucketname` − Value: provide the data bucket name
     - Key: `prefix` – Value: provide the main to the data folder
   - Click the **Advanced** tab to change resources to run the blueprint, as required.
3. Click the **Batch** task to display its dialog.
   - Within the **Parameters** tab, provide the following Key-Value pair information:
     - Key: `source` – Value: provide the S3 location containing all the images and videos
     - `/input/s3_connector/object_detection_batch` − ensure the path adheres to this format
     NOTE: You can use prebuilt example data paths provided.
   - Click the **Advanced** tab to change resources to run the blueprint, as required.
4. Click the **Run** button. The cnvrg software deploys a object-detector model that detects objects and their locations in a batch of images.
5. Track the blueprint’s real-time progress in its Experiments page, which displays artifacts such as logs, metrics, hyperparameters, and algorithms.
6. Select **Batch > Experiments > Artifacts** and locate the output files.
7. Select a File Name, click the Menu icon, and select **Open File** to view an output image or video file.

A tailored model that detects objects, draws their boundaries, and labels them in images and videos has now been deployed in batch mode.

For detailed instructions on this blueprint's run, click [here](). To learn how this blueprint was created, click [here](https://github.com/cnvrg/object-detection-blueprint).
