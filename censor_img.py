
import cv2
import process_img as pimg
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import argparse
import utils

args = argparser = argparse.ArgumentParser()
args.add_argument('--mode', default='image') # ['image', 'video', webcam']
args.add_argument('--file_path', default='./data/example.jpg')
args = args.parse_args()

# model_path = './blaze_face_short_range.tflite'
model_path = './blaze_face_full_range.tflite'

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.FaceDetectorOptions(base_options=base_options)

with vision.FaceDetector.create_from_options(options) as detector:
    if args.mode in ["image"]:
        img = cv2.imread(args.file_path)
        img = pimg.process_img(img, detector)

        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        utils.save_img(img, args.file_path)

    elif args.mode in ["video"]:

        cap = cv2.VideoCapture(args.file_path)
        ret, frame = cap.read()

        output_video = utils.video_parameters(frame, args.file_path)

        while ret:
            frame = pimg.process_img(frame, detector)
            output_video.write(frame)
            ret, frame = cap.read()

        cap.release()
        output_video.release()

    elif args.mode in ["webcam"]:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()

        while ret:
            frame = pimg.process_img(frame, detector)

            cv2.imshow('webcam', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            ret, frame = cap.read()

        cap.release()
        cv2.destroyAllWindows()




