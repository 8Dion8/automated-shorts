from configparser import ConfigParser
import praw

class RedditHandler:
    def __init__(self, config: ConfigParser, appClientID: str, appClientSecret: str, appUserAgent: str) -> None:
        self.CONFIGSECTION = 'reddit'
        self.appClientID = appClientID
        self.appClientSecret = appClientSecret
        self.appUserAgent = appUserAgent
        self.load_config(config)
    
    
    def load_config(self, config: ConfigParser) -> None:
        self.subreddit = config.get(self.CONFIGSECTION, 'SUBREDDIT')
        self.sortMethod = config.get(self.CONFIGSECTION, 'SORTMETHOD')
        self.contentToScrape = config.get('main', 'VIDEOTYPE').split(',')
        self.numPostsToScrape = int(config.get(self.CONFIGSECTION, 'NUMPOSTS'))
    
    def authenticateAPI(self) -> None:
        self.app = praw.Reddit(
            client_id = self.appClientID,
            client_secret = self.appClientSecret,
            user_agent = self.appUserAgent
        )
    
    def scrapeSubreddit(self) -> list:
        scrapedContent = []
        
        match self.sortMethod:
            case 'top_all':
                posts = self.app.subreddit(self.subreddit).top(limit=self.numPostsToScrape)
            case 'hot':
                posts = self.app.subreddit(self.subreddit).hot(limit=self.numPostsToScrape)
            case default:
                posts = self.app.subreddit(self.subreddit).hot(limit=self.numPostsToScrape)
                
        for post in posts:
            scrapedObj = {}
            if 'title' in self.contentToScrape:
                scrapedObj['title'] = post.title
                
            if 'body' in self.contentToScrape:
                scrapedObj['body'] = post.selftext
                
            if 'topcomment' in self.contentToScrape:
                scrapedObj['topcomment'] = post.comments[0].body
            scrapedContent.append(scrapedObj)
        
        return scrapedContent
    
            