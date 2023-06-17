from ultralytics import YOLO
import cv2
import os

YOLO_DATA = "/home/mine01/Desktop/code/AWP/Cows_identification/cows_datasets"
INPUT_DIR = "/home/mine01/Desktop/code/AWP/Cows_identification/cows_datasets/val"
OUTPUT_DIR = "/home/mine01/Desktop/code/AWP/Cows_identification/val_results_l"
# Yolo nano:  train2[10 mins, 50 epochs] (val accuracy:0.971);
# Yolo small: train[15 mins, 50 epochs] (val accuracy:0.991);
# Yolo medium: train3[30 mins, 50 epochs] (val accuracy:0.991);
# Yolo large: train4[1.2 hours, 50 epochs] (val accuracy: 0.987);
MODEL_PATH = 'runs/classify/train3/weights/best.pt'


def init_yolo(model_path, train):
    if train:
        # Load a pretrained YOLO model (recommended for training)
        yolo = YOLO('yolov8l-cls.pt')

        # Train the model
        yolo.train(data=YOLO_DATA, epochs=50, imgsz=640)
    else:
        # Load a trained YOLO model
        yolo = YOLO(model_path)

    # Validate the model
    metrics = yolo.val()
    print(metrics.top1)   # top1 accuracy
    print(metrics.top5)   # top5 accuracy

    return yolo


def recreate_directory_structure(input_dir, output_dir):
    # Recreate the same directory structure in output directory
    for root, dirs, files in os.walk(input_dir):
        for dir_ in dirs:
            os.makedirs(os.path.join(output_dir, os.path.relpath(os.path.join(root, dir_), input_dir)), exist_ok=True)


def classify_and_save_results(yolo, input_dir, output_dir):
    # Classify each image and save results
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(('.jpg', '.png', '.jpeg')):  # add or remove file extensions as required
                image_path = os.path.join(root, file)
                result = yolo(image_path)
                res_plotted = result[0].plot()

                # Generate a save path with a new name
                output_path = os.path.join(output_dir, os.path.relpath(root, input_dir), f'{file}')
                cv2.imwrite(output_path, res_plotted)


def yolo_train(train = False):
    yolo = init_yolo(MODEL_PATH, train=train)
    # recreate_directory_structure(INPUT_DIR, OUTPUT_DIR)
    # classify_and_save_results(yolo, INPUT_DIR, OUTPUT_DIR)
    return yolo

