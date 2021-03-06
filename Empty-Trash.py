#!/usr/bin/python3.8
import tweepy
import time
import sys
from keyconf import Config
from datetime import date

Go = False

def main():
    global Go

    Api_Key = Config['Api_Key']
    Api_Secret = Config['Api_Secret']
    Bearer_Token = Config['Bearer_Token']
    Access_Token = Config['Access_Token']
    Access_Secret = Config['Access_Secret']
    Account_ScreeName = Config['Account_ScreeName']
    Inactive_Day = Config['Inactive_Day']


    auth = tweepy.OAuthHandler(Api_Key, Api_Secret)
    auth.set_access_token(Access_Token,Access_Secret)

#    api = tweepy.API(auth, retry_count=10, retry_delay=30, timeout=60,wait_on_rate_limit=True)
    api = tweepy.API(auth, retry_count=3, retry_delay=5, timeout=30,wait_on_rate_limit=True)
    user = api.get_user(screen_name=Account_ScreeName)

    print("%s has %s friends"%(Account_ScreeName,user.followers_count))
    print("%s is following %s users"%(Account_ScreeName,user.friends_count))

    print("\n\n===\n***\nProceeding with Friends:")
    inactives = [];


    for friend in tweepy.Cursor(api.get_friends, screen_name=user.screen_name).items():
        print("\n***\n-Friend: ", friend.screen_name)
#        if "crazyjunkie1" == friend.screen_name:
#           Go = True
#        if Go is False:
#               continue
        try:
            tweets_list= api.user_timeline(screen_name = friend.screen_name, count = 1)
            tweet= tweets_list[0] 
            print('-Last tweet:',tweet.created_at)
            print()

            delta = date.today() - tweet.created_at.date()

            if (delta.days > int(Inactive_Day)):
                print("-%s account is NOT active..."%friend.screen_name)
                inactives.append(friend)
                print("-Unfollowing :", friend.screen_name)
                api.destroy_friendship(screen_name=friend.screen_name)
                time.sleep(2)
            else:
                print("-%s account is active."%friend.screen_name)

        except Exception as e:
              if "list index out of range" in str(e):
                  print("-User has no tweets")
                  print("-Unfollowing :", friend.screen_name)
                  api.destroy_friendship(screen_name=friend.screen_name)
              elif "401 Unauthorized" in str(e):
                  print("-Tweets from %s are hidden."%friend.screen_name)
                  print("-Unfollowing :", friend.screen_name)
                  api.destroy_friendship(screen_name=friend.screen_name)

              else:
                 print("\nError :",e)
              time.sleep(5)

####
    print("\n\n===\n***\nProceeding with Followers:")

    for friend in tweepy.Cursor(api.get_followers, screen_name=user.screen_name).items():
        print("\n***\n-Friend: ", friend.screen_name)
        try:
            tweets_list= api.user_timeline(screen_name = friend.screen_name, count = 1)
            tweet= tweets_list[0] 

            print('-Last tweet:',tweet.created_at)
            print()

            delta = date.today() - tweet.created_at.date()
            if (delta.days > int(Inactive_Day)):
                print("-%s account is NOT active..."%friend.screen_name)
                inactives.append(friend)
                print("Unfollowing ", friend.screen_name)
                api.destroy_friendship(screen_name=friend.screen_name)
                time.sleep(2)
            else:
                print("-%s account is active."%friend.screen_name)

        except Exception as e:
              if "list index out of range" in str(e):
                  print("-User has no tweets")
                  print("-Unfollowing :", friend.screen_name)
                  api.destroy_friendship(screen_name=friend.screen_name)
              elif "401 Unauthorized" in str(e):
                  print("-Tweets from %s are hidden."%friend.screen_name)
                  print("-Unfollowing :", friend.screen_name)
                  api.destroy_friendship(screen_name=friend.screen_name)
              else:
                 print("\nError :",e)
              time.sleep(5)


    if len(inactives) > 0:

        for friend in inactives:
            print(friend.screen_name)

        print("The %s users above were inactives for more than %s days and has been unfollowed." %(len(inactives),Inactive_Day))
    else:
        print("No inactives users were found.")

if __name__ == "__main__":
    main()
