import cv2
import pyautogui
import threading
import time
import speech_recognition as sr
import mediapipe as mp

# Initialize mediapipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,  # REQUIRED for iris landmarks
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def track_eye_movement():
    cap = cv2.VideoCapture(0)
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
            face_landmarks = results.multi_face_landmarks[0]
            landmarks = face_landmarks.landmark

            if len(landmarks) >= 300:
                left_eye = landmarks[33]  # Reliable outer eye landmark
                screen_x = screen_w * left_eye.x
                screen_y = screen_h * left_eye.y
                pyautogui.moveTo(screen_x, screen_y, duration=0.1)
            else:
                print(f"[DEBUG] Only {len(landmarks)} landmarks found.")
        else:
            print("[DEBUG] No face detected.")

        cv2.imshow("Eye Tracker", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def execute_voice_command(command):
    command = command.lower()
    print(f"[COMMAND RECEIVED] → {command}")

    if "click" in command:
        pyautogui.click()
    elif "scroll up" in command:
        pyautogui.scroll(500)
    elif "scroll down" in command:
        pyautogui.scroll(-500)
    elif "open calculator" in command:
        pyautogui.press('win'); time.sleep(1); pyautogui.write('calculator'); pyautogui.press('enter')
    elif "open notepad" in command:
        pyautogui.press('win'); time.sleep(1); pyautogui.write('notepad'); pyautogui.press('enter')
    elif "open whatsapp" in command:
        pyautogui.press('win'); time.sleep(1); pyautogui.write('whatsapp'); pyautogui.press('enter')
    elif "close tab" in command:
        pyautogui.hotkey('ctrl', 'w')
    else:
        print("[INFO] Command not recognized.")

def listen_voice():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        try:
            with mic as source:
                print("[VOICE] Listening...")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)
                print(f"[VOICE] Detected: {command}")
                execute_voice_command(command)
        except sr.UnknownValueError:
            print("[VOICE] Didn't understand.")
        except sr.RequestError:
            print("[VOICE] Request failed.")

# Start both threads
threading.Thread(target=listen_voice, daemon=True).start()
threading.Thread(target=track_eye_movement, daemon=True).start()

# Keep main thread alive
while True:
    time.sleep(1)
