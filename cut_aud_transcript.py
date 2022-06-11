# importing libraries
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from translate import Translator

# create a speech recognition object
r = sr.Recognizer()

# a function that splits the audio file into chunks
# and applies speech recognition
transcript = []


def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 200 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
                              min_silence_len=100,
                              silence_thresh=sound.dBFS-14,
                              keep_silence=500,
                              )
    folder_name = "wavs"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                pass
            else:
                text = f"{text.capitalize()}. "
                with open('textfile.txt', 'w') as f:
                    for _ in transcript:
                        f.write(whole_text)
                transcript.append(text)
                whole_text += text + '\n'
    # return the text for all chunks detected
    return whole_text


get_large_audio_transcription(
    '/home/rishi/Documents/Rishi/ineuron_hackathon_ps1/test_fin.wav')

translated_text = []

language = input("Enter the language to translate to: ")

if language == 'fr':
    translate_text_french = Translator(from_lang='en', to_lang='fr')
    for i in transcript:
        translated_text.append(translate_text_french.translate(i))

    with open('translated_textfile.txt', 'w') as f:
        for i in translated_text:
            f.write(i + '\n')

elif language == 'es':
    translate_text_spanish = Translator(from_lang='en', to_lang='es')
    for i in transcript:
        translated_text.append(translate_text_spanish.translate(i))

    with open('translated_textfile.txt', 'w') as f:
        for i in translated_text:
            f.write(i + '\n')
else:
    pass
