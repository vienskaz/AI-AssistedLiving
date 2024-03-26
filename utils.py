import cv2
from tensorflow.keras.models import load_model
import numpy as np


def resize_image(image, target_size=(640, 480)):
    normalized = image / 255.0
    arr = cv2.resize(normalized, target_size)
    return np.array(arr)


def detect(preprocessed_image):
    model = load_model("C:/Users/User/Desktop/detect/stand_lie.h5")
    result = model.predict(preprocessed_image.reshape(
        1, *preprocessed_image.shape))

    prediction = np.argmax(result)

    if prediction == 0:
        print("lezy")

    else:
        print("stoi")
