#these imports are for text to speach and speach to text
import pyttsx3
import speech_recognition as sr

from _datetime import datetime
import webbrowser
import wikipedia
# these imports are for opening app and closing app
import os
import subprocess
import psutil
import signal
#for email sending through gmail
import smtplib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voice',voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.now().hour)
    if (hour>0 and hour <12):
        speak("Good Morning!")
    elif (hour>12 and hour <18):
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I am Jarvis Sir. Please tell me how may i help you")

def takeCommand():
    '''It takes microphone input from the user and return string output'''
    r =sr.Recognizer()
    with sr.Microphone() as source:
        # r.adjust_for_ambient_noise(source)
        print("Listening....")
        r.pause_threshold=1 #person can stop speaking and take a pause of 2 sec
        r.energy_threshold=100
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query= r.recognize_google(audio,language='en-in')
        print(f"User said: {query}\n ")
        speak(query)

    except Exception as e:
        print(e)
        print("Say that again please....")
        return "None"

    return query

# def takeCommand():
#     listen = False
#     r = sr.Recognizer()
#     while True:
#         while listen==False:
#             with sr.Microphone() as source:
#                 audio = r.listen(source)
#
#             try:
#                 query=r.recognize_google(audio, language='en-in')
#                 if (query == "start"):
#                     listen = True
#                     print(f"User said: {query}\n ")
#                     speak(query)
#                     print("Listening...")
#                     break
#                 else:
#                     continue
#             except LookupError:
#                 continue
#
#         while listen == True:
#             with sr.Microphone() as source:
#                 audio = r.listen(source)
#             print("1")
#             try:
#                 print("2")
#                 query = r.recognize_google(audio, language='en-in')
#                 if (query == "stop"):
#                     listen = False
#                     print("Listening stopped. Goodnight")
#                     break
#                 else:
#                     print("You saiddd " + query)
#                     return query
#             except LookupError:
#                 engine.say('Audio cannot be read!')
#                 engine.runAndWait()
#                 print("Could not understand audio")

def sendEmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('aliraza16aliraza@gmail.com','3520268038647')
    server.sendmail('aliraza16aliraza@gmail.com',to,content)
    server.close()

def action():
    shell_process = "global"
    while True:
        query= takeCommand().lower()
        # logic for executing tasks based on query
        if 'open google' in query:
            webbrowser.open("google.com")

        elif 'wikipedia' in query:
            speak("searching wikipedia...")
            query=query.replace('wikipedia','')
            results=wikipedia.summary(query,sentences=2)
            speak('according to wikipedia')
            speak(results)

        elif 'the time' in query:
            strTime=datetime.now().strftime('%H:%M:%S')
            speak(f"Sir, the time is {strTime}")

        elif 'open sublime text' in query:
            codePath="C:\\Program Files (x86)\\Sublime Text 3\\sublime_text.exe"
            # os.startfile(codePath)
            #you have an alternative way of opening a file via a shell:
            shell_process = subprocess.Popen([codePath], shell=True)
            print(shell_process.pid)

        elif 'close sublime text' in query:
            #Returned pid is the pid of the parent shell, not of your process itself. Killing it won't be sufficient - it will only kill a shell, not the child process. We need to get to the child:
            parent = psutil.Process(shell_process.pid)
            children = parent.children(recursive=True)
            print(children)
            child_pid = children[0].pid
            print(child_pid)
            #This is the pid you want to close. Now we can terminate the process:
            os.kill(child_pid, signal.SIGTERM)

        elif 'email to ahmed' in query:
            try:
                speak('what should i say')
                content=takeCommand()
                to='muhammadahmadazhar16@gmail.com'
                sendEmail(to, content)
                speak('email has been sent')
            except Exception as e:
                print(e)
                speak('sorry, i am not able to send this email')

if __name__ == '__main__':
    # speak("Amjad is a good boy")
    # wishMe()
    action()
