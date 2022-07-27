from ast import Str
from pyspark.sql import functions as F
from pyspark.sql.functions import lit
from pyspark.sql.types import StringType, StructType, StructField
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
import findspark
from spark.my_utils import cleanTweet, getPolarity,getSentiment,getSubjectivity
# from sentiment_anylasis import model,tokenizer,sentimentAnylasis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
from textblob import TextBlob


findspark.init()


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


def write_row_in_mongo(df, dd):
    print(df.show())
    print(df.printSchema())
    df.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()
    pass


if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("TwitterSentimentAnalysis") \
        .master('local[*]') \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.mongodb.spark:mongo-spark-connector_2.12:3.0.0") \
        .config("spark.mongodb.input.uri","mongodb+srv://manh:123@abc.jo2kt.mongodb.net/abc.uvw")\
        .config("spark.mongodb.output.uri","mongodb+srv://manh:123@abc.jo2kt.mongodb.net/abc.uvw")\
        .getOrCreate()

    print("*******COLUMNS*******")
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "apple") \
        .load()
    print("COLUMNS:", df.columns)
    print("=============")

    mySchema = StructType([StructField("data", StringType(), True)])
    schema = StructType([
            StructField("data", StructType([
                StructField("text",StringType(),True),
                StructField("created_at",StringType(),True)
            ]),True),
        ])

    values = df.select(from_json(df.value.cast("string"), schema).alias("tweet"))

    df1 = values.select("tweet.*")

    print(df1.printSchema())
        
    clean_tweets = F.udf(cleanTweet, StringType())
    
    raw_tweets = df1.withColumn('processed_text', clean_tweets(col("data.text"))).withColumn('created_at', col("data.created_at"))
    subjectivity = F.udf(getSubjectivity, StringType())
    polarity = F.udf(getPolarity, StringType())
    sentiment = F.udf(getSentiment, StringType())
   
    subjectivity_tweets = raw_tweets.withColumn('subjectivity', subjectivity(col("processed_text")))
    polarity_tweets = subjectivity_tweets.withColumn("polarity", polarity(col("processed_text")))
    sentiment_tweets = polarity_tweets.withColumn("sentiment", sentiment(col("polarity")))

    topic = sentiment_tweets.withColumn('topic',lit('apple'))

    query = topic.writeStream.format("console") \
        .foreachBatch(write_row_in_mongo).start()

    query.awaitTermination()