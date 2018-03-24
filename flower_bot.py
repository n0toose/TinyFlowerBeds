#!/usr/bin/env python

from credentials import *
import tweepy
import time, random

# Variables 

flowers = ["🌻", "💮", "🌺", "🌹", "🌼", "🌿", "🌿", "🌷"]
limit_per_line = 5
lines = 3
limit = lines * limit_per_line
hour = 3600 # Will be used later for cooldowns
cooldown = 2

def generate_batch():
    batch = []
    counter = 0
    while counter < limit:
        if counter % limit_per_line == 0:
            batch.append("\n")
        counter += 1
        batch.append(random.choice(flowers))
    tweet = ''.join(batch)
    return tweet

def start():
    while True:
        try:
            api.update_status(generate_batch())
            time.sleep(hour * cooldown)
        except tweepy.TweepError:
            time.sleep(hour * cooldown)

try:
    auth = tweepy.OAuthHandler(cons_key, cons_sec)
    auth.set_access_token(access_key, access_sec)
    api = tweepy.API(auth)
    print("Successfully logged on!")
    start()
except tweepy.TweepError:
    print("Authentication Error!")
    print("The credentials you supplied were probably incorrect.")
    time.sleep(10)
    quit()


