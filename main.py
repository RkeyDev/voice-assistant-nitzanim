import listen as listen
import components.speak as speak
import assistant_actions
import components.eye_tracker as eye_tracker
import threading

def main() -> None:
    print("start")
    print("starting eye tracker")
    threading.Thread(target=eye_tracker.run_eye_tracker).start() #Starting eye tracker

    trys: int = 0
    while True:
        try:
            text: str = listen.listen()
            if "python" in text or "peyton" in text:
                # region start greeting
                print("Hi ,I'm python")
                speak.speak("Hi , I'm python")
                # endregion
                assistant_actions.start_comments(text)
                # region end greeting
                print("thanks for using python, good by :)")
                speak.speak("thanks for using python, good by")
                # endregion
                break

            elif text == "None":
                print("I cant hear anything")
                speak.speak("I cant hear anything\n")
                trys += 1

            elif text == "over" or text == "finish" or text == "exit":
                # region end greeting
                print("you exited, thanks for using python, good by :)")
                speak.speak("you exited, thanks for using python, good by")
                # endregion
                break

            else:
                print(f"got this: {text}, try a different word")
                speak.speak("try a different word")

        except Exception as e:
            print("you got an error, try again" + str(e))
            speak.speak("You got an error, try again")

        if trys >= 3:
            print("quiting")
            speak.speak("quiting")
            break

    print("finish")


if __name__ == '__main__':
    main()
