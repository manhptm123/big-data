from kafka import KafkaProducer
import tweepy
"""API ACCESS KEYS"""
# API Key : fthucnbP6DZHq5lFDmTUVjCQy
# API Key Secret: ThKtzAlOkX6T9XXABwdeaMFudocsmuynoSTpS9Yaq6GmoG7XJJ
bearer_token_1 = "AAAAAAAAAAAAAAAAAAAAADufeQEAAAAAHqRW9ARhjvsogOFvBf0jKEDuRrk%3DjxaNVaAu6IojtB064K3a1B84XCVfaOIse3kb3UCYY0CzsoySIv"
bearer_token_2 = "AAAAAAAAAAAAAAAAAAAAAMeBfAEAAAAAkBQ4oQccNyNdrZPnMT5uLxlXsnM%3DuEWkFh3i8DI9lrNLr6GU01proIkacLqpdRiGxB1C6HaSGlhgV8"
# consumerKey = "fthucnbP6DZHq5lFDmTUVjCQy"
# consumerSecret = "ThKtzAlOkX6T9XXABwdeaMFudocsmuynoSTpS9Yaq6GmoG7XJJ"
# accessToken = "1543157172733083648-e2x4tVgAoqcRqObJd6IpSAZyZGPC7s"
# accessTokenSecret = "FRwxk8A0PsCTwbxZUf2du2nOYm0yPdfVNxniqTtmIrd2p"

producer = KafkaProducer(bootstrap_servers='localhost:9092')

# def twitterAuth():
#     authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)
#     authenticate.set_access_token(accessToken, accessTokenSecret)
#     api = tweepy.API(authenticate, wait_on_rate_limit=True)
#     return api