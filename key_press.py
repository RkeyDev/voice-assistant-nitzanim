import listen
import components.speak as speak
import keyboard

from UI import main_window


def press_keys(screen: main_window.MainScreen) -> None:
    while True:
        # asking for keys to press
        print("What to press ?")
        screen.update_status("What to press ?")
        speak.speak("What to press ?")
        text: str = listen.listen()  # listening what key to press

        # exit key press
        if text == "over" or text == "finish" or text == "exit" or text == "stop":
            return None

        try:
            keyboard.press_and_release(text)
        except Exception as e:
            print(e)
            return None

        print("Pressed")
        screen.update_status("Pressed")
        speak.speak("Pressed")


if __name__ == '__main__':
    raise RuntimeError("This script is not meant to be run directly.")
