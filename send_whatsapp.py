import listen
import components.speak as speak
import webbrowser
import pyautogui
import time


def send_whatapp() -> None:
    # asking for a message
    print("What is the message ?")
    speak.speak("What is the message ?")
    text: str = listen.listen()  # listening for a message

    # exit key press
    if text == "over" or text == "finish" or text == "exit" or text == "stop":
        return

    phone_number: str = "+972 50-645-4778"

    try:
        webbrowser.open(f"https://web.whatsapp.com/send?phone={phone_number}&text={text}")
        time.sleep(5)
        pyautogui.press("enter")

        # if we want to close the tab uncomment this
        # time.sleep(3)
        # pyautogui.hotkey("ctrl", "w")

    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    raise RuntimeError("This script is not meant to be run directly.")
