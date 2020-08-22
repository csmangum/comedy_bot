"""
File to generate response based on GPT-2 language model
"""

from simpletransformers.language_generation import LanguageGenerationModel
from simpletransformers.classification import ClassificationModel
import config as conf
from util import *
import random

model = LanguageGenerationModel(
    "gpt2", "comedy_bot/models/text_gen", args={"max_length": 300}, use_cuda=False)

score = ClassificationModel(
    "roberta", "comedy_bot/models/text_classify", use_cuda=False)


def generate_response(prompt, trunc=True):
    """
    Generate a response based on incoming prompt
    :return: generated response
    """
    if prompt[-1] not in ['.', '?', '!', '"', '”'] and trunc:
        prompt = prompt + '.'

    if trunc is False:
        words = conf.ADD_WORDS

        prompt = prompt + random.choice(words)

    generated = model.generate(prompt, verbose=False)

    if trunc:
        response = generated[0][len(prompt):]
    else:
        response = generated[0]

    return response


def get_response(prompt, trunc=True):
    """
    Prepare generated response for tweeting
    :return: generated response
    """
    while True:
        response = prepare_tweet(generate_response(prompt, trunc=trunc))
        predictions, raw_outputs = score.predict([response])

        if predictions[0] == 1:
            break

    return response
