#!/usr/bin/env python3

import os
import re
import pyttsx3

from openai import OpenAI
import speech_recognition as sr

import sounds

def clean_text(text):
    """ Take a string and remove punctation, trailing and leading sapces """
    #text = re.sub(r'[\W]', '', text).lower()
    #text = re.sub(r'{P}', '', text).lower()
    punct = re.compile(r'(\w+)')
    tokenized = [m.group() for m in punct.finditer(text)]
    text = ' '.join(tokenized).lower()
    return text

def list_of_voice_names(voices):
    names = []
    for voice in voices:
        names += voice.id
    return names

def audio_to_text(audio):
    r = sr.Recognizer()
    enabled_listen_engines = [
                        #'google',
                        #'sphinx',
                        'whisper',
                      ]
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
            if read_text != '':
                print(f"User: {read_text}")
        except sr.UnknownValueError:
            print("Whisper could not understand audio")
        except sr.RequestError as e:
            print("Whispher error; {0}".format(e))
    return read_text

def main():
    # init tts engine
    print("Initializing text to speech engine...")
    tts = pyttsx3.init()
    tts.setProperty('rate', 175)     # setting up new voice rate
    rate = tts.getProperty('rate')   # getting details of current speaking rate
    print(rate)                        #printing current voice rate
    voices = tts.getProperty('voices')
    number_of_voices = len(voices)
    print(f"Available voices: {number_of_voices}")

    i = 0
    for voice in voices:
        print(f"num: {i}, id: {voice.id}")
        i += 1

    #voice_names_list = list_of_voice_names(voices)
    #print(f"Full list of voices: {voice_names_list}")
    #tts.setProperty('voice', voices[179].id)
    voice = tts.getProperty('voice')
    print(f"Current voice: {voice}")

    # init sounds for beeps and boops
    print("Initializing sound playback engine..")
    sound = sounds.SoundEngine()

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
    context = "You are helpful, wise, and chill. Cool, useful, and scathingly cynical. Not too enthusiastic. Do not hallucinate. Nevertheless, be aware that you do hallucinate, and should always be double-checked for accuracy."
    triggers = [
                "hello computer",
                "hey computer",
                "yo computer",
                "okay computer",
                ]

    # runtime state
    listening = True
    triggered = False

    print("Adjusting for ambient noise...")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

    print('Active Triggers:')
    for trigname in triggers:
        print(f'  {trigname}')
    print('')
    print("Listening...")
    print('')
    tts.say("I'm listening. Say Hey Computer to trigger me.")
    tts.runAndWait()

    while listening:
        while not triggered:
            with sr.Microphone() as source:
                #r.pause_threshold = 1
                audio = r.listen(source)
                #print("Done listening. Processing...")


            read_text = audio_to_text(audio)
            text = clean_text(read_text)

            #print(f"cleaned: {text}")

            if text in triggers:
                print('')
                print("Triggered!!!")
                print('')
                triggered = True

        if triggered:
            # Beep here (high pitch, listening sound)
            sound.beep()

            print("Ask ChatGPT a question!")
            print('')

            # Triggered, so listen for prompt.
            with sr.Microphone() as source:
                #r.pause_threshold = 1
                audio = r.listen(source)
                read_text = audio_to_text(audio)
                sound.hibeep()

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
            clean_message = clean_text(prompt)

            # Custom commands
            if clean_message == 'nevermind' or clean_message == 'never mind':
                triggered = False
                sound.boop()
            elif clean_message == 'quit':
                listening = False
                triggered = False
                break
            elif clean_message == 'reset voice':
                tts = pyttsx3.init()
                tts.setProperty('rate', 175)     # setting up new voice rate
                message = "Done. The voice has been reset."
                tts.say(message)
                tts.runAndWait()
                message = None
            elif clean_message == 'set voice number' or \
                    clean_message == 'set voice':
                message = "Which voice number do you want to set? Minimum is 0, Maximum is "
                max_num = len(voices)
                message += str(max_num)
                tts.say(message)
                tts.runAndWait()
                # get number from user
                sound.beep()
                with sr.Microphone() as source:
                    #r.pause_threshold = 1
                    audio = r.listen(source)
                user_response = clean_text(audio_to_text(audio))
                sound.hibeep()
                if user_response == "zero":
                    user_response = "0"
                print(f"User: {user_response}")
                if user_response.isdigit():
                    # it's a number, see if it's valid
                    num = int(user_response)
                    if num >= 0 and num <= max_num:
                        # Valid voice number. set it.
                        tts.setProperty('voice', voices[num].id)
                        message = f"Done! The voice has been set to voice {num}."
                        tts.say(message)
                        tts.runAndWait()
                        message = None
                    else:
                        sound.boop()
                        message = f"Sorry. {num} is not valid. The voice number must be between 0 and {max_num}."
                        tts.say(message)
                        tts.runAndWait()
                        message = None
                else:
                    sound.boop()
                    message = f"Sorry, I didn't understand. The voice number must be between 0 and {max_num}."
                    tts.say(message)
                    tts.runAndWait()
                    message = None
            elif message:
                print("Thinking...", end='')
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
                    #model="gpt-4o",
                    model="gpt-4o-mini",
                )
                reply = chat_completion.choices[0].message.content
                print('')
                print(f"Chat GPT: {reply}")
                print('')  # blank line

                # Speak chatGPT's reply out loud
                tts.say(reply)
                tts.runAndWait()
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
