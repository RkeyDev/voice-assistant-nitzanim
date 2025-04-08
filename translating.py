import listen
import components.speak as speak
from translate import Translator

from UI import main_window


def translate(screen: main_window.MainScreen, to_language: str = "he") -> str:
    # asking for a sentence to translate
    print("What to translate ?")
    speak.speak("What to translate ?")
    text: str = listen.listen(screen)  # listening for sentence

    # exit key press
    if text == "over" or text == "finish" or text == "exit" or text == "stop":
        return ""

    try:
        translator = Translator(from_lang="en", to_lang=to_language)
        return translator.translate(text)
    except Exception as e:
        print(e)
        return ""


if __name__ == '__main__':
    raise RuntimeError("This script is not meant to be run directly.")
