#!/usr/bin/env python3

import schedule
import time
import random
from datetime import datetime, timedelta
from social_media_api_client import SocialMediaApiClient  # Replace with actual API client for your social media

# Configuration for social media posts
# Please replace 'your_access_token' and 'social_media_api_client' with actual values
ACCESS_TOKEN = 'your_access_token'
social_media_client = SocialMediaApiClient(ACCESS_TOKEN)

def post_to_social_media(message, image_path=None):
    """Posts the message to social media, optionally with an image."""
    try:
        if image_path:
            social_media_client.post_image_with_message(image_path=image_path, message=message)
        else:
            social_media_client.post_message(message)
        print(f"Posted to social media at {datetime.now()}: {message}")
    except Exception as e:
        print(f"Failed to post to social media: {e}")

def schedule_posts():
    """Schedules a series of posts from the provided list."""
    posts = [
        {"message": "Good morning, world!", "image": None, "time": "07:00"},
        {"message": "Here's your daily dose of inspiration!", "image": "inspiration.jpg", "time": "12:00"},
        {"message": "Good night, sweet dreams everyone!", "image": None, "time": "21:00"},
        # Add more posts as needed
    ]

    for post in posts:
        schedule_time = datetime.strptime(post['time'], "%H:%M").time()
        schedule_message = random.choice([post['message'], post['message'].upper(), post['message'].capitalize()])
        if post['image']:
            schedule.every().day.at(post['time']).do(post_to_social_media, schedule_message, post['image'])
        else:
            schedule.every().day.at(post['time']).do(post_to_social_media, schedule_message)

def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each elapsed time interval."""
    while True:
        schedule.run_pending()
        time.sleep(interval)

if __name__ == '__main__':
    schedule_posts()
    run_continuously()
