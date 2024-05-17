from elevenlabs.client import ElevenLabs
from elevenlabs import save
from configparser import ConfigParser
import os

class SpeechHandler():
    def __init__(self, config: ConfigParser, APIKey: str) -> None:
        self.CONFIGSECTION = 'speech'
        self.load_config(config)
        self.APIKey = APIKey
    
    def load_config(self, config: ConfigParser) -> None:
        self.voices = config.get(self.CONFIGSECTION, 'VOICE').split(',')
        self.model = config.get(self.CONFIGSECTION, 'MODEL')
        self.savePath = config.get('main', 'MEDIAPATH')
        
    def init_client(self):
        self.client = ElevenLabs(api_key = self.APIKey)
        
    def generate_speech(self, text: str, fileID: str, voiceNum: int) -> str:
        audio = self.client.generate(
            text = text,
            voice = self.voices[voiceNum],
            model = self.model
        )
        pathToAudio = os.path.join(self.savePath, fileID + '.mp4')
        save(audio, pathToAudio)
        return pathToAudio