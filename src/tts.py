# TTS library for Mayasist

import pyttsx3

class MayaTTS():

    def __init__(self):
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 175)     # setting up new voice rate
        rate = self.tts.getProperty('rate')   # getting details of current speaking rate
        print(rate)                        #printing current voice rate
        voices = self.tts.getProperty('voices')
        number_of_voices = len(voices)
        print(f"Available voices: {number_of_voices}")
        i = 0
        for voice in voices:
            print(f"num: {i}, id: {voice.id}")
            i += 1


    def say(self, text):
        self.tts.say(text)
        # this SHOULD pause.. does in macos, doesn't in Linux?
        # Instead it seems to run in the backround.
        self.tts.runAndWait()


    def runAndWait(self):
        print("runAndWait() was run in tts.py. This shouldn't happen. :)")

    def stop(self):
        pass
