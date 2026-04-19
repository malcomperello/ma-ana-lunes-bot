import tweepy
import os

auth = tweepy.OAuth1UserHandler(
    os.environ["API_KEY"],
    os.environ["API_SECRET"],
    os.environ["ACCESS_TOKEN"],
    os.environ["ACCESS_SECRET"]
)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    api.update_status("SÍ.")
    print("Tweet enviado")
except Exception as e:
    print("ERROR:", e)
