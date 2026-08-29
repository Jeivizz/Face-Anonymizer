import cv2
import mediapipe as mp


def process_img(img, detector):
    H, W, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
    out = detector.detect(mp_image)

    if out.detections is not None:

        for detection in out.detections:
            bbox = detection.bounding_box
            x1, y1 = max(0, bbox.origin_x), max(0, bbox.origin_y)
            x2, y2 = min(W, x1 + bbox.width), min(H, y1 + bbox.height)
            img[y1:y2, x1:x2] = cv2.blur(img[y1:y2, x1:x2], (33, 33))

    return img