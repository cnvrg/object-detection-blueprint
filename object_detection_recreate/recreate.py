import os
import sys
import argparse
import shutil
import cv2
from sklearn.model_selection import train_test_split
import traceback

#define cnvrg working directory
cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")
#acceptable video formats
VID_FORMATS = ["mov", "avi", "mp4", "mpg", "mpeg", "m4v", "wmv", "mkv"]
#acceptable image formats
IMG_FORMATS = ["bmp", "jpg", "jpeg", "png", "tif", "tiff", "dng", "webp", "mpo"]



def argument_parser():
    parser = argparse.ArgumentParser(description="""Creator""")
    parser.add_argument(
        "-f",
        "--files",
        action="store",
        dest="files",
        default="/data/images",
        required=True,
        help="""Location to the folder containing all training images/videos""",
    )
    parser.add_argument(
        "--labels",
        action="store",
        dest="labels",
        default="/data/labels",
        help="""Location to the folder containing all training labels""",
    )
    parser.add_argument(
        "--keep_all_frames",
        action="store",
        dest="keep_all_frames",
        default=False,
        help="""Location to the folder containing all training labels""",
    )

    return parser.parse_args()


def argument_validation(args):
    """
    check if the files directories provided are a valid path if not raise an exception

    Arguments
    - argument parser

    Raises
    - An assertion error if the path provided is not a valid directory
    """
    img_path = args.files
    label_path = args.labels
    assert os.path.exists(
        img_path
    ), " Path to the image/video files provided does not exist "
    assert os.path.exists(
        label_path
    ), " Path to the labels files provided does not exist "


def move_files_to_folder(list_of_files, destination_folder):
    """
    move a list of files to a target directory
    """
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except:
            print(f)
            assert False


def FrameCapture(path):
    """
    Accept path to a video and extract frames from the video and save those frames
    in the same path
    """
    directory = os.path.dirname(path)
    videoname = os.path.basename(path)
    # Path to video file
    vidObj = cv2.VideoCapture(path)

    # Used as counter variable
    count = 0

    # checks whether frames were extracted
    success = 1
    try:
        success, image = vidObj.read()
    except cv2.error as e:
        print(f"while extracting frames from video {path} error occurred", e)
    while success:
        cv2.imwrite(os.path.join(directory, f"{videoname}_frame_%d.jpg" % count), image)
        success, image = vidObj.read()
        count = count + 1


def new_name_finder(name):
    """
    remove extra 0s in string for example
    frame_00001.txt will be converted to frame_1.txt
    """
    find_ = name[name.rfind("_") + 1 : -4]

    return name[: name.rfind("_") + 1] + str(int(find_))


def remove_empty_labels(path):
    """
    remove empty .txt files
    """
    if os.stat(path).st_size == 0:
        os.remove(path)
        return True
    return False


def annotations(path, videoname):
    """
    rename all the frame label files to have the same name as that
    of the video to which they belong along with frame number as suffix
    for example frame_1.txt belonging to video.mp4 will be converted to
    video.mp4_frame_1.txt
    """
    directory = os.path.dirname(path)
    filename = os.path.basename(path)
    # remove the extra zeroes
    filename = str(new_name_finder(filename)) + ".txt"
    newname = os.path.join(directory, f"{videoname}_{filename}")
    os.rename(path, newname)
    return newname


def process_videos(args):
    """
    Find all videos in the file directory
    Extract frames from the videos
    Rename the labels for each frame
    Move all the labels from the video label folder to main
    label folder.
    If the user chooses not to keep all frames, delete the frames that do not have any labels.
    """
    img_path = args.files
    label_path = args.labels
    keep_all_frames = args.keep_all_frames
    if keep_all_frames is not False:
        keep_all_frames = True
    videos = [
        os.path.join(img_path, x)
        for x in os.listdir(img_path)
        if x.endswith(tuple(VID_FORMATS))
    ]
    for video in videos:
        FrameCapture(video)
        video_name = os.path.basename(video)
        annotation_folder = os.path.join(label_path, video_name)
        video_annotations = []
        for annotation_file in os.listdir(annotation_folder):
            annotation_path = os.path.join(annotation_folder, annotation_file)
            new_name = annotations(annotation_path, video_name)
            new_annotation_file = os.path.basename(new_name)
            if not keep_all_frames:
                if remove_empty_labels(
                    os.path.join(annotation_folder, new_annotation_file)
                ):
                    os.remove(
                        os.path.join(
                            img_path, new_annotation_file.replace(".txt", ".jpg")
                        )
                    )

                else:
                    video_annotations.append(new_name)
            else:
                video_annotations.append(new_name)
        move_files_to_folder(video_annotations, label_path)


def train_test_val_split(images, annotations):
    train_images, val_images, train_annotations, val_annotations = train_test_split(
        images, annotations, test_size=0.1, random_state=1
    )
    val_images, test_images, val_annotations, test_annotations = train_test_split(
        val_images, val_annotations, test_size=0.5, random_state=1
    )

    return (
        train_images,
        train_annotations,
        val_images,
        test_images,
        val_annotations,
        test_annotations,
    )


def create_directories(img_path, label_path):
    # create subdirectories of test/train/val for images folder
    os.mkdir(os.path.join(img_path, "train"))
    os.mkdir(os.path.join(img_path, "test"))
    os.mkdir(os.path.join(img_path, "val"))

    # create subdirectories of test/train/val for labels folder
    os.mkdir(os.path.join(label_path, "train"))
    os.mkdir(os.path.join(label_path, "test"))
    os.mkdir(os.path.join(label_path, "val"))


def main():

    args = argument_parser()
    argument_validation(args)

    img_path = args.files
    label_path = args.labels
    keep_all_frames = args.keep_all_frames
    if keep_all_frames is not False:
        keep_all_frames = True

    process_videos(args)
    images = [
        os.path.join(img_path, x)
        for x in os.listdir(img_path)
        if x.endswith(tuple(IMG_FORMATS))
    ]
    annotations = [
        os.path.join(label_path, x) for x in os.listdir(label_path) if x[-3:] == "txt"
    ]
    images.sort()
    annotations.sort()

    #make sure if the user has given an image or video that is not supported we do not consider it's labels
    temp_images = [os.path.basename(image[:image.rfind(".")]) for image in images] 
    annotations = [annotation for annotation in annotations if os.path.basename(annotation)[:-4] in temp_images]
    
    # Split the dataset into train-valid-test splits
    try:
        (
            train_images,
            train_annotations,
            val_images,
            test_images,
            val_annotations,
            test_annotations,
        ) = train_test_val_split(images, annotations)
    except ValueError:
        #print(traceback.format_exc())
        assert False,("You are seeing this error, because the number of images/videos provided are too low to proceed with training")

    # create directoires
    create_directories(img_path, label_path)

    # move the files to the respective split folders
    move_files_to_folder(train_images, os.path.join(img_path, "train"))
    move_files_to_folder(val_images, os.path.join(img_path, "val"))
    move_files_to_folder(test_images, os.path.join(img_path, "test"))
    move_files_to_folder(train_annotations, os.path.join(label_path, "train"))
    move_files_to_folder(val_annotations, os.path.join(label_path, "val"))
    move_files_to_folder(test_annotations, os.path.join(label_path, "test"))

    # move the data files to cnvrg folder
    shutil.move(img_path, cnvrg_workdir)
    shutil.move(label_path, cnvrg_workdir)


if __name__ == "__main__":
    main()
