
<img src="https://pbs.twimg.com/profile_banners/1286875760058175488/1595728872/1500x500" width="900">

# Comedy Bot

This project aimed to build a full scope Twitter bot using an NLP language model. It was completed in five days using many helpful tools like [Simple Transformers](https://github.com/ThilinaRajapakse/simpletransformers) and [Tweepy](https://www.tweepy.org/). I wanted to use the tweets of comedian [Tim Dillon](https://twitter.com/TimJDillon) to build a twitter bot that could mimic his tweets. I was surprised at how quickly I was able to put up a working but (Less than a day) and at the quality of the results.

I used Open AIs GPT-2 language model to train my bot with around 2,500 tweets. Here is the functionality I wanted to include:

1. Reply to every tweet by Tim Dillon
2. Train a model to score based on tweet likes
    * Tweets classified as high likes are accepted, otherwise a new tweet is generated
3. Tweet on a random interval with one of these tweet types:
    * Meme
    * News Headline
    * Top Trending
    * Retweet selected users
    * Random Image
    * Random GIF

Eventually the account was banned by Tim Dillon as it had become somewhat antagonistic. It was also temporarily limited by Twitter for breaking platform rules. For this reason I eventually stopped running the bot continuously so I could keep a record of the tweets sent by the bot.

Be aware the content is based on a adult-themed comedian. [DimJTillon](https://twitter.com/DimJTillon) twitter bot profile

## How to Use - Docker

I chose to build a Docker implementation for easy start-up. All a user will need to do is:

1. Update the [config](https://github.com/csmangum/comedy_bot/blob/master/comedy_bot/config.py) file with appropriate API keys and settings.

2. Run:

```docker
docker build -t comedy_bot .
```

3. It will take a few minutes to install packages/dependencies and download the models

```docker
docker run comedy_bot
```

## Build model based on user tweets

1. Fine-tune language model

```python
from simpletransformers.language_modeling import LanguageModelingModel

train_args = {
    "reprocess_input_data": True,
    "overwrite_output_dir": True,
    "train_batch_size": 32,
    "num_train_epochs": 5,
    "mlm": False,
    'fp16': True,
    'save_eval_checkpoints': False,
    'no_save': False,
    'no_cache': True,
}

model = LanguageModelingModel('gpt2', 'gpt2', args=train_args, use_cuda=True)

model.train_model(PATH TO TWEETS)
```

2. Fine-tune model used to label response like-ability

```python
from simpletransformers.classification import ClassificationModel

def train(model_type, model_name):
    
    model = ClassificationModel(model_type, model_name, args=({'fp16': False}), use_cuda=True)
    
    model.train_model(df_train,
                 output_dir='test',
                  no_save=True,
                  args=({
                      'save_eval_checkpoints': False,
                      'num_train_epochs':3,
                      'no_save': False,
                      'no_cache': True,
                      'overwrite_output_dir':True})
                 )
    
    result, model_outputs, wrong_predictions = model.eval_model(df_test,
                                                            acc=sklearn.metrics.accuracy_score,
                                                            f1=sklearn.metrics.f1_score,
                                                            roc_auc=sklearn.metrics.roc_auc_score,
                                                            precision=sklearn.metrics.precision_score,
                                                            recall=sklearn.metrics.recall_score)
    
    return result
    
    
train('roberta','roberta-base')
```

3. Add trained models into the model folder
4. Adjust Dockerfile to not download pre-trained model
5. Follow Docker instructions above to run the bot
