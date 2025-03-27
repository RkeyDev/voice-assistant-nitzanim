import os
import components.speak as speak
from typing import Union, NoReturn

def open_applications(text: str) -> Union[str | NoReturn]:
    # in progress
    calendar_shortcut_path = r"C:\Users\WIN11\Desktop\Google calendar.lnk"
    os.startfile(calendar_shortcut_path)
    print(text)


    print(NotImplementedError("open - not implemented"))
    speak.speak("open - not implemented")
