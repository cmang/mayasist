# Speech recognition

import speech_recognition as sr

class Recognizer:

    def __init__(self):
        self.r = sr.Recognizer()
        self.listen_engines = [ \
                'google', \
                'sphinx', \
                'whisper', \
                'faster-whisper', \
                ]

        self.default_engine = 'faster-whisper'
        self.engine = self.default_engine

    def set_ambient_levels(self):
        """ Adjusting for ambient noise """
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)

    def list_audio_sources(self):
        """ Returns a list of mic/audio sources """
        return sr.Microphone.list_microphone_names()

    def listen(self, threshold = 1):
        with sr.Microphone() as source:
            self.r.pause_threshold = threshold
            audio = self.r.listen(source)
            return audio

    def audio_to_text(self, audio):
        # Try Google Speech Recognition
        if self.engine == 'google':
            # recognize speech using Google Speech Recognition (Cloud/Online!)
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                read_text = self.r.recognize_google(audio)
                print("Google Speech API (online): " + read_text)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

        # Try Sphinx Speech Recognition (offline)
        if self.engine == 'sphinx':
            try:
                read_text = self.r.recognize_sphinx(audio)
                print(f"Sphinx API (offline): {read_text}")
            except sr.UnknownValueError:
                print("Sphinx could not understand audio")
            except sr.RequestError as e:
                print("Sphinx error; {0}".format(e))

        # Try Faster Whisper Speech Recognition (offline)
        if self.engine == 'faster-whisper':
            try:
                read_text = self.r.recognize_whisper(audio, language="english")
                if read_text != '':
                    print(f"User: {read_text}")
            except sr.UnknownValueError:
                print("Whisper could not understand audio")
            except sr.RequestError as e:
                print("Whispher error; {0}".format(e))

        # Try Whisper Speech Recognition (offline)
        if self.engine == 'whisper':
            try:
                read_text = self.r.recognize_faster_whisper(audio, language="english")
                if read_text != '':
                    print(f"User: {read_text}")
            except sr.UnknownValueError:
                print("Whisper could not understand audio")
            except sr.RequestError as e:
                print("Whispher error; {0}".format(e))

        return read_text    
