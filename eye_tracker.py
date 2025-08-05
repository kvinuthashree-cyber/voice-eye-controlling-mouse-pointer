import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model

class EyeTracker:
    def __init__(self):
        self.model = load_model("model/eye_model.h5")
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
        self.directions = ['left', 'right', 'up', 'down', 'center']

    def get_eye_roi(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)

        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            h, w, _ = frame.shape
            # Left eye indices (use right eye if needed)
            indices = [33, 133, 159, 145, 160, 161]  # around left eye

            points = [(int(face_landmarks.landmark[i].x * w),
                       int(face_landmarks.landmark[i].y * h)) for i in indices]

            x_vals = [p[0] for p in points]
            y_vals = [p[1] for p in points]
            x1, y1 = max(min(x_vals) - 10, 0), max(min(y_vals) - 10, 0)
            x2, y2 = min(max(x_vals) + 10, w), min(max(y_vals) + 10, h)

            eye_img = frame[y1:y2, x1:x2]
            return eye_img

        return None

    def get_eye_direction(self, frame):
        eye = self.get_eye_roi(frame)
        if eye is not None and eye.size > 0:
            gray_eye = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray_eye, (64, 64))  # match your model input size
            normalized = resized / 255.0
            reshaped = normalized.reshape(1, 64, 64, 1)

            prediction = self.model.predict(reshaped)
            class_id = np.argmax(prediction)
            direction = self.directions[class_id]

            # Optional: Draw box
            cv2.putText(frame, direction, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            return direction
        return "center"
    def track_eyes():
     cap = cv2.VideoCapture(0)
     if not cap.isOpened():
        print("[ERROR] Webcam not detected!")
        return

    screen_w, screen_h = pyautogui.size()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[DEBUG] Frame not received from webcam.")
            continue

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            print("[DEBUG] Face detected.")
            for face_landmarks in results.multi_face_landmarks:
                ih, iw, _ = frame.shape

                try:
                    right_eye_landmarks = [33, 133]  # outer corners
                    left_point = face_landmarks.landmark[right_eye_landmarks[0]]
                    right_point = face_landmarks.landmark[right_eye_landmarks[1]]

                    cx = int((left_point.x + right_point.x) / 2 * iw)
                    cy = int((left_point.y + right_point.y) / 2 * ih)

                    screen_x = screen_w * left_point.x
                    screen_y = screen_h * left_point.y
                    pyautogui.moveTo(screen_x, screen_y, duration=0.1)

                except IndexError:
                    print("[DEBUG] Not enough eye landmarks.")

        else:
            print("[DEBUG] No face detected.")

        cv2.imshow("Eye Tracker", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
