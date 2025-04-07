import os
import components.speak as speak
from typing import Union, NoReturn
import assistant_actions


def open_applications(text: str) -> Union[str | NoReturn]:
    path = ""

    if assistant_actions.search_speech("calender|calendar", text):
        path = r"C:\Users\WIN11\Desktop\Google calendar.lnk"

    # TODO add more application

    if path == "":
        raise Exception(f"{text} application not found/is not an option")

    try:
        os.startfile(path)
        print(f"starting {text} application")
        speak.speak(f"starting {text} application")

    except FileNotFoundError:
        print(f"The {text} application is not found")
        speak.speak(f"The {text} application is not found")


if __name__ == '__main__':
    raise RuntimeError("This script is not meant to be run directly.")
