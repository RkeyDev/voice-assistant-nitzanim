import listen
from typing import Union
import components.speak as speak


def transcribe() -> Union[str, None]:
    while True:
        # asking for transcribe
        print("What to transcribe ?")
        speak.speak("What to transcribe ?")
        text: str = listen.listen()  # listening what to transcribe

        # exit key press
        if text == "over" or text == "finish" or text == "exit" or text == "stop":
            return None

        # TODO integrate with UI
        print(text)


if __name__ == '__main__':
    raise RuntimeError("This script is not meant to be run directly.")
