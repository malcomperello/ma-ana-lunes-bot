import tweepy
import os
import traceback

try:
    auth = tweepy.OAuth1UserHandler(
        os.environ["API_KEY"],
        os.environ["API_SECRET"],
        os.environ["ACCESS_TOKEN"],
        os.environ["ACCESS_SECRET"]
    )

    api = tweepy.API(auth)

    print("Probando credenciales...")
    api.verify_credentials()
    print("Auth OK")

    print("Intentando tweet...")
    response = api.update_status("SÍ.")
    print("Tweet enviado:", response)

except Exception as e:
    print("ERROR COMPLETO:")
    traceback.print_exc()
