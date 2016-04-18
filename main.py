import tweepy
import csv
from tqdm import tqdm
from twittersecrets import *

# Authenticating
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(token, token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=False)


def get_friends(user_id=None):
   """Return the list of followers and last tweet date and text"""
   try:
      friends = api.friends_ids(user_id=user_id)
      return friends
   except tweepy.error.TweepError:  # No access to user
      return []


class Friend(object):
   def __init__(self, user_id, screen_name, description, friends):
       self.user_id = user_id
       self.screen_name = screen_name
       self.description = description
       self.friends = friends

   def write_to_csv(self, file="friends.csv"):
       with open('friends.csv', 'a') as f:
           writer = csv.writer(f)
           row = [self.screen_name, self.user_id, self.description, len(self.friends)] + self.friends
           writer.writerow(row)

if __name__ == '__main__':

  my_friends = get_friends()
  print "Got %s friends" % str(len(my_friends))
  me = Friend(0, "vallettea", "", my_friends)
  me.write_to_csv()

  for user_id in tqdm(me.friends):
      friends = get_friends(user_id)
      try:
        friend = api.get_user(user_id)
        f = Friend(user_id, friend.screen_name, friend.description, friends)
        f.write_to_csv()
      except:
        pass
