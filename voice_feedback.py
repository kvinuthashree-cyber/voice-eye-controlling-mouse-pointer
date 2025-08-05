import pyttsx3

class VoiceFeedback:
    def __init__(self, enable=True):
        self.engine = pyttsx3.init()
        self.enable = enable
        self.engine.setProperty('rate', 160)  # Adjust speed

    def speak(self, message):
        if self.enable:
            self.engine.say(message)
            self.engine.runAndWait()
