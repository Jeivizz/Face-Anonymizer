import os
import cv2


output_dir = './output'

def fileName_split(file_path):
    filename = os.path.basename(file_path)
    name = os.path.splitext(filename)[0]
    return name

def save_img(img, img_path):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)


    saved_name = fileName_split(img_path) + '-blurred.png'
    cv2.imwrite(os.path.join(output_dir, saved_name), img)


def video_parameters(frame, video_path):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    saved_name = fileName_split(video_path) + '-blurred.mp4'

    output_video = cv2.VideoWriter(
        os.path.join(output_dir, saved_name),
        cv2.VideoWriter_fourcc(*'MP4V'),
        25,
        (frame.shape[1], frame.shape[0])
    )
    return output_video



