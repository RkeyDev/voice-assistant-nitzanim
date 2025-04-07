import listen
import components.speak as speak
import re
import os
import subprocess
from typing import Union, NoReturn
import threading
import components.eye_tracker as eye_tracker
import sys

screen = None

def repeat() -> None:
    screen.update_status("What to repeat?")
    print("What to repeat ?")
    speak.speak("What to repeat ?")
    text = listen.listen()
    screen.update_status(f"You said {text}")
    print(f"You said {text}")
    speak.speak(f"You said {text}")

def search_chrome() -> None:
    screen.update_status("What to search?")
    print("What to search ?")
    speak.speak("What to search ?")
    search = listen.listen()
    url = f"https://www.google.com/search?q={search.replace(' ', '+')}"
    screen.update_status(f"Searching for {search}")
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    profile_name = "Default"
    subprocess.run([chrome_path, f"--profile-directory={profile_name}", "--new-window", url])

def open_applications(text: str) -> Union[str, NoReturn]:
    screen.update_status(text)
    calendar_shortcut_path = r"C:\Users\WIN11\Desktop\Google calendar.lnk"
    os.startfile(calendar_shortcut_path)
    screen.update_status("open - not implemented")
    print(text)
    print(NotImplementedError("open - not implemented"))
    speak.speak("open - not implemented")

def search_speech(pattern: str, text: str) -> bool:
    return re.search(pattern.replace(" ", ""), text.replace(" ", "")) is not None

def remove_from_speech(pattern: str, text: str) -> str:
    return re.sub(pattern, "", text)

def start_comments(text: str = "") -> None:
    text = remove_from_speech(r"hey |hey|hi |hi|hello |hello|python |python|peyton |peyton|thank you |thank you|thanks |thanks|please |please|play |play|\d", text)
    if text in ("over", "finish", "exit", "stop"):
        sys.exit()
        return
    if search_speech("repeat this|repeat", text):
        text = remove_from_speech("repeat this |repeat this|repeat |repeat", text)
        repeat()
    if search_speech("open up|open", text):
        text = remove_from_speech("open up |open up|open |open", text)
        open_applications(text)
    if search_speech("search", text):
        text = remove_from_speech("search |search", text)
        search_chrome()
    if search_speech("mouse", text):
        screen.update_status("Starting eye tracker")
        print("Starting eye tracker")
        threading.Thread(target=eye_tracker.run_eye_tracker).start()
    screen.update_status("What would you like to do?")
    print("What would you like to do ?")
    speak.speak("What would you like to do ?")
    new_cmd = listen.listen()
    start_comments(new_cmd)



if __name__ == '__main__':
    raise RuntimeError("This script is not meant to be run directly.")
