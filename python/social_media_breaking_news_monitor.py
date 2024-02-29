#!/usr/bin/env python3
import tweepy
import time

# Twitter API credentials
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_TOKEN_SECRET = "your_access_token_secret"

# Authenticate to Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Define the list of keywords to monitor
KEYWORDS = ["breaking news", "urgent", "alert"]

class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            # Extract relevant information from the tweets
            tweet_text = status.extended_tweet["full_text"] if 'extended_tweet' in status._json else status.text

            for keyword in KEYWORDS:
                if keyword.lower() in tweet_text.lower():
                    print(f"Breaking News: @{status.user.screen_name} tweeted: {tweet_text}")
                    # Here you can add your code to alert you, store the tweet, or handle it in a different way

        except Exception as e:
            print(f"Error: {e}")

    def on_error(self, status_code):
        if status_code == 420:
            # Return False to disconnect the stream
            return False

# Setup Stream listener
listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=listener)

# Filter realtime Tweets by keywords
print("Monitoring Twitter for breaking news...")
stream.filter(track=KEYWORDS)

# Keep the script running
while True:
    time.sleep(60)
