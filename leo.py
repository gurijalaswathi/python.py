import speech_recognition as sr
import pyttsx3
from datetime import datetime
import wikipedia
import webbrowser
from googleapiclient.discovery import build
import requests
import json
import warnings

warnings.filterwarnings("ignore")  # This will not display any warning in the cmd

api_key = 'AIzaSyDLXnvSP2Exf4JZAdDpT-WuCK4HLRGQiDc'  # google api key
youtube = build('youtube', 'v3', developerKey=api_key)  # accessing google youtube api v3

engine = pyttsx3.init('sapi5')  # Initializing the Microsoft voice engine
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[0].id)  # Selecting the voice


def speak(audio):
    """ This function is for audio"""
    engine.say(audio)
    engine.runAndWait()


def wish_me():
    """  This Function is used for wishing the person greeting oof the day based on
      what time it is.
      Input : it take hour from datetime now in 24 hour format
      Output: Speak out Greetings
      """
    hour = int(datetime.now().hour)
    if hour <= 12:
        print("Leo:\n\tGood morning")
        speak("Good morning")
    elif 12 < hour <= 18:
        print("Leo:\n\tGood Afternoon")
        speak("Good Afternoon")
    elif 18 < hour <= 24:
        print("Leo:\n\tGood Evening")
        speak("Good Evening")
    else:
        speak("You are not earth ")


def take_command(input_text):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak(input_text)
        r.pause_threshold = 1
        text = r.listen(source)

        try:
            recognised_text = r.recognize_google(text)
            print("User:")
            print("\t", recognised_text)
            speak(recognised_text)

        except sr.UnknownValueError or sr.RequestError:
            print("Leo:\n\tCan you Repeat please?")
            speak("Can you Repeat please?")
            return None
    return recognised_text


def wiki_search():
    print("Leo:\n\tWhat would like to search in wikipedia ? just say the topic that you want search ")
    search_text = take_command("What would like to search in wikipedia ? just say the topic that you want search ")
    if search_text is None:
        wiki_search()
    else:
        try:
            qurey = wikipedia.summary(search_text, sentences=2)

            speak("According to wikipedia")
            print("Leo:\n\tAccording to wikipedia", qurey)
            speak(qurey)
        except:
            print("Leo:\n\tThis is not a valid search")
            speak("This is not a valid search")
            wiki_search()


def youtube_search():
    print("Leo:\n\tWhat would you like to search in youtube ?")
    search_text = take_command("What would you like to search in youtube ?")
    if search_text is None:
        youtube_search()
    else:
        print("Leo:\n\tOpening youtube please wait")
        speak("Opening youtube please wait")
        webbrowser.open("https://www.youtube.com/results?search_query=" + search_text)


def google_search():
    print("Leo:\n\tWhat would you like to search on google?")
    search_text = take_command("What would you like to search on google?")
    if search_text is None:
        google_search()
    else:
        print("Leo:\n\tOpening google please wait")
        speak("Opening google please wait")
        webbrowser.open(
            "https://www.google.com/search?sxsrf=ALeKk03Fqt3NF54kl8uSLFa9vIcsisZ2vg%3A1606455271216&source=hp&ei=54_AX9TgCuiC4-EP-oW5oAk&q=" + search_text + "&oq=orange+fruit&gs_lcp=CgZwc3ktYWIQAzILCC4QsQMQyQMQkwIyBwgAEBQQhwIyBQgAELEDMgIIADIHCAAQFBCHAjICCAAyBQgAELEDMgIIADICCAAyAggAOgQIIxAnOgQIABBDOgUIABCRAjoLCC4QsQMQxwEQowI6DQguELEDEMcBEKMCEEM6BwgAELEDEENQoAVY4hhgnRpoAHAAeAGAAZAFiAGyD5IBBzAuOS41LTGYAQCgAQGqAQdnd3Mtd2l6&sclient=psy-ab&ved=0ahUKEwiU8KSegKLtAhVowTgGHfpCDpQQ4dUDCAc&uact=5")


def play_youtube():
    print("Leo:\n\tWhat video would like to play ? just say the name of video")
    query = take_command("What video would like to play ? just say the name of video")
    if query is None:
        print("Leo:\n\tNot a valid search")
        speak("Not a valid search")
        play_youtube()
    else:
        request = youtube.search().list(
            part="snippet",
            maxResults=1,
            q=query
        )
        response = request.execute()
        search_text = response['items'][0]['id']['videoId']
        webbrowser.open("https://www.youtube.com/watch?v=" + search_text)


def share_price():
    print("Leo:\n\tWhat is the name of the company ? just say the name")
    query = take_command("What is the name of the company ? just say the name")
    if query is None:
        share_price()
    else:
        url = (
                "https://financialmodelingprep.com/api/v3/search?query=" + query + "&limit=10&exchange=NASDAQ&apikey=674878522f196363484492950df596a9")
        response = requests.request("GET", url)
        a = json.loads(response.text)
        if a:
            symbol = a[0]['symbol']
            speak(f"Symbol is {symbol}")
            url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + a[0][
                'symbol'] + "&interval=5min&apikey=2AQZO0C0U4FWMEF3"

            response = requests.request("GET", url)

            a = json.loads(response.text)
            print(response.text)

            for x in a['Time Series (5min)']:
                for y in a['Time Series (5min)'][str(x)]:
                    speak(f"{y[3:]} at {float(a['Time Series (5min)'][str(x)][str(y)])}")

                break
        else:
            speak("Invalid company name")
            share_price()


def covid_data():
    url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"
    print("Leo:\n\tWhich country should I get details about ?")
    query = take_command("Which country should I get details about ?")
    if query == None:
        covid_data()
    else:
        querystring = {"country": query.title()}

        headers = {
            'x-rapidapi-key': "dbf3e507dfmshe181f5af81fe1b7p11ecf5jsna07124f3def4",
            'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        a = json.loads(response.text)
        print(response.text)
        print("Leo:")
        print(f"\tTotal number of recovered are {float(a['data']['recovered'])}")
        print(f"\tTotal number of deaths are {float(a['data']['deaths'])}")
        print(f"\tTotal number of confirmed cases are {float(a['data']['confirmed'])}")
        speak(f"Total number of recovered are {float(a['data']['recovered'])}")
        speak(f"Total number of deaths are {float(a['data']['deaths'])}")
        speak(f"Total number of confirmed cases are {float(a['data']['confirmed'])}")


if __name__ == '__main__':
    wish_me()
    while True:
        print("Leo:\n\tWhat are my commands ?")
        search_text = take_command("What are my commands ?")
        if search_text == None:
            pass
        elif 'wikipedia' in search_text.lower():
            wiki_search()
        elif 'play' in search_text.lower():
            play_youtube()
        elif 'youtube' in search_text.lower():
            youtube_search()
        elif 'google' in search_text.lower():
            google_search()

        elif 'share' in search_text.lower() or 'stock' in search_text.lower():
            share_price()
        elif 'covid' in search_text.lower() or 'covid19' in search_text.lower():
            covid_data()
        elif 'quit' in search_text.lower():
            exit(0)
        else:
            speak("Command is not recognized")
