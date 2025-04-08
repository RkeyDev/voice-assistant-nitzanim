import time

import listen
from typing import Union
import components.speak as speak
from UI import main_window


def transcribe(screen: main_window.MainScreen) -> Union[str, None]:
    while True:
        # asking for transcribe
        print("What to transcribe ?")
        screen.update_status("What to transcribe ?")
        speak.speak("What to transcribe ?")
        text: str = listen.listen()  # listening what to transcribe

        # exit key press
        if text == "over" or text == "finish" or text == "exit" or text == "stop":
            return None

        screen.update_status(text)
        print(text)
        time.sleep(3)


if __name__ == '__main__':
    raise RuntimeError("This script is not meant to be run directly.")
