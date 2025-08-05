import threading
import pyautogui
import pyttsx3
import speech_recognition as sr
import cv2
import time
import numpy as np
from eye_tracker import EyeTracker  # uses CNN model

# Init
pyautogui.FAILSAFE = False
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    print(f"[VOICE] {text}")
    engine.say(text)
    engine.runAndWait()

# ========== VOICE COMMAND ==========
def execute_command(command):
    command = command.lower()
    print(f"[CMD] → {command}")

    if "click" in command:
        pyautogui.click()
        speak("Clicked")

    elif "scroll up" in command:
        pyautogui.scroll(500)
        speak("Scrolling up")

    elif "scroll down" in command:
        pyautogui.scroll(-500)
        speak("Scrolling down")

    elif "type" in command:
        text = command.replace("type", "").strip()
        pyautogui.write(text)
        speak(f"Typed {text}")

    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()

    else:
        speak("Command not recognized")

def voice_loop():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        print("[VOICE] Listening...")
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f"[VOICE] Heard: {command}")
            execute_command(command)
        except:
            speak("Could not understand")

# ========== EYE CONTROL ==========
def eye_loop():
    tracker = EyeTracker()
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("[ERROR] Could not open webcam")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        direction = tracker.get_eye_direction(frame)

        if direction == "left":
            pyautogui.moveRel(-15, 0)
        elif direction == "right":
            pyautogui.moveRel(15, 0)
        elif direction == "up":
            pyautogui.moveRel(0, -15)
        elif direction == "down":
            pyautogui.moveRel(0, 15)
        elif direction == "center":
            pass  # do nothing

        cv2.imshow("Eye Control", frame)
        if cv2.waitKey(1) == 27:  # ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

# ========== RUN BOTH ==========
if __name__ == "__main__":
    speak("Starting voice and eye control system")

    # Run in threads
    voice_thread = threading.Thread(target=voice_loop)
    eye_thread = threading.Thread(target=eye_loop)

    voice_thread.start()
    eye_thread.start()

    voice_thread.join()
    eye_thread.join()
