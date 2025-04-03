import listen as listen
import components.speak as speak
import assistant_actions
import sys

tries: int = 0
is_app_running = True

def startApplication() -> None:
    print("Starting")

    while is_app_running:
        try:
            listenToVoiceInput() #Listen to user voice input
        except Exception as e:
            handleError(e) #Handle an error

        if tries >= 3:
            quitApp()

    print("app finished")


def listenToVoiceInput():
    text: str = listen.listen() #Listen to user voice
    if "python" in text or "peyton" in text:
        handleGreeting(text) 

    elif text == "None":
        handleNoInputDetected()

    elif text == "over" or text == "finish" or text == "exit":
        handleAppExit()

    else:
        handleUnknownWord(text)
        
def handleGreeting(text:str):
        print("Hi ,I'm python")
        speak.speak("Hi , I'm python")
        # endregion

        assistant_actions.start_comments(text)
        # region end greeting
        print("thanks for using python, good by :)")
        speak.speak("thanks for using python, good by")
        
        is_app_running = False


def handleAppExit():
    # region end greeting
        print("you exited, thanks for using python, good bye :)")
        speak.speak("you exited, thanks for using python, good bye")
        # endregion
        sys.exit()
        is_app_running = False


def handleNoInputDetected():
    print("I cant hear anything")
    speak.speak("I cant hear anything\n")
    tries += 1

def handleUnknownWord(text):
    print(f"got this: {text}, try a different word")
    speak.speak("try a different word")

def handleError(error:Exception):
    print("you got an error, try again" + str(error))
    speak.speak("You got an error, try again")

def quitApp():
    print("quiting")
    speak.speak("quiting")
    is_app_running = False


def main() -> None:
    #TODO remove the comment when UI is done
    """screen = window.MainScreen(run_app_func=startApplication)
    target=screen.start_window()"""

    startApplication()

if __name__ == '__main__':
    main()
