#!/usr/bin/env python3

import schedule
import time
from datetime import datetime
import tweepy

# social media credentials (placeholder values, replace with your own)
TWITTER_CONSUMER_KEY = 'your_twitter_consumer_key'
TWITTER_CONSUMER_SECRET = 'your_twitter_consumer_secret'
TWITTER_ACCESS_TOKEN = 'your_twitter_access_token'
TWITTER_ACCESS_TOKEN_SECRET = 'your_twitter_access_token_secret'

# Authenticate to Twitter
auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth)

# Function to post to Twitter
def post_to_twitter(text):
    try:
        print(f"Posting to Twitter at {datetime.now()}")
        api.update_status(text)
        print("Posted successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

# Your posts data
posts = [
    {"time": "09:00", "text": "Good morning! #morningvibes"},
    {"time": "12:00", "text": "Check out our new product! #innovation"},
    {"time": "18:00", "text": "Thanks for following us today. #gratitude"}
]

# Schedule the posts
for post in posts:
    schedule.every().day.at(post["time"]).do(post_to_twitter, post["text"])

# Keeps the script running to execute the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
