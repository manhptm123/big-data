from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
from textblob import TextBlob


def cleanTweet(tweet: str) -> str:
    tweet = re.sub(r'http\S+', '', str(tweet))
    tweet = re.sub(r'bit.ly/\S+', '', str(tweet))
    tweet = tweet.strip('[link]')

    # remove users
    tweet = re.sub('(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)', '', str(tweet))
    tweet = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)', '', str(tweet))

    # remove puntuation
    my_punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@â'
    tweet = re.sub('[' + my_punctuation + ']+', ' ', str(tweet))

    # remove number
    tweet = re.sub('([0-9]+)', '', str(tweet))

    # remove hashtag
    tweet = re.sub('(#[A-Za-z]+[A-Za-z0-9-_]+)', '', str(tweet))

    return tweet

def getSubjectivity(tweet: str) -> str:
    return str(TextBlob(tweet).sentiment.subjectivity)
    
def getPolarity(tweet: str) -> str:
    sid_obj = SentimentIntensityAnalyzer()
    return str(sid_obj.polarity_scores(tweet)['compound'])

def getSentiment(polarityValue: str) -> str:
    if float(polarityValue) >= 0.05:
        return 'Positive'
    elif float(polarityValue) <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'
