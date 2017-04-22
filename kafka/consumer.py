import boto3
import json
from kafka import KafkaConsumer
from textblob import TextBlob

awsAccessKey = 'KEY'
awsSecret = 'SecretKEY'
awsRegion = 'us-west-2'

# create instance of AWS SNS
consumer = KafkaConsumer('myTopic')
arn = 'SNS ARN'


# Create an SNS clienthttps://search-twittermap-zhychepoqowvbu7g3v5r7uqesq.us-west-2.es.amazonaws.com/
client = boto3.client(
    "sns",
    aws_access_key_id=awsAccessKey,
    aws_secret_access_key=awsSecret,
    region_name=awsRegion
)


for msg in consumer:
    tweetMsg = json.loads(msg.value)
    sentimentAnalyzer = TextBlob(tweetMsg['tweet'])
    tweetPolarity = sentimentAnalyzer.sentiment.polarity
    tweetMsg['sentiment'] = (0 if tweetPolarity < -0.25 else 1) if tweetPolarity < 0.25 else 2 # 0-negative, 1-neutral, 2-positive
    print(json.dumps(tweetMsg))
    response = client.publish(
        TargetArn=arn,
        Message=json.dumps(tweetMsg)
    )
