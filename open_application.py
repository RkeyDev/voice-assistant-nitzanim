import os

import pyautogui

import components.speak as speak
from typing import Union, NoReturn
import assistant_actions


def open_applications(text: str) -> Union[str | NoReturn]:
    path = ""

    # speech check's
    if assistant_actions.search_speech("calender|calendar", text):
        path = r"C:\Users\WIN11\Desktop\Google calendar.lnk"

    if assistant_actions.search_speech("notepad", text):
        path = r"C:\Windows\System32\notepad.exe"

    if assistant_actions.search_speech("calculator", text):
        path = r"C:\Windows\System32\calc.exe"

    if assistant_actions.search_speech("settings", text):
        pyautogui.hotkey("win", "i")
        path = "None"

    # path check's
    if path == "None":
        print(f"starting {text} application")
        speak.speak(f"starting {text} application")
        return None

    if path == "":
        raise Exception(f"{text} application not found/is not an option")

    # path start
    try:
        os.startfile(path)
        print(f"starting {text} application")
        speak.speak(f"starting {text} application")

    except FileNotFoundError:
        print(f"The {text} application is not found")
        speak.speak(f"The {text} application is not found")


if __name__ == '__main__':
    raise RuntimeError("This script is not meant to be run directly.")
