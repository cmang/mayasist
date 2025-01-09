import pyaudio
import wave

class SoundEngine():
    def __init__(self):
        # Initialize PyAudio
        self.p = pyaudio.PyAudio()
        self.beep_filename = 'beep.wav'
        self.hibeep_filename = 'hibeep.wav'
        self.boop_filename = 'boop.wav'

    def beep(self):
        self.play_sound(self.beep_filename)

    def hibeep(self):
        self.play_sound(self.hibeep_filename)
        
    def boop(self):
        self.play_sound(self.boop_filename)

    def play_sound(self, filename):
        # Defines a chunk size of 1024 samples per data frame.
        chunk = 1024 
        # Open sound file  in read binary form.
        file = wave.open(filename, 'rb')
        # Creates a Stream to which the wav file is written to.
        # Setting output to "True" makes the sound be "played" rather than recorded
        stream = self.p.open(format = self.p.get_format_from_width(file.getsampwidth()),
                        channels = file.getnchannels(),
                        rate = file.getframerate(),
                        output = True)
        # Read data in chunks
        data = file.readframes(chunk)
        # Play the sound by writing the audio data to the stream
        #while data != '':
        while data:
            stream.write(data)
            data = file.readframes(chunk)
        # Stop, Close and terminate the stream
        stream.stop_stream()
        stream.close()

        
        #self.p.terminate()

def list_of_voice_names(voices):
    names = []
    for voice in voices:                                                                                    names += voice.id
    return names

