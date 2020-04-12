
import tweepy
import time
import logging, os, textwrap
from config import *
from random import randint
import sys
import credentials
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
            except:
                print(sys.exc_info())
                logging.critical("Tweeting failed due to ratelimit. Waiting {} more minutes.".format(cooldown))
                time.sleep(cooldown)
                
    def main(self):
        '''
        Main function that takes care of the authentication and the threading.
        '''
        logging.info("Attempting to login!")


        # Authenticate to Twitter
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

        api = tweepy.API(auth)

        try:
            api.verify_credentials()
            logging.info("Successfully logged in!")
            self.tweet_loop(api)
        except:
            print("Error during authentication")


if __name__ == '__main__':
    try:
        
        TwitterBot = Bot()
        
        TwitterBot.main()
    except:
      print(sys.exc_info())
      quit()
