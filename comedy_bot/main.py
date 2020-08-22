
import random
from create_tweet import get_response
from api import *
from util import *
import config
import time

from PIL import Image
import requests
from io import BytesIO

api = tweet_api()

tweet_type = config.TWEET_TYPE


def format_tweet(response, tweet_choice, url=None):
    """
    Add url to response if needed
    :return: formatted response
    """

    if tweet_choice in ['retweet', 'headline']:
        response = response + '\n\n' + url

    return response


def save_img(url):
    """
    Save an image used in tweet
    :return: saved image filename
    """

    if url[-3:] == 'gif':
        filename = 'temp.gif'
    else:
        filename = 'temp.jpg'

    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

    return filename


def make_tweet(response, url, filename, tweet_choice):
    """
    Send tweets
    :return: None
    """

    if tweet_choice in ['retweet', 'headline']:
        api.update_status(status=response + "\n\n" + url)
    elif tweet_choice in ['gif', 'meme', 'image']:
        img_id = upload_media(filename, api)
        api.update_status(status=response, media_ids=[img_id])
    else:
        api.update_status(status=response)


def tweet_flow(tweet_choice, url, text):
    """
    Prepare tweet based on random choice
    :return: generated response and image filename
    """

    if tweet_choice in ['gif', 'meme', 'image']:
        filename = save_img(url)
    else:
        filename = ''

    if tweet_choice == 'trending':
        pre_response = get_response(text, trunc=False)
    else:
        pre_response = get_response(text)

    if tweet_choice in ['retweet', 'headline']:
        response = format_tweet(pre_response, tweet_choice, url)
    else:
        response = format_tweet(pre_response, tweet_choice)

    return response, filename


def main():
    """
    Main function for tweet generation
    :return: None
    """

    url = ''
    tweet_choice = random.choice(tweet_type)

    if tweet_choice == 'gif':
        url, text = get_gif()
    elif tweet_choice == 'retweet':
        user, tweet_id, text = get_tweet(api)
        url = f'https://twitter.com/{user}/status/{tweet_id}'
    elif tweet_choice == 'headline':
        url, text = get_headlines(image=False)
    elif tweet_choice == 'meme':
        url, text = get_meme()
    elif tweet_choice == 'image':
        url, text = get_headlines(image=True)
    else:
        text = get_trends(api)

    final_response, filename = tweet_flow(tweet_choice, url, text)

    make_tweet(final_response, url, filename, tweet_choice)


while True:

    main()

    # Choose random length to sleep before next tweet
    rand_length = random.randrange(1, 6)
    time.sleep(rand_length * 60 * 60)
