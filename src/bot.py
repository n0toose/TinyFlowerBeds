#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@author: AlwaysLivid
@description: Bot that posts a tiny flower bed on Twitter every few hours.
'''

import tweepy
import time
import logging, os, textwrap
from config import *
from random import randint

print("""
                       TinyFlowerBeds
            Copyright (C) 2018-2019 AlwaysLivid
=============================================================
======================= DISCLAIMER ==========================
=============================================================
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions; read the LICENSE file for details.
=============================================================
""")

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(asctime)s - %(levelname)s - %(message)s', 
    handlers=[
        logging.FileHandler("{0}/{1}.txt".format(os.path.dirname(os.path.realpath(__file__)), "log")),
        logging.StreamHandler()
    ]
)

mininterval = config['mininterval']
maxinterval = config['maxinterval']

cooldown = randint(mininterval, maxinterval) * 24 * 60 * 60
# converts the random value from days to seconds

limit = config['lines'] * config['limit_per_line']


credential_list = ["CONSUMER_KEY", "CONSUMER_SECRET", "ACCESS_KEY", "ACCESS_SECRET"]
use_environment_variables = bool
use_file_variables = bool
amount_of_credentials = len(credential_list)
credential_counter = 0

CONSUMER_KEY = str
CONSUMER_SECRET = str
ACCESS_KEY = str
ACCESS_SECRET = str

for credential in credential_list:
    if credential_list[0] in os.environ:
        credential_counter += 1

if credential_counter == amount_of_credentials:
    logging.info("All environment variables were found!")
    use_environment_variables = True
    use_file_variables = False
else:
    logging.warning("Environment variables were not successfully found!")
    logging.info("Using credentials.py instead.")
    use_environment_variables = False
    use_file_variables = True

if use_environment_variables == True:
    logging.info("Using environment variables.")
    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    ACCESS_KEY = os.environ['ACCESS_KEY']
    ACCESS_SECRET = os.environ['ACCESS_SECRET']
elif use_file_variables == True:
    logging.info("Using file variables.")
    try:
        from credentials import *
    except ImportError:
        logging.critical("An error occured while importing the credentials from the credentials.py file.")
        logging.critical("The bot will now shut down.")
        logging.info("Please check the README.md file for more information.")
        exit()

class Bot:
    def user_info(self, api, user): 
        ''' 
        Prints user information. 
        
        Also works as a way to check whether the credentials are valid without making a tweet.
        '''
        logging.info("Username: {}".format(api.get_user(user.id).screen_name))
        logging.info("Display Name: {}".format(user.name))
        logging.info("ID: {}".format(user.id))

    def generate_batch(self):
        '''
        Generates a string containing flower emojis, while creating a virtual flower bed in the form of a tweet!
        '''
        batch = ''
        counter = 0
        while counter != limit:
            batch += random.choice(config['emojis'])
            counter += 1
        batch = batch[:16] # Temporary hack
        tweet = '\n'.join(textwrap.wrap(batch, config['limit_per_line']))
        return tweet

    def tweet_loop(self, api):
        '''
        Function that generates and tweets a flower batch at a specified interval.
        '''
        while True:
            try:
                if not (os.getenv('CI') == None or os.getenv('CI') == False) or not (os.getenv('CONTINUOUS_INTEGRATION') == None or os.getenv('CONTINUOUS_INTEGRATION') == False):
                    logging.critical("CI detected! Skipping tweet.")
                    logging.critical("Everything seems to be fine. Exiting...")
                    exit()
                else:
                    api.update_status(self.generate_batch())
                    logging.info("Tweeted out a new flower bed!")
                    logging.info("The next tweet is scheduled to be made in {} minutes".format(cooldown))
                    time.sleep(cooldown)
            except tweepy.RateLimitError:
                logging.critical("Tweeting failed due to ratelimit. Waiting {} more minutes.".format(cooldown))
                time.sleep(cooldown)

    def main(self):
        '''
        Main function that takes care of the authentication and the threading.
        '''
        logging.info("Attempting to login!")
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)
        user = api.me()
        self.user_info(api, user)
        logging.info("Successfully logged in!")
        self.tweet_loop(api)

if __name__ == '__main__':
    try:
        TwitterBot = Bot()
        TwitterBot.main()
        
        
        
    except tweepy.RateLimitError:
        logging.critical("Tweeting failed due to ratelimit. Waiting {} more minutes.".format(cooldown))
        time.sleep(cooldown)
    except tweepy.TweepError:
      logging.critical("Authentication Error!")
      logging.info("Please validate your credentials.")
      time.sleep(10)
      quit()
    except Exception as ex:
      logging.critical("Exception {} has occured.".format( type(ex).__name__))
      logging.critical("The app will now exit")
      quit()
