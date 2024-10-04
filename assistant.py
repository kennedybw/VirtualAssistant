import speech_recognition as sr
import pyttsx3
import webbrowser
import random
import requests
import threading
import datetime
from dotenv import load_dotenv
import os
from googletrans import Translator
from assistant_gui import create_gui

# initialize recognizer and text-to=speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')

for voice in voices:
    if "great britain" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break


# function to convert speech to text
def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return None
        except sr.RequestError:
            print("API unavailable or error.")
            return None

# function to convert text to speech
def speak(text, speak_and_display_func):
    speak_and_display_func(text)
    engine.say(text)
    engine.runAndWait()


def calculate(expression, speak_and_display_func):
    try:
        result = eval(expression)
        speak(f"The result is {result}", speak_and_display_func)
    except Exception as e:
        speak("Sorry, I couldn't calculate that", speak_and_display_func)

def get_weather(city, speak_and_display_func):
    load_dotenv()
    api_key = os.getenv("WEATHER_API_KEY")
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
    response = requests.get(base_url)
    weather_data = response.json()

    if weather_data["cod"] != "404":
        main_weather = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        speak(f"The weather in {city} is currently {main_weather} with a temperature of {temperature} degrees Fahrenheit.", speak_and_display_func)
    else:
        speak(f"Sorry, I couldn't find the weather for {city}.", speak_and_display_func)


def translate_text(text, target_language, speak_and_display_func):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=target_language)
        speak(f"The translation in {target_language} is: {translation.text}", speak_and_display_func)
    except Exception as e:
        speak(f"Sorry, I could't translate that. Error: {e}", speak_and_display_func)

def search_google(query, speak_and_display_func):
    webbrowser.open(f"https://www.google.com/search?q={query}")
    speak(f"Searching for {query} on Google.", speak_and_display_func)

def fun_facts(speak_and_display_func):
    facts = [
        "Did you know? Honey never spoils.",
        "Fun fact: Octupuses have three hearts.",
        "Did you know? Bananas are berries, but strawberries are not."
        "A day on Venus is longer than a year on Venus.",
        "Did you know? A single strand of spaghetti is called a spaghetto.",
        "The Eiffel Tower can be 15 cm taller during the summer due to the expansion of metal in the heat.",
        "Fun fact: A group of flamingos is called a 'flamboyance.'",
        "Polar bears have black skin underneath their white fur.",
        "Did you know? There are more stars in the universe than grains of sand on Earth.",
        "Sharks existed before trees!",
        "The shortest war in history lasted 38 minutes.",
        "Fun fact: The word 'quiz' was invented as a bet in 1791 to see if a nonsensical word could become popular.",
        "Koalas sleep up to 22 hours a day.",
        "A bolt of lightning contains enough energy to toast 100,000 slices of bread."
    ]
    speak(random.choice(facts), speak_and_display_func)

def greet_user():
    user_name = "Kennedy"
    hour = datetime.datetime.now().hour

    if hour < 12:
        greeting = f"Good morning, {user_name}!"
    elif hour < 18:
        greeting = f"Good afternoon, {user_name}!"
    else:
        greeting = f"Good evening, {user_name}!"

    return greeting

def assistant_mood():
    moods = [
        "I'm feeling great today!",
        "A little tired, but I'm happy to assist!",
        "I'm full of energy! Ready to help.",
        "I'm feeling productive today."
    ]
    return random.choice(moods)

def daily_quote():
    quotes = [
        "Beleive in yourself and all that you are.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "Success is not final, failure is not fatal: It is courage to continue that counts."
    ]
    return random.choice(quotes)

def trivia_game(speak_and_display_func):
    trivia_questions = {
        "What is the capital of France?": "paris",
        "Who wrote 'Hamlet'?": "shakespeare",
        "What is the largest planet in our solar system?": "Jupiter"
    }

    question, answer = random.choice(list(trivia_questions.items()))
    speak(question, speak_and_display_func)
    user_answer = listen()

    if user_answer == answer:
        return "Correct!"
    else: 
        return f"Sorry, the correct answer is {answer}."



def assistant_loop(window,speak_and_display_func):
    
    greet_message = greet_user()
    speak(greet_message, speak_and_display_func)

    speak("How can I assist you?", speak_and_display_func)

    is_listening = True

    while is_listening:
        command = listen()
        if command:
            command = command.lower().strip()

            if "stop" in command:
                speak("Goodbye!", speak_and_display_func)
                is_listening = False
                window.quit()

            elif "hello" in command:
                speak("Hello! How are you today?", speak_and_display_func)
            
            elif "how are you" in command:
                mood_response = assistant_mood()
                speak(mood_response,speak_and_display_func)

            elif "open youtube" in command:
                speak("Opening Youtube", speak_and_display_func)
                webbrowser.open("https://www.youtube.com")

            elif "open google" in command:
                speak("Opening Google", speak_and_display_func)
                webbrowser.open("https://www.google.com")

            elif "tell me a joke" in command:
                jokes = [
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "Why was the math book sad? It had too many problems.",
                    "What do you get if you cross a cat with dark horse? Kitty Perry."
                ]
                joke = random.choice(jokes)
                speak(joke, speak_and_display_func)
            
            elif "calculate" in command:
                speak("Please say the expression", speak_and_display_func)
                expression = listen()
                if expression:
                    calculate(expression, speak_and_display_func)
            
            elif "weather" in command:
                speak("Which city would you like the weather for?", speak_and_display_func)
                city = listen()
                if city:
                    get_weather(city, speak_and_display_func)
            
            elif "translate" in command:
                speak("What would you like to translate?", speak_and_display_func)
                text_to_translate = listen()
                if text_to_translate:
                    speak("Which language should I translate it to?", speak_and_display_func)
                    target_language = listen().lower()
                    translate_text(text_to_translate, target_language, speak_and_display_func)
            
            elif "search" in command:
                speak("What would you like to search for?", speak_and_display_func)
                query = listen()
                if query:
                    search_google(query, speak_and_display_func)
            
            elif "fun fact" in command:
                fun_facts(speak_and_display_func)

            elif "motivate me" in command:
                quote = daily_quote()
                speak(quote, speak_and_display_func)
            
            elif "play trivia" in command:
                result = trivia_game(speak_and_display_func)
                speak(result, speak_and_display_func)

            else:
                speak("Sorry, I didn't understand that command.", speak_and_display_func)
    


# main function to listen and respond
def main():
    # create the gui window and get the speak_and_display function
    window, speak_and_display_func = create_gui("")

    # function to greet the user and start assistant loop
    def greet_and_start_assistant():
        assistant_loop(window, speak_and_display_func)

    # run the assistant loop in a separate thread to avoid blocking the GUI
    assistant_thread = threading.Thread(target=greet_and_start_assistant)
    assistant_thread.daemon = True # ensures the thread will exit when the program ends
    assistant_thread.start()

    # start the tkinter main event loop to keep the GUI responsive
    window.mainloop()

# main entry point of the program
if __name__ == "__main__":
    main()