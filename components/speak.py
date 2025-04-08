import pyttsx3 as p3
from typing import Union, NoReturn


def speak(text: str) -> Union[None | NoReturn]:
    try:
        voice: p3.Engine = p3.init()
        voice.say(text)
        voice.runAndWait()
    except Exception as e:
        print(f"damn... you got this exception:")
        print(e)
        return None


if __name__ == '__main__':
    raise RuntimeError("This script is not meant to be run directly.")
