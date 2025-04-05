import listen as listen
import components.speak as speak
import assistant_actions
import sys

tries: int = 0
is_app_running = True


def start_application() -> None:
    print("Starting")

    while is_app_running:
        try:
            listen_to_voice_input()  # Listen to user voice input
        except Exception as e:
            handle_error(e)  # Handle an error

        if tries >= 3:
            quit_app()

    print("app finished")


def listen_to_voice_input():
    text: str = listen.listen()  # Listen to user voice
    if "python" in text or "peyton" in text:
        handle_greeting(text)

    elif text == "None":
        handle_no_input_detected()

    elif text == "over" or text == "finish" or text == "exit":
        handle_app_exit()

    else:
        handle_unknown_word(text)


def handle_greeting(text: str):
    print("Hi ,I'm python")
    speak.speak("Hi , I'm python")
    # endregion

    assistant_actions.start_comments(text)
    # region end greeting
    print("thanks for using python, good by :)")
    speak.speak("thanks for using python, good by")

    is_app_running = False


def handle_app_exit():
    # region end greeting
    print("you exited, thanks for using python, good bye :)")
    speak.speak("you exited, thanks for using python, good bye")
    # endregion
    is_app_running = False
    sys.exit()


def handle_no_input_detected():
    print("I cant hear anything")
    speak.speak("I cant hear anything\n")
    tries += 1


def handle_unknown_word(text):
    print(f"got this: {text}, try a different word")
    speak.speak("try a different word")


def handle_error(error: Exception):
    print("you got an error, try again" + str(error))
    speak.speak("You got an error, try again")


def quit_app():
    print("quiting")
    speak.speak("quiting")

    is_app_running = False


def main() -> None:
    # TODO remove the comment when UI is done
    """screen = window.MainScreen(run_app_func=startApplication)
    target=screen.start_window()"""

    start_application()


if __name__ == '__main__':
    main()
