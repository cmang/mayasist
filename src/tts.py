# TTS library for Mayasist

import pyttsx3

class MayaTTS():

    def __init__(self):
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 175)     # setting up new voice rate
        rate = self.tts.getProperty('rate')   # getting details of current speaking rate
        print(rate)                        #printing current voice rate
        self.voices = self.tts.getProperty('voices')
        voice_count = len(self.voices)
        print(f"Available voices: {voice_count}")
        i = 0
        for voice in self.voices:
            print(f"num: {i}, id: {voice.id}")
            i += 1
        self.set_voice_num = 0

    def setVoiceNum(self, voice_num):
        self.tts.setProperty('voice', self.voices[voice_num].id)
        self.set_voice_num = voice_num

    def getVoiceName(self):
        return self.voices[self.set_voice_num].id

    def say(self, text):
        self.tts.say(text)
        # this SHOULD pause.. does in macos, doesn't in Linux?
        # Instead it seems to run in the backround.
        self.tts.runAndWait()


    def runAndWait(self):
        print("runAndWait() was run in tts.py. This shouldn't happen. :)")

    def stop(self):
        pass
