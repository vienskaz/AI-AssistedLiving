import cv2
import mediapipe as mp
import os
from PIL import Image
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

"""""
def apply_contour(image_path, output_path):
    # Inicjalizacja detektora konturów z Mediapipe
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = pose.process(image)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(
                                          color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        # Zapisz obraz
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, image)

"""""


def resize_image(image, target_size):
    return image.resize(target_size)


def apply_many_contours(images, output_folder):
    # Upewnienie się, że podana ścieżka folderu istnieje
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Inicjalizacja detektora konturów z Mediapipe
    mp_holistic = mp.solutions.holistic
    mp_drawing = mp.solutions.drawing_utils

    for i, image in enumerate(images):
        # Wykrywanie konturów na obrazie
        with mp_holistic.Holistic(static_image_mode=True) as holistic:
            # Konwersja obrazu z RGB na BGR
            bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            results = holistic.process(bgr_image)

        annotated_image = bgr_image.copy()

        # Parametry rysowania konturów
        pose_drawing_spec = mp_drawing.DrawingSpec(
            color=(245, 117, 66), thickness=2, circle_radius=2)
        connection_drawing_spec = mp_drawing.DrawingSpec(
            color=(245, 66, 230), thickness=2, circle_radius=2)

        # Rysowanie konturów z niestandardowymi parametrami
        mp_drawing.draw_landmarks(
            annotated_image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
            pose_drawing_spec, connection_drawing_spec)

        output_path = os.path.join(output_folder, f"image_{i}.jpg")

        cv2.imwrite(output_path, annotated_image)


stand_path = r"C:\Users\User\Desktop\detect\standing"
lying_path = r"C:\Users\User\Desktop\detect\lying"
prepstanding_path = r"C:\Users\User\Desktop\detect\prepstanding"
preplying_path = r"C:\Users\User\Desktop\detect\preplying"

stand_files = [os.path.join(stand_path, f) for f in os.listdir(
    stand_path) if os.path.isfile(os.path.join(stand_path, f))]
lying_files = [os.path.join(lying_path, f) for f in os.listdir(
    lying_path) if os.path.isfile(os.path.join(lying_path, f))]

desired_width = 640
desired_height = 480

stand_arrays = []
for stand_file in stand_files:
    try:
        stand = Image.open(stand_file)
        # Specify desired width and height
        stand_resized = resize_image(stand, (desired_width, desired_height))
        stand_array = np.array(stand_resized)
        stand_arrays.append(stand_array)
    except:
        pass

lying_arrays = []
for lying_file in lying_files:
    try:
        lying = Image.open(lying_file)
        # Specify desired width and height
        lying_resized = resize_image(lying, (desired_width, desired_height))
        lying_array = np.array(lying_resized)
        lying_arrays.append(lying_array)
    except:
        pass

apply_many_contours(lying_arrays, preplying_path)
