import time,json,sys,requests
from kafka import KafkaProducer
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import Stream

# es = Elasticsearch()
con_key ='KEY'
con_secret ='KEY'
acess_token ='KEY'
acess_secret = 'KEY'
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))

class listener(StreamListener):
    def on_data(self, raw_data):
        all_data = json.loads(raw_data)
        if 'text' in all_data and all_data["user"]["location"] != 'null' :
            try:
                location = all_data["user"]["location"]
                response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address= %s' % location)
                resp_json_payload = response.json()
                doc = {
                    'location': resp_json_payload['results'][0]['geometry']['location'],
                    'tweet': all_data["text"],
                    'username': all_data["user"]["screen_name"]
                }
                print(doc)
                producer.send('myTopic', doc)
                # hell = es.index(index="twitter", doc_type='tweet', body=doc)
                # print("Tweet for trump added")
            except:
                pass

    def on_error(self, status_code):
        print ("Error Code: %s" % status_code)

auth = OAuthHandler(con_key, con_secret)
auth.set_access_token(acess_token, acess_secret)

try:
    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=["trump", "marchforscience", "RecordStoreDay", "FACup", "ReasonsToLeaveEarth"])
except:
    pass
