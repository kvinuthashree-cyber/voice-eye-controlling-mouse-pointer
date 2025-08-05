# voice_listener.py

import queue
import sounddevice as sd
import vosk
import json

# Load the Vosk model
model_path = r"C:\Users\vinut\OneDrive\Desktop\eye-controlling-mouse-pointer\model\vosk-model-small-en-in-0.4"
model = vosk.Model(model_path)

q = queue.Queue()

# Audio callback to store audio data
def callback(indata, frames, time, status):
    if status:
        print(f"[Audio Status] {status}")
    q.put(bytes(indata))

# Start voice recognizer
def listen_for_commands(callback_func):
    print("[VOICE] Listening... (say 'click', 'scroll', etc.)")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if 'text' in result:
                    command = result['text']
                    if command:
                        print(f"[VOICE] Detected: {command}")
                        callback_func(command)  # Send to command handler
