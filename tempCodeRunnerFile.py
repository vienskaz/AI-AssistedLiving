import cv2
from tensorflow.keras.models import load_model


def screenshot():
    global cam
    cv2.imshow("screenshot", cam.read()[1])  # shows the screenshot directly
    # cv2.imwrite('screenshot.png',cam.read()[1]) # or saves it to disk


def resize_image(image, target_size=(640, 480)):
    return image.resize(target_size)


def detect(preprocessed_image):
    model = load_model("C:/Users/User/Desktop/detect/stand_lie.h5")
    result = model.predict(preprocessed_image)

    print(result)


detect("C:/Users/User/Desktop/detect/prepstanding/image_1.jpg")
