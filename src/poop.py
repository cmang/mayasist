#!/usr/bin/env python3

import os
import re
import pyttsx3

from openai import OpenAI
#import speech_recognition as sr

import src.sounds as sounds
import src.lights as lights
import src.speech as speech

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

def main():
    # Init speech recognition
    print("Initializing speech recognition engine...")
    #r = sr.Recognizer()
    stt = speech.Recognizer()

    print("Audio sources:")
    sources = stt.list_audio_sources()
    print(sources)

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

    # Init lights "engine"
    light = lights.LightsX10()

    # init sounds for beeps and boops
    print("Initializing sound playback engine..")
    sound = sounds.SoundEngine()


    # config
    # Phrase to trigger the assistant into action
    #context = "You are a helpful assistant, but also a bad dude with a rude tude. Do not hallucinate."
    context = "You are helpful, wise, and chill. Cool, useful, and scathingly cynical. Not too enthusiastic. Do not hallucinate. Nevertheless, be aware that you do hallucinate, and should always be double-checked for accuracy."
    triggers = [
                "hello computer",
                "hey computer",
                "a computer",   # stupid fuzzy match for "hey computer"
                "yo computer",
                "okay computer",
                "hey stupid computer",
                "yo tupid computer",
                ]

    # runtime state
    listening = True
    triggered = False

    command_list = ['help', 'set voice', 'list voices', 'lights on', 'lights off', 'say', 'nevermind', 'exit']

    print("Adjusting for ambient noise...")
    stt.set_ambient_levels()

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
            # Listen for trigger word
            print("listening..")
            audio = stt.listen()
            print("listened..")

            read_text = stt.audio_to_text(audio)
            text = clean_text(read_text)

            #print(f"cleaned: {text}")

            #if text in triggers:
            if any(trig in text for trig in triggers):
                print('')
                print("Triggered!!!")
                print('')
                triggered = True

        if triggered:
            # Triggered, so listen for prompt.

            print("Give me a command or ssk ChatGPT a question.")
            print('')
            sound.beep()

            # wait a little longer (2) for this one. Thoughts may be rambling.
            audio = stt.listen(threshold = 2)

            read_text = stt.audio_to_text(audio)
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
            if 'nevermind' in clean_message or 'never mind' in clean_message:
                triggered = False
                sound.boop()
            elif clean_message == 'help' or clean_message == 'list commands':
                tts.say("The following commands are available.")
                tts.runAndWait()
                for command in command_list:
                    if command == command_list[-1]:
                        print(f"{command}")
                        tts.say(f"and {command}.")
                    else:
                        print(command)
                        tts.say(command)
                    tts.runAndWait()
                print('')
                triggered = False
            elif clean_message == 'quit' or \
                    clean_message == 'exit':
                listening = False
                triggered = False
                tts.say("Shutting down.")
                tts.runAndWait()
                break
            elif clean_message.startswith("say") or \
                    clean_message.startswith("repeat after me"):
                clean_message = clean_message.lstrip("say")
                clean_message = clean_message.lstrip("repeat after me")
                tts.say(clean_message)
                tts.runAndWait()
            elif "lights on" in clean_message or \
                    "turn on the light" in clean_message:
                tts.say("Turning on the lights.")
                tts.runAndWait()
                light.on()
            elif "lights off" in clean_message or \
                    "turn off the light" in clean_message:
                tts.say("Turning off the lights.")
                tts.runAndWait()
                light.off()
            #elif clean_message == 'reset voice':
            #    tts = pyttsx3.init()
            #    tts.setProperty('rate', 175)     # setting up new voice rate
            #    message = "Done. The voice has been reset."
            #    tts.say(message)
            #    tts.runAndWait()
            #    message = Nona
            elif 'list voices' in clean_message or \
                    'list the voices' in clean_message or \
                    'list of the voices' in clean_message or \
                    'list of all the voices' in clean_message:
                tts.say("Printing voice list to console.")
                tts.runAndWait()
                if len(voices) > 10:
                    tts.say("It may be long.")
                    tts.runAndWait()
                i = 0
                for voice in voices:
                    print(f"num: {i}, id: {voice.id}")
                    i += 1
            elif \
                    clean_message.startswith('set voice') or \
                    clean_message.startswith('change voice') or \
                    clean_message == 'said voice':
                message = "Which voice number do you want to set? Minimum is 0, Maximum is "
                max_num = len(voices)
                message += str(max_num)
                tts.say(message)
                tts.runAndWait()

                # get number from user
                sound.beep()
                audio = stt.listen()
                user_response = clean_text(audio_to_text(audio))
                sound.hibeep()

                if user_response == "zero":
                    user_response = "0"
                if user_response == "for":
                    user_response = "4"
                if user_response == "sex":
                    user_response = "6"
                if user_response == "ate":
                    user_response = "8"
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

if __name__ == "__main__":
    main()
