#!/usr/bin/env python
# -*- coding: utf-8 -*-

from credentials import *
import tweepy
import time, random
import logging, os                                                                                                                                                     

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(asctime)s - %(levelname)s - %(message)s', 
    handlers=[
        logging.FileHandler("{0}/{1}.txt".format(os.path.dirname(os.path.realpath(__file__)), "log")),
        logging.StreamHandler()
    ]
)

config = {
    'limit_per_line': 5,
    'lines': 3,
    'hour': 3600, # minutes in an hour
    'cooldown': 2, # hours to wait
    'emojis': ["🌻", "💮", "🌺", "🌹", "🌼", "🌿", "🌿", "🌷"]
}

limit = config['lines'] * config['limit_per_line']

def user_info(api, user): 
    ''' 
    Prints user information. 
    
    Also works as a way to check whether the credentials are valid without making a tweet.
    '''
    logging.info("Username: {}".format(api.get_user(user.id).screen_name))
    logging.info("Display Name: {}".format(user.name))
    logging.info("ID: {}".format(user.id))

def generate_batch():
    '''
    Generates a string containing flower emojis, while creating a virtual flower bed in the form of a tweet!
    '''
    batch = []
    counter = 0
    while counter < limit:
        if counter % config['limit_per_line'] == 0:
            batch.append("\n")
        counter += 1
        batch.append(random.choice(config['emojis']))
    tweet = ''.join(batch)
    return tweet

def main():
    logging.info("Attempting to login!")
    auth = tweepy.OAuthHandler(cons_key, cons_sec)
    auth.set_access_token(access_key, access_sec)
    api = tweepy.API(auth)
    user = api.me()
    user_info(api, user)
    logging.info("Successfully logged in!")
    while True:        
        try:
            # api.update_status(generate_batch())
            logging.info("Tweeted out a new flower bed!")
            logging.info("The next tweet is scheduled to be made in {0} minutes".format(config['hour']))
            time.sleep(config['hour'] * config['cooldown'])
        except tweepy.RateLimitError:
            logging.critical("Tweeting failed due to ratelimit.")
            time.sleep(config['hour'] * config['cooldown'])

if __name__ == '__main__':
    try:
        main()
    except tweepy.TweepError:
      logging.critical("Authentication Error!")
      logging.info("Please validate your credentials in the  credentials.py file.")
      time.sleep(10)
      quit()
