import key_press
import listen as listen
import components.speak as speak
import re
import subprocess
import threading
import components.eye_tracker as eye_tracker
import send_whatsapp
import translating
import voice_to_text
from UI import main_window
from game import start_game
from open_application import open_applications


def repeat(screen: main_window.MainScreen) -> None:
    # asking for repeat
    print("What to repeat ?")
    screen.update_status("What to repeat ?")
    speak.speak("What to repeat ?")
    text: str = listen.listen()  # listening what to repeat

    # repeating
    print(f"You said {text}")
    screen.update_status(f"You said {text}")
    speak.speak(f"You said {text}")


def search_chrome(screen: main_window.MainScreen) -> None:
    # asking for search
    print("What to search ?")
    screen.update_status("What to search ?")
    speak.speak("What to search ?")
    search: str = listen.listen()  # listening for what to search

    try:
        url = f"https://www.google.com/search?q={search.replace(' ', '+')}"  # creating url from speech

        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        profile_name = "Default"

        subprocess.run([chrome_path, f"--profile-directory={profile_name}", "--new-window", url])  # searching google
    except Exception as e:
        print("You got an exception while opening chrome")
        screen.update_status("You got an exception while opening chrome")
        return None

    print("Opened")
    screen.update_status("opened")
    speak.speak("opened")


def search_speech(pattern: str, text: str) -> bool:
    processed_pattern = pattern.replace(" ", "")  # removing all whitespaces
    processed_text = text.replace(" ", "")  # removing all whitespaces

    return re.search(processed_pattern, processed_text) is not None  # searching for pattern in the text


def remove_from_speech(pattern: str, text: str) -> str:
    return re.sub(pattern, "", text)  # removing all pattern occurrences from text


def start_comments(text: str, screen: main_window.MainScreen) -> None:
    print(text)
    # removing starting sentences(unneeded words)
    text = remove_from_speech(r"hey |hey|hi |hi|hello |hello|python |python|peyton |peyton|thank you |thank "
                              r"you|thanks |thanks|please |please|play |play|\\d|and |and|an |an", text)

    # region searching for talking patterns
    # stopping commend
    if text == "over" or text == "finish" or text == "exit" or text == "stop":
        return None

    # commend repeat
    if search_speech("repeat this|repeat", text):
        text = remove_from_speech("repeat this |repeat this|repeat |repeat", text)
        repeat(screen)

    # commend open
    if search_speech("open up|open", text):
        text = remove_from_speech("open up |open up|open |open|start |start", text)
        open_applications(text, screen)

    # commend search
    if search_speech("search", text):
        text = remove_from_speech("search |search", text)
        search_chrome(screen)

    # commend mouse
    if search_speech("mouse", text):
        text = remove_from_speech("mouse |mouse", text)
        print("Starting eye tracker")
        threading.Thread(target=eye_tracker.run_eye_tracker()).start()  # run eye tracker

    # commend send
    if search_speech("send|text|what's up|whatsapp", text):
        text = remove_from_speech("send |sent|text |text|what's up |what's up|whatsapp |whatsapp", text)
        send_whatsapp.send_whatapp(screen)

    # commend translate
    if search_speech("translate|trslate", text):
        text = remove_from_speech("translate |translate|trslate |trslate", text)
        screen.update_status(translating.translate(screen, "he"))

    # commend game
    if search_speech("start game|game", text):
        text = remove_from_speech("start game |start game|game |game", text)
        start_game(screen)

    # commend press\keyboard\key
    if search_speech("press|keyboard|key", text):
        text = remove_from_speech("press |press|keyboard |keyboard|keys |keys|key |key", text)
        key_press.press_keys(screen)

    # commend press\keyboard\key
    if search_speech("transcribe", text):
        text = remove_from_speech("transcribe", text)
        voice_to_text.transcribe(screen)

    print(text)
    # commends handled - asking again
    print("What would you like to do ?")
    screen.update_status("What would you like to do ?")
    speak.speak("What would you like to do ?")
    new_commend: str = listen.listen()
    start_comments(new_commend, screen)

    # endregion


if __name__ == '__main__':
    raise RuntimeError("This script is not meant to be run directly.")
