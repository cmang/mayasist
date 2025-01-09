Mayasist

An AI assistant. My assistant.

It doesn't do that much yet. It uses offline local speech to text and text to speech. It listens for trigger phrases "hey computer" and "yo computer," understands "nevermind," can "quit," "list commands," and "set voice." All other requests go to chatGPT.

Needs these things:

    OPENAI_API_KEY set

    pip install openai PyAudio SpeechRecognition PocketSphinx openai-whisper soundfile pyttsx3

pyttsx3 might need:

    apt install espeak ffmpeg libespeak1

portaudio:

    brew install portaudio

    or

    apt install portaudio19-dev


