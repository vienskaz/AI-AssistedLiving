import cv2
import mediapipe as mp
import time
from utils import resize_image
from utils import detect
import os
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

if __name__ == "__main__":

    try:
        os.remove("ss.jpg")
    except:
        pass

    cap = cv2.VideoCapture(0)

    with mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6) as pose:
        last_save_time = time.time()  # Inicjalizacja czasu ostatniego zapisu
        while cap.isOpened():
            ret, frame = cap.read()

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            detected = False
            try:
                left_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
                right_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]
                left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
                right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
                left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(
                                              color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(
                                              color=(245, 66, 230), thickness=2, circle_radius=2))
                detected = True

            except:
                detected = False

            if detected:
                cv2.imshow('Mediapipe Feed', image)

                current_time = time.time()

                if current_time - last_save_time >= 10:
                    cv2.imwrite("ss.jpg", image)
                    last_save_time = current_time
                    camera = cv2.imread("ss.jpg")
                    prep_camera = resize_image(camera)
                    detect(prep_camera)

            else:
                cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
