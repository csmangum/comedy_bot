
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy

from util import *
from create_tweet import get_response
import config

import time
import json

user = [l for l in config.LISTEN.keys()]
user_id = [l for l in config.LISTEN.values()]


def make_tweet(string, tweet_id, screen_name):
    """
    Send out tweet
    :return: None
    """
    api.update_status(status=f'@{screen_name} ' + string,
                      in_reply_to_status_id=tweet_id)


class listener(StreamListener):
    """
    Create ongoing listener for any tweets from specified user
    :return: listener
    """

    def on_data(self, data):

        res = json.loads(data)

        if res["user"]['screen_name'] in user:
            try:

                if data.split(',"text":"')[1][0:2] not in 'RT':
                    try:
                        tweet = res["extended_tweet"]["full_text"]
                    except:
                        tweet = res["text"]

                    reply = get_response(tweet)

                    tweet_id = int(res['id'])

                    screen_name = res["user"]['screen_name']

                    # Tweet the generated text
                    make_tweet(str(reply), tweet_id, screen_name)

                    print(f'User:{screen_name}, Reply:{reply}')

            except BaseException as e:
                print('failed ondata, ', str(e))
                time.sleep(5)

    def on_error(self, status):
        print(status)


if __name__ == "__main__":

    auth = OAuthHandler(config.API_KEY, config.API_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    twitterStream = Stream(auth, listener(), tweet_mode='extended')
    twitterStream.filter(languages=["en"], follow=user_id)
