"""File to handle various API connection

Separated into different functions
"""

import tweepy
import random
from tweepy import OAuthHandler
import urllib.request
import requests
import giphy_client
import json
from newsapi import NewsApiClient
import config


def tweet_api():
    """
    Connection from tweepy to twitter api
    :return: an api connection
    """
    ckey = config.API_KEY
    csecret = config.API_SECRET
    atoken = config.ACCESS_TOKEN
    asecret = config.TOKEN_SECRET

    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    return api


def get_tweet(api):
    """
    Gets a random tweet from a list of users
    :return: username, tweet id, tweet
    """
    rand_user = random.choice(config.RETWEET)

    tweets = tweepy.Cursor(api.user_timeline, screen_name=rand_user, timeout=999999, lang="en",
                           tweet_mode='extended', include_rts=False).items(1)

    for tw in tweets:
        data = tw._json
        tweet_id = data['id']
        text = data['full_text']
        user = data['user']['screen_name']

    return user, tweet_id, text


def upload_media(filename, api):
    """
    Uploads media to twitter
    :return: image id
    """
    media = api.media_upload(filename)

    img_id = media.media_id

    return img_id


def random_word():
    """
    Generate a random word to be used in creating the tweet
    :return: a random word
    """
    url = urllib.request.urlopen(
        "https://raw.githubusercontent.com/sindresorhus/mnemonic-words/master/words.json")
    words = json.loads(url.read())
    tag_word = random.choice(words)

    return tag_word


def get_gif():
    """
    Connect to Giphy and get a random gif
    :return: gif, tag word
    """
    api_instance = giphy_client.DefaultApi()
    api_key = config.GIPHY_API
    tag_word = random_word()

    api_response = api_instance.gifs_random_get(
        api_key, tag=tag_word, rating='g', fmt='json').to_dict()

    gif_url = api_response['data']['image_original_url']

    return gif_url, tag_word


def get_meme():
    """
    Get a random meme with a title
    :return: url and description
    """
    meme_api = "https://meme-api.herokuapp.com/gimme"
    r = requests.get(url=meme_api).json()

    url = r['url']
    text = r['title']

    return url, text


def get_trends(api):
    """
    Gather a random trending hashtag or topic
    :return: trending item
    """
    count = 0

    trends = api.trends_place(2442047)[0]['trends']

    word = random.choice(config.ADD_WORDS)

    while count == 0:

        rand_trend = random.choice(trends)

        if rand_trend['tweet_volume'] is not None and rand_trend['tweet_volume'] > 70000:
            count = 1

    return rand_trend['name']+word


def get_headlines(image=False):
    """
    Get random headline from US news sources
    :return: url and short description
    """
    newsapi = NewsApiClient(api_key=config.NEWSAPI)

    top_headlines = newsapi.get_top_headlines(language='en', country='us')

    article = random.choice(top_headlines['articles'])

    headline = article['description']

    if headline == '':
        headline = 'Nothing.'

    if image:
        url = article['urlToImage']
    else:
        url = article['url']

    return url, headline
