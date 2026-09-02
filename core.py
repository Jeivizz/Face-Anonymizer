import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import process_img as pimg

MODEL_PATH = './blaze_face_full_range.tflite'


def load_detector():
    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.FaceDetectorOptions(base_options=base_options)
    return vision.FaceDetector.create_from_options(options)


def anonymize_single_image(image_path, detector):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Not possible to process image: {image_path}")

    processed_img = pimg.process_img(img, detector)
    return processed_img