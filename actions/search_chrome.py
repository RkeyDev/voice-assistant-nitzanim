import components.speak as speak
import listen
import subprocess


def search_chrome() -> None:
    # asking for search
    print("What to search ?")
    speak.speak("What to search ?")
    search: str = listen.listen()  # listening for what to search

    url = f"https://www.google.com/search?q={search.replace(' ', '+')}"  # creating url from speech

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    profile_name = "Default"

    subprocess.run([chrome_path, f"--profile-directory={profile_name}", "--new-window", url])  # searching google
