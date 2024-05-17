import whisper_timestamped as whisper
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
        self.model = whisper.load_model("base")
    
    def transcribe_audio(self, audioPath):
        audio = whisper.load_audio(audioPath)

        results = whisper.transcribe(self.model, audio, task='transcribe', language='en')
        
        return results['segments']
        
        
