import configparser
import os
from dotenv import load_dotenv

from utils.reddit import RedditHandler

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
    