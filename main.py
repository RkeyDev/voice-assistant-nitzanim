import listen
import components.speak as speak
import assistant_actions
import sys
from UI.main_window import MainScreen

class VoiceAssistantApp:
    def __init__(self, screen):
        self.screen = screen
        self.tries = 0
        self.is_app_running = True

    def run(self) -> None:
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
        text = listen.listen(self.screen)
        if "python" in text or "peyton" in text:
            self.respond_to_greeting(text)
        elif text == "None":
            self.respond_to_no_input()
        elif text in {"over", "finish", "exit"}:
            self.respond_to_exit_command()
        else:
            self.respond_to_unknown_input(text)

    def respond_to_greeting(self, text: str) -> None:
        self.screen.update_status("Hi, I'm python")
        print("Hi ,I'm python")
        speak.speak("Hi , I'm python")
        assistant_actions.start_comments(text)
        self.screen.update_status("thanks for using python, good bye")
        print("thanks for using python, good bye")
        speak.speak("thanks for using python, good bye")
        self.is_app_running = False

    def respond_to_exit_command(self) -> None:
        self.screen.update_status("you exited, thanks for using python, good bye")
        print("you exited, thanks for using python, good bye")
        speak.speak("you exited, thanks for using python, good bye")
        self.is_app_running = False
        sys.exit()

    def respond_to_no_input(self) -> None:
        self.screen.update_status("I cant hear anything")
        print("I cant hear anything")
        speak.speak("I cant hear anything")
        self.tries += 1

    def respond_to_unknown_input(self, text: str) -> None:
        self.screen.update_status("try a different word")
        print(f"got this: {text}, try a different word")
        speak.speak("try a different word")

    def handle_exception(self, error: Exception) -> None:
        self.screen.update_status("You got an error, try again")
        print("you got an error, try again: " + str(error))
        speak.speak("You got an error, try again")

    def exit_due_to_max_attempts(self) -> None:
        self.screen.update_status("quiting")
        print("quiting")
        speak.speak("quiting")
        self.is_app_running = False

def main() -> None:
    screen = MainScreen(run_app_func=lambda: None)
    app = VoiceAssistantApp(screen)
    screen.run_app_func = app.run
    assistant_actions.screen = screen
    screen.start_window()

if __name__ == '__main__':
    main()