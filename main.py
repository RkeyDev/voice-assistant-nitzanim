import listen as listen
import components.speak as speak
import assistant_actions
import sys


# noinspection PyMethodMayBeStatic
class VoiceAssistantApp:
    """
    A voice-activated assistant application that listens to user input
    and responds accordingly with greetings, exit commands, or unknown responses.
    """

    def __init__(self):
        self.tries: int = 0
        self.is_app_running: bool = True

    def run(self) -> None:
        """
        Starts the main application loop, listening to user input until the app exits
        or the maximum number of failed attempts is reached.
        """
        print("Starting")

        while self.is_app_running:
            try:
                self.process_voice_input()
            except Exception as e:
                self.handle_exception(e)

            if self.tries >= 3:
                self.exit_due_to_max_attempts()

        print("app finished")

    def process_voice_input(self) -> None:
        """
        Processes voice input and dispatches to the appropriate handler
        based on the input text.
        """
        text: str = listen.listen()

        if "python" in text or "peyton" in text:
            self.respond_to_greeting(text)

        elif text == "None":
            self.respond_to_no_input()

        elif text in {"over", "finish", "exit"}:
            self.respond_to_exit_command()

        else:
            self.respond_to_unknown_input(text)

    def respond_to_greeting(self, text: str) -> None:
        """
        Handles greeting input and initiates assistant actions.
        """
        print("Hi ,I'm python")
        speak.speak("Hi , I'm python")

        assistant_actions.start_comments(text)

        print("thanks for using python, good by :)")
        speak.speak("thanks for using python, good by")

        self.is_app_running = False

    def respond_to_exit_command(self) -> None:
        """
        Handles explicit app exit commands and terminates the program.
        """
        print("you exited, thanks for using python, good bye :)")
        speak.speak("you exited, thanks for using python, good bye")

        self.is_app_running = False
        sys.exit()

    def respond_to_no_input(self) -> None:
        """
        Handles the case when no voice input is detected.
        """
        print("I cant hear anything")
        speak.speak("I cant hear anything\n")
        self.tries += 1

    def respond_to_unknown_input(self, text: str) -> None:
        """
        Handles unrecognized voice input.
        """
        print(f"got this: {text}, try a different word")
        speak.speak("try a different word")

    def handle_exception(self, error: Exception) -> None:
        """
        Handles exceptions during voice input processing.
        """
        print("you got an error, try again: " + str(error))
        speak.speak("You got an error, try again")

    def exit_due_to_max_attempts(self) -> None:
        """
        Gracefully quits the application after too many failed attempts.
        """
        print("quiting")
        speak.speak("quiting")

        self.is_app_running = False


def main() -> None:
    # TODO remove the comment when UI is done
    """screen = window.MainScreen(run_app_func=app.start)
    target = screen.start_window()"""

    app = VoiceAssistantApp()
    app.run()


if __name__ == '__main__':
    main()
