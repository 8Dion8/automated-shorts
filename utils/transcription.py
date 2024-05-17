from vosk import Model, KaldiRecognizer, SetLogLevel
import wave
import os
from configparser import ConfigParser
import subprocess

class TranscriptionHandler():
    def __init__(self, config: ConfigParser) -> None:
        self.CONFIGSECTION = 'transcription'
        self.load_config(config)
    
    def load_config(self, config: ConfigParser):
        self.modelPath = config.get(self.CONFIGSECTION, 'MODELPATH')
        
    def init_model(self): 
        self.model = Model(self.modelPath)
        self.recognizer = KaldiRecognizer(self.model, 16000)
    
    def convert_audio_for_vosk(self, audioPath):
        print(os.getcwd())
        audioPath = os.path.join(os.getcwd(), audioPath)
        subprocess.run(
            ['ffmpeg', '-i', audioPath, '-ar', '16000', '-ac', '1', '-acodec', 'pcm_s16le', audioPath+'.wav']
        )
    
    def transcribe_audio(self, audioPath):
        audio = wave.open(audioPath, 'r')
        if audio.getnchannels() != 1 or audio.getsampwidth() != 2 or audio.getcomptype() != "NONE":
            print("Audio file must be WAV format mono PCM. converting.")
            self.convert_audio_for_vosk(audioPath)
            audio = wave.open(audioPath+'.wav', 'r')
        
        audio_data = audio.readframes(audio.getnframes())
        if self.recognizer.AcceptWaveform(audio_data):
            print(self.recognizer.FinalResult())
        else:
            print(self.recognizer.Result())
        
