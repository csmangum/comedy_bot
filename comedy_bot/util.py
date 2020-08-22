"""File to perform text based cleaning and prep
"""

import re
import random
import config as conf
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key=conf.NEWSAPI)


def clean_html(text):
    """
    Use regex to clean text
    :return: string
    """
    patt_dict = {
        r"(?:\@|https?\://)\S+": "",
        r"pic.twitter.com/\w+": "",
        r"\w+\/+": "",
        r"\@w+": "",
    }

    pattern = re.compile("|".join(patt_dict.keys()), re.I)

    corrected = pattern.sub("", text)

    return fix_punct(corrected)


def fix_punct(text):
    """
    Fix punctuation
    :return: string
    """
    rep = {
        ".": ". ",
        "...": ". ",
        ",...": ". ",
        "..": ". ",
        "?": "? ",
        "!": "! ",
        "””": "",
        "“": "",
        "”": "",
        "Dr.": "Dr",
        "<|endoftext|>": "", }

    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    final = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    cleaned = final.replace('  ', ' ').strip()

    return cleaned


def prepare_tweet(string):
    """
    Perform all text prep for tweeting
    :return: final prepped response
    """
    rand_length = random.randrange(2, 5)

    reply = ''

    for t in string.split('.')[:rand_length]:
        reply = reply+t+'.'

        if len(reply) >= 200:
            reply = reply.replace(t+'.', '')

            break

    response = clean_html(reply)

    return response
