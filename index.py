import tweepy
from time import sleep
from random import choice

bearer_token = r"AAAAAAAAAAAAAAAAAAAAAKxVeQEAAAAAph0uSxt7QAtYN6ujkMo1lyCCU3w%3D1JnfDfbWB83lu2lFtLdquMT2B8zBpGekciE7IkJKi66HwiCvY2"
consumer_key = "9pYreB2pLfotJ8yMFRHW8zfQh"
consumer_secret = "Ph5bO29RHf4RrcX6NZvs9lOgfwDwfoFFw8OVMQb1kPAuxRDwr6"
access_token = "1542331311192416256-ukiZbZbxf4qyKbQ9bPLTkHf8ZjrHCB"
access_token_secret = "TX2HMac7q5YGPUOHFymBYzTRXRpo74jdyBLePDlo0woYF"

client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret) 
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

bot_id = client.get_me().data.id
start_id = 1
text = choice(['ih mané', 'meteu essa serin?', 'ta maluco po', 'que papinho hein?', 'VASCO'])
while True: 
    response = client.get_users_mentions(bot_id, since_id = start_id)
    if response.data != None:
        for tweet in response.data:
            try:
                client.create_tweet(in_reply_to_tweet_id=tweet.id, text=text)
                start_id = tweet.id
            except:
                print('error')

    sleep(5)
