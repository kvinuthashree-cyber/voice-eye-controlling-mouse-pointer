import pyautogui
import os
import webbrowser

def execute_command(command):
    print(f"[COMMAND RECEIVED] → {command}")

    command = command.lower()

    if "click" in command:
        pyautogui.click()

    elif "scroll up" in command:
        pyautogui.scroll(300)

    elif "scroll down" in command:
        pyautogui.scroll(-300)

    elif "close all tabs" in command:
        for _ in range(10):  # try closing multiple
            pyautogui.hotkey('ctrl', 'w')

    elif "open notepad" in command:
        os.system("start notepad")

    elif "open chrome" in command:
        os.system("start chrome")

    elif "open file explorer" in command:
        os.system("explorer")

    elif "open command prompt" in command or "open cmd" in command:
        os.system("start cmd")

    elif "minimize window" in command:
        pyautogui.hotkey("win", "down")

    elif "maximize window" in command:
        pyautogui.hotkey("win", "up")

    elif "shutdown" in command:
        os.system("shutdown /s /t 5")

    else:
        print("❓ Command not recognized.")
