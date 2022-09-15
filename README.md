Use this blueprint with your custom data to train a tailored model and deploy an API endpoint which detects objects in images. Training an object-detection algorithm requires data provided in the form of object-containing images, the object locations, and their labels. To train this model with your data, provide the following two folders in the S3 Connector:
* Images − A folder with the object-containing images to train the model
* Labels − A folder with labels that correlate to the objects in the images folder

Complete the following steps to train the object-detector model:
1. Click the **Use Blueprint** button. The cnvrg Blueprint Flow page displays.
2. In the flow, click the **S3 Connector** task to display its dialog.
   * Within the **Parameters** tab, provide the following Key-Value pair information:
     - **Key**: `bucketname` - **Value**: enter the data bucket name
     - **Key**: `prefix` - **Value**: provide the main path where the data folder is located
   * Click the **Advanced** tab to change resources to run the blueprint, as required.
3. Return to the flow and click the **Recreate** task to display its dialog.
   * Within the **Parameters** tab, provide the following Key-Value pair information:
     - **Key**: `images` – **Value**: provide the path to the images including the S3 prefix, with the following format: `/input/s3_connector/<prefix>/images`
     - **Key**: `labels` – **Value**: provide the path to the labels including the S3 prefix, with the following format: `/input/s3_connector/<prefix>/labels`
   NOTE: You can use prebuilt example data paths already provided.
   * Click the **Advanced** tab to change resources to run the blueprint, as required.
4. Click the **Retrain** task to display its dialog.
   * Within the **Parameters** tab, provide the following Key-Value pair information:
     - **Key**: `batch` – **Value**:  set the batch size the neural network ingests before calculating loss and readjusting weights
     - **Key**: `epochs` – **Value**: set the number of times the neural network trains the dataset
     - **Key**: `class_names` – **Value**: provide the names of the classes for the model to learn
   * Click the **Advanced** tab to change resources to run the blueprint, as required.
4.	Click the blue **Run** button. The cnvrg software launches the training blueprint as set of experiments, generating a trained object-detector model and deploying it as a new API endpoint.
5. Track the blueprint's real-time progress in its experiments page, which displays artifacts such as logs, metrics, hyperparameters, and algorithms.
6. Click the **Serving** tab in the project and locate your endpoint. Complete one or both of the following options:
   * Use the Try it Live section with any object image to check the model.
   * Use the bottom integration panel to integrate your API with your code by copying in your code snippet.
   
A custom model and an API endpoint which can detect objects in images have now been trained and deployed. Click [here](link) for detailed instructions to run this blueprint. To learn how this blueprint was created, click [here](https://github.com/cnvrg/object-detection-blueprint).
