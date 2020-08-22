# Twitter Developer API keys and tokens
API_KEY = ""
API_SECRET = ""
ACCESS_TOKEN = ""
TOKEN_SECRET = ""

# API for News API service https://newsapi.org/
NEWSAPI = ""

# This seems to be a generic API key that works
GIPHY_API = "dc6zaTOxFJmzC"

# Include the screen names of the individual you will follow tweets for and then reply
RETWEET = [SCREEN_NAME]

# Words to add when responding to trending topics
ADD_WORDS = [' is', ' was', ' will', " won't", " can't", ' never', ' always']

# The possible tweet types
TWEET_TYPE = ['gif', 'retweet', 'headline', 'meme', 'trending', 'image']

# Dictionary of user screen name and tweet id
# Use tweepy to find the tweet id of each user
LISTEN = {SCREEN_NAME: USER_ID}
