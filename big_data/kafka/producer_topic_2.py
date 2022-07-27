import tweepy
from kafka import KafkaProducer
import logging
from producer import bearer_token_2,producer

search_term_2 = 'samsung'
topic_name_2 = 'samsung'
bearer_token = bearer_token_2
class Topic_2_Listener(tweepy.StreamingClient):

    def on_data(self, raw_data):
        logging.info("LOGGING")
        logging.info(raw_data)
        producer.send(topic_name_2, value=raw_data)
        print(raw_data)
        return True

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def start_streaming_tweets(self, search_term):
        print("start")
        self.add_rules(tweepy.StreamRule(search_term))
        print("filter")
        self.filter(tweet_fields=["created_at"])

if __name__ == '__main__':
    topic_2_stream = Topic_2_Listener(bearer_token)
    topic_2_stream.start_streaming_tweets(search_term_2)

