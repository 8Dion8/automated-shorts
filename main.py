import configparser
import os
from dotenv import load_dotenv

from utils.reddit import RedditHandler
from utils.speech import SpeechHandler
from utils.transcription import TranscriptionHandler
from utils.producer import Producer

if __name__ == '__main__':
    load_dotenv()
    redditClientID = os.getenv("REDDITCLIENTID")
    redditClientSecret = os.getenv("REDDITCLIENTSECRET")
    redditUserAgent = os.getenv("REDDITUSERAGENT")
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    redditHandler = RedditHandler(config, redditClientID, redditClientSecret, redditUserAgent)
    
    redditHandler.authenticateAPI()
    scraped = redditHandler.scrapeSubreddit()
    print(scraped)
    
    transcriptionHandler = TranscriptionHandler(config)
    transcriptionHandler.init_model()
    
    speechHandler = SpeechHandler(config, os.getenv('ELEVENLABSTOKEN'))
    speechHandler.init_client()
    
    producer = Producer(config)
    
    
    for post in scraped:
        
        speechHandler.generate_speech(
            post['title'],
            post['id'] + '_title',
            0
        )
        speechHandler.generate_speech(
            post['topcomment'],
            post['id'] + '_topcomment',
            1
        )
    
        titleSegments = transcriptionHandler.transcribe_audio(f'media/{post["id"]}_title.wav')
        commentSegments = transcriptionHandler.transcribe_audio(f'media/{post["id"]}_topcomment.wav')
        
    
        producer.make_short(post['id'], titleSegments, commentSegments)
    
        
    