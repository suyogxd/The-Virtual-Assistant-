from flask import Flask,render_template,redirect,request
import warnings
warnings.filterwarnings('ignore')
import speech_recognition as sr
import pyttsx3
from playsound import playsound
import datetime
import pyjokes
import imaplib
import email
import os
import requests
from bs4 import BeautifulSoup
from email.message import EmailMessage
import webbrowser
from pytube import Search
import openai
openai.api_key = "Your OpenAI API Key"
model_engine = "text-davinci-003"
sound_file = "ambient_sound.mp3"
sound_path = os.path.join("D:\\", "final", sound_file)
listener = sr.Recognizer()

app = Flask("__name__")
assistant_name = "Mona"
conversation = []

def engine_talk(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty('voice', voices[6].id)
    engine.say(text)
    engine.runAndWait()
   
def user_commands():
    command=''
    try:
        with sr.Microphone() as source:
            print("LISTENING...")
            playsound(sound_path)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            if 'mona' in command:
                command = command.lower()
                command = command.replace('mona', '') 
    except:
        pass
    return command

def read_email_from_gmail():
    show=''
    say=''
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login("Your Email", "your password")
    mail.select("[Gmail]/Starred")

    result, data = mail.search(None, "ALL")
    latest_email_id = data[0].split()[-1]

    result, data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = data[0][1].decode("utf-8")
    email_message = email.message_from_string(raw_email)
    
    show =  'MONA: '
    print(show)
    conversation.append(show)
    
    show = f"Subject: {email_message['subject']}"
    print(show)
    engine_talk(show)
    conversation.append(show)

    show= f"From: {email_message['from']}"
    print(show)
    engine_talk(show)
    conversation.append(show)

    show=f"To: {email_message['to']}"
    print(show)
    engine_talk(show)
    conversation.append(show)

    for part in email_message.walk():
        if part.get_content_type() == 'text/plain':
            show= f"Message: {part.get_payload(decode=True).decode('utf-8')}"
            print(show)
            engine_talk(part.get_payload(decode=True).decode('utf-8'))  
            conversation.append(show)  

def get_weather(location):
    show=''
    say=''
    URL = f"https://www.weather-forecast.com/locations/{location}/forecasts/latest"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    weather_section = soup.find("span", attrs={"class": "phrase"})
    weather = weather_section.text
    weather = weather_section.text
    show = f"MONA: The Weather in {location} is: {weather}"
    print(show)
    conversation.append(show)
    say =f" The Weather in {location} is: {weather}"
    engine_talk(say)

def searchYoutube(query):
    search_results = Search(query).results
    if len(search_results) > 0:
        first_result = search_results[0]
        search_url = f"https://www.youtube.com/results?search_query={first_result.title}"
        webbrowser.open(search_url)
    else:
        engine_talk("Invalid command. Please try again.") 

def chitchat(prompt):
    show=''
    try:
        if not prompt:
            show = 'MONA: SORRY I CAN\'T HEAR YOU'
            say = 'SORRY I CAN\'T HEAR YOU'
            print(show)
            conversation.append(show)
            engine_talk(say)
        else:
            completion = openai.Completion.create(
                    engine=model_engine,
                    prompt=prompt,
                    max_tokens=1024,
                    n=1,
                    stop=None,
                    temperature=0.5,
                    )
            response = completion.choices[0].text
            show = f'MONA: {response}'
            print(show)
            conversation.append(show)
            engine_talk(f'{response}')
            if 'bye' in response:
                exit()
    except Exception as e:
        print(f"Error occurred: {str(e)}")   

def run_mona():
    global conversation
    say=''
    show=''
    command = user_commands()
    user=(f'YOU: {command}')
    print(user)
    conversation.append(user)
    if 'hello' in command:
        say = f'Hello there! How can i help you?'
        show = f'MONA: Hello there! How can i help you?'
        print(show)
        engine_talk(say)
        conversation.append(show)
    elif 'your name' in command:
        say = f'My name is {assistant_name}, your virtual assistant. How may I assist you?'
        show = f'MONA: My name is {assistant_name}, your virtual assistant. How may I assist you?'
        print(show)
        engine_talk(say)
        conversation.append(show)
    elif 'your age' in command:
        say = f'I am not a physical being and therefore do not have an age. However, I am always learning and growing.'
        show = f'MONA: I am not a physical being and therefore do not have an age. However, I am always learning and growing.'
        print(show)
        engine_talk(say)
        conversation.append(show)
    elif 'how old are you' in command:
        say = f'I am not a physical being and therefore do not have an age. However, I am always learning and growing.'
        show = f'MONA: I am not a physical being and therefore do not have an age. However, I am always learning and growing.'
        print(show)
        engine_talk(say)
        conversation.append(show)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        say = f'Current Time is {time}'
        show = f'MONA: Current Time is {time}'
        print(show)
        engine_talk(say)
        conversation.append(show)
    elif 'date' in command:
        date = datetime.datetime.now().strftime('%A, %B %d, %Y')
        say = f'Today is {date}'
        show = f'MONA: Today is {date}'
        print(show)
        engine_talk(say)
        conversation.append(show)
    elif 'joke' in command:
        get_j = pyjokes.get_joke()
        say = f'Here\'s a joke for you: {get_j}'
        show = f'MONA: Here\'s a joke for you: {get_j}'
        print(show)
        engine_talk(say)
        conversation.append(show)
    elif 'email' in command:
        read_email_from_gmail()
    elif 'weather' in command:
        if 'in' in command or 'of' in command:
            if 'in' in command:
                location = command[command.index('in') + 3:].strip() 
            elif 'of' in command:
                location = command[command.index('of') + 3:].strip() 
        else:
            show = "MONA: Weather of?"
            print(show)
            conversation.append(show)
            say = "Weather of?"
            engine_talk(say)
            weathercommand = user_commands()
            if "weather" in weathercommand:
                if 'in' in weathercommand:
                    location = weathercommand[weathercommand.index('in') + 3:].strip() 
                elif 'of' in command:
                    location = weathercommand[weathercommand.index('of') + 3:].strip() 
            else:
                location = weathercommand       
        show = f'MONA: Finding the weather of {location}'
        print(show)
        conversation.append(show)
        say = f'Finding the weather of {location}'
        engine_talk(say)
        get_weather(location) 
    elif 'search' in command and 'YouTube' in command:
        query = command[7:command.index('in')].strip()
        show = f'MONA: Searching for {query}'
        print(show)
        conversation.append(show)
        engine_talk('Searching for ' + query)
        searchYoutube(query)  
    # elif 'bye' in command:
    #     engine_talk('Have a good day')
    #     print(say)
    #     exit()
    else:
        prompt = command
        chitchat(prompt)

@app.route('/')
def hello():
    return render_template("mona.html")

@app.route("/home")
def home():
    return redirect('/')

@app.route('/',methods=['POST', 'GET'])
def submit():
    global conversation
    while True:
        run_mona()
        return render_template("mona.html", conversation=conversation)
       
if __name__ =="__main__":
    app.run(debug=True)