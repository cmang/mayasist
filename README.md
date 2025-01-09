Mayasist

An AI assistant. My assistant.

It doesn't do that much yet.

- Offline local speech to text and text to speech.
- Listens for trigger phrases (to be customizable):
  - "hey computer"
  - "hello computer"
  - "yo computer"
  - "hey stupid computer"
- Other commands:
  - "nevermind"
  -  "quit"
  -  "exit"
  -  "help"
  -  "list commands"
- "set voice" and "list voices" to change the voice on the fly
- All other requests go to chatGPT.

Needs these things:

    OPENAI_API_KEY set

    pip install openai PyAudio SpeechRecognition PocketSphinx openai-whisper soundfile pyttsx3

pyttsx3 might need:

    apt install espeak ffmpeg libespeak1

portaudio:

    brew install portaudio

    or

    apt install portaudio19-dev


