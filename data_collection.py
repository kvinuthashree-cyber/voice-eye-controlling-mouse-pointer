import cv2
import mediapipe as mp
import os

# MediaPipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
LEFT_EYE_LANDMARKS = [474, 475, 476, 477]  # Right iris landmarks (mirror image for webcam)

# Dataset save path
DATASET_PATH = "dataset"

# Capture device
cap = cv2.VideoCapture(0)

# Ask user which direction to capture
label = input("Enter label (left/right/up/down/center): ").strip().lower()
save_dir = os.path.join(DATASET_PATH, label)
os.makedirs(save_dir, exist_ok=True)

count = 0
MAX_IMAGES = 200  # You can change this

print(f"[INFO] Starting to collect images for label: {label}")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        mesh = results.multi_face_landmarks[0].landmark
        h, w, _ = frame.shape

        # Get bounding box around iris
        x_coords = [int(mesh[i].x * w) for i in LEFT_EYE_LANDMARKS]
        y_coords = [int(mesh[i].y * h) for i in LEFT_EYE_LANDMARKS]
        min_x, max_x = min(x_coords) - 10, max(x_coords) + 10
        min_y, max_y = min(y_coords) - 10, max(y_coords) + 10

        eye_crop = frame[min_y:max_y, min_x:max_x]

        if eye_crop.shape[0] > 0 and eye_crop.shape[1] > 0:
            # Save cropped eye
            filename = os.path.join(save_dir, f"{label}_{count}.jpg")
            cv2.imwrite(filename, eye_crop)
            count += 1

        # Draw box and label
        cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)
        cv2.putText(frame, f"Collecting {label} ({count}/{MAX_IMAGES})", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        if count >= MAX_IMAGES:
            print("[INFO] Done collecting images.")
            break

    cv2.imshow("Data Collection", frame)
    if cv2.waitKey(1) == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
