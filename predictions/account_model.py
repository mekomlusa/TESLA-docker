from django.db import models
import twitter
import time
import pandas as pd
import numpy as np
import pickle
from sklearn.externals import joblib
import json
import os

script_dir = os.path.dirname(__file__)

from .ignore import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET


def get_user(user_id=None, screen_name=None):

    api = twitter.Api(consumer_key=CONSUMER_KEY,
                     consumer_secret=CONSUMER_SECRET,
                     access_token_key=ACCESS_TOKEN_KEY,
                     access_token_secret=ACCESS_TOKEN_SECRET)

    try:
        json = api.GetUser(user_id=user_id, screen_name=screen_name, include_entities=True, return_json=False)
        json_data = json._json
    except:
        return None
    
    # feature Count of favorite tweets
    Count_of_favorite_tweets = int(json_data['favourites_count'])
    # feature Friends to follower ratio
    if json_data['followers_count'] == 0:
        Friends_to_follower_ratio = float(100000)
    else:
        Friends_to_follower_ratio = (float(json_data['friends_count']) / json_data['followers_count'])
    # feature Total status count
    Total_status_count = int(json_data['statuses_count'])
    
    # feature Default profile image & Default profile
    # def_p_na','def_p_false','def_p_true'
    if json_data['default_profile_image'] == 'FALSE':
        Def_p_img_false = 1.0
        Def_p_img_true = 0.0
        Def_p_img_na = 0.0
    elif json_data['default_profile_image'] == 'True':
        Def_p_img_false = 0.0
        Def_p_img_true = 1.0
        Def_p_img_na = 0.0
    else:
        Def_p_img_false = 0.0
        Def_p_img_true = 0.0
        Def_p_img_na = 1.0

    if json_data['default_profile'] == 'FALSE':
        Def_p_false = 1.0
        Def_p_true = 0.0
        Def_p_na = 0.0
    elif json_data['default_profile'] == 'True':
        Def_p_false = 0.0
        Def_p_true = 1.0
        Def_p_na = 0.0
    else:
        Def_p_false = 0.0
        Def_p_true = 0.0
        Def_p_na = 1.0
    
    # feature Account ages
    created_at = json_data['created_at']
    Account_age = survival_time(created_at)

    # feature User name and screen_name
    User_name = json_data['name']
    Screen_name = json_data['screen_name']
    User_name_digit, User_name_char = counter(User_name)
    Screen_name_digit, Screen_name_char = counter(Screen_name)

    # feature Length of description and Description text
    description_pre = json_data['description']
    Description_length = len(description_pre)
    
    # feature Average tweet per day
    # Average_tweets_per_day = Total_status_count / float(Account_age)

    # feature listed count
    Listed_count = json_data['listed_count']

    # feature of description, the number of hashtag, @ and url
    Bio_hashtag = json_data['description'].count('#')
    Bio_at = json_data['description'].count('@')
    Bio_url = json_data['description'].count('http')

    feature = pd.DataFrame(index=[0])
    feature['favorite_count'] = Count_of_favorite_tweets
    feature['friends_to_followers'] = Friends_to_follower_ratio
    feature['statuses_count'] = Total_status_count
    feature['def_p_img_na'] = Def_p_img_na
    feature['def_p_img_false'] = Def_p_img_false
    feature['def_p_img_true'] = Def_p_img_true
    feature['def_p_na'] = Def_p_na
    feature['def_p_false'] = Def_p_false
    feature['def_p_true'] = Def_p_true
    feature['age'] = Account_age
    feature['name_letter'] = User_name_char
    feature['name_num'] = User_name_digit
    feature['screen_letter'] = Screen_name_char
    feature['screen_num'] = Screen_name_digit
    feature['des_len'] = Description_length
#     feature['avg_tweet_per_day'] = Average_tweets_per_day
#     feature['des_text'] = Description_tfidf
    feature['listed_count'] = Listed_count
    feature['bio_hashtag'] = Bio_hashtag
    feature['bio_at'] = Bio_at
    feature['bio_url'] = Bio_url

    return feature



def survival_time(created_at):
	# get the account ages: crawl at time - created at time 
	current_time = time.localtime(time.time())
	current_year = current_time.tm_year
	current_month = current_time.tm_mon
	current_day = current_time.tm_mday

	meta = created_at.split(" ")
	created_month = meta[1]
	if created_month == 'Jan':
		created_month = int(1)
	elif created_month == 'Feb':
		created_month = int(2)
	elif created_month == 'Mar':
		created_month = int(3)
	elif created_month == 'Apr':
		created_month = int(4)
	elif created_month == 'May':
		created_month = int(5)
	elif created_month == 'Jun':
		created_month = int(6)
	elif created_month == 'Jul':
		created_month = int(7)
	elif created_month == 'Aug':
		created_month = int(8)
	elif created_month == 'Sep':
		created_month = int(9)
	elif created_month == 'Oct':
		created_month = int(10)
	elif created_month == 'Nov':
		created_month = int(11)
	elif created_month == 'Dec':
		created_month = int(12)
	created_day = int(meta[2])
	created_year = int(meta[5])

	Account_age = (current_year - created_year) * 365 + (current_month - created_month) * 30 + (current_day - created_day)

	return Account_age

def counter(name):
	# counter of char & counter of digit
	numbers = sum(c.isdigit() for c in name)
	words   = sum(c.isalpha() for c in name)

	return numbers, words



