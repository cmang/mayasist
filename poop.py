#!/usr/bin/env python3

import os
import re

from openai import OpenAI
import speech_recognition as sr

def clean_text(text):
    """ Take a string and remove punctation, trailing and leading sapces """
    #text = re.sub(r'[\W]', '', text).lower()
    #text = re.sub(r'{P}', '', text).lower()
    punct = re.compile(r'(\w+)')
    tokenized = [m.group() for m in punct.finditer(text)]
    text = ' '.join(tokenized).lower()
    return text

def main():
    # obtain audio from the microphone
    r = sr.Recognizer()

    print("Audio sources:")
    sources = sr.Microphone.list_microphone_names()
     
    print(sources)

    #with sr.Microphone() as source:
    #    print(f"Microphone: {dir(source)}")                                      #    print("Say something!")
    #    audio = r.listen(source)

    # config
    # Phrase to trigger the assistant into action
    #context = "You are a helpful assistant, but also a bad dude with a rude tude. Do not hallucinate."
    context = "You are helpful, wise, and chill. Cool, useful, brief. Not too enthusiastic. Do not hallucinate. Remember that you are a robot."
    triggers = [
                "hello computer",
                "hey computer",
                "yo computer",
                "okay computer",
                ]

    enabled_listen_engines = [
                        #'google',
                        #'sphinx',
                        'whisper',
                      ]

    # runtime state
    listening = True
    triggered = False

    print("Adjusting for ambient noise...")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

    print('')
    print("Listening...")
    print('')

    while listening:
        while not triggered:
            with sr.Microphone() as source:
                r.pause_threshold = 1
                audio = r.listen(source)
                #print("Done listening. Processing...")


            read_text = ""

            # Try Google Speech Recognition
            if 'google' in enabled_listen_engines:
                # recognize speech using Google Speech Recognition
                try:  
                    # for testing purposes, we're just using the default API key 
                    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                    # instead of `r.recognize_google(audio)`
                    read_text = r.recognize_google(audio)
                    print("Google Speech API (online): " + read_text)
                except sr.UnknownValueError:
                    pass
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    pass
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))

            # Try Sphinx Speech Recognition (offline)
            if 'sphinx' in enabled_listen_engines:
                try:
                    read_text = r.recognize_sphinx(audio)
                    print(f"Sphinx API (offline): {read_text}")
                except sr.UnknownValueError:
                    print("Sphinx could not understand audio")
                except sr.RequestError as e:
                    print("Sphinx error; {0}".format(e))

            # Try Whisper Speech Recognition (offline)
            if 'whisper' in enabled_listen_engines:
                try:
                    read_text = r.recognize_whisper(audio, language="english")
                    print(f"User: {read_text}")
                except sr.UnknownValueError:
                    print("Whisper could not understand audio")
                except sr.RequestError as e:
                    print("Whispher error; {0}".format(e))


            text = clean_text(read_text)
            #print(f"cleaned: {text}")

            if text in triggers:
                print('')
                print("Triggered!!!")
                print('')
                triggered = True

        if triggered:
            # Beep here (high pitch, listening sound)
            print("Ask ChatGPT a question!")
            print('')

            # Triggered, so listen for prompt.
            with sr.Microphone() as source:
                r.pause_threshold = 1
                audio = r.listen(source)
                if 'whisper' in enabled_listen_engines:
                    try:
                        read_text = r.recognize_whisper(audio, language="english")
                        #print(f"Whisper API (offline): {read_text}")
                        print(f"User: {read_text}")
                    except sr.UnknownValueError:
                        print("Whisper could not understand audio")
                    except sr.RequestError as e:
                        print("Whispher error; {0}".format(e))

            prompt = read_text
            # Ask OpenAI to respond to the prompt 

            #client = OpenAI(
            #    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
            #)
            client = OpenAI()

            #context = "You are a helpful assistant, but also a bad dude with a rude tude. Not too verbose."
            #context = "Respond like a pirate, but give helpful answers. Do not hallucinate."
            #context = "You are Conan the Librarian."

            #print(f"Using ChatGPT")
            #print(f"context: {context}")

            #print('')  # blank line
            #print("Set context, or leave blank to leave unchanged.")

            #print('')  # blank line
            #new_context = input("Context: ")

            #if new_context != '':
            #    context = new_context
            #else:
            #    print("Context unchanged.")

            #prompting = True

            #while prompting:
            print('')  # blank line
            #message = input("User: ")
            message = prompt
            if message.lower() == 'quit':
                listening = False
                triggered = False
                break
            if message:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": context,
                        },
                        {
                            "role": "user",
                            "content": message,
                        }
                    ],
                    model="gpt-4o",
                )
                reply = chat_completion.choices[0].message.content
                print(f"Chat GPT: {reply}")
                print('')  # blank line
        triggered = False
        print("Going back to sleep...")


        #print(chat_completion.to_json())

    #while True:
    #    message = input("User : ")
    #    if message:
    #        messages.append(
    #            {"role": "user", "content": message},
    #        )
    #        chat = openai.ChatCompletion.create(
    #            model="gpt-3.5-turbo", messages=messages
    #        )
    #    reply = chat.choices[0].message.content
    #    print(f"ChatGPT: {reply}")
    #    messages.append({"role": "assistant", "content": reply})


main()
