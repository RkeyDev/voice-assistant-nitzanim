import speech_recognition as s
import components.speak as speak
from typing import NoReturn, Union
from UI import main_window 

speech_ready: bool = False


def adjust_for_speech(sr: s.Recognizer, source: s.Microphone,screen:main_window.MainScreen) -> None:
    global speech_ready

    # if ambient noise already adjusted for
    if speech_ready:
        return None

    # requesting quiet
    print("Do not speak pls")
    screen.update_status("Do not speak please")
    speak.speak("Do not speak please")

    # adjusting
    sr.adjust_for_ambient_noise(source, duration=2)
    speech_ready = True

    # allowing for speech
    print("Now speak pls")
    screen.update_status("Now speak please")
    speak.speak("Now speak please")


def listen(screen:main_window.MainScreen) -> Union[str, NoReturn]:
    sr: s.Recognizer = s.Recognizer()

    # opening microphone as sound source
    with s.Microphone() as main_source:
        while True:
            try:
                adjust_for_speech(sr, main_source,screen)
                audio: s.AudioData = sr.listen(main_source, phrase_time_limit=3, timeout=10)  # listening for speech
                text = sr.recognize_google(audio)  # recognizing words from audio
                text = text.lower()  # all lower case

                # got text so stop
                if text != "":
                    break

            except s.exceptions.UnknownValueError:
                # couldn't translate audio to text
                print("I couldn't understand, please repeat")
                screen.update_status("Now speak please")
                speak.speak("I couldn't understand, please repeat")

            except s.exceptions.WaitTimeoutError:
                # couldn't hear anything 
                return "None"

            except Exception as unknown_error:
                print(f"damn... you got this exception:")
                print(unknown_error)
                return

        return text


if __name__ == '__main__':
    raise RuntimeError("This script is not meant to be run directly.")