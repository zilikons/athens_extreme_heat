import os
import tweepy

# Authenticate to Twitter
TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
TWITTER_API_SECRET_KEY = os.environ.get('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
TWITTER_BEARER_TOKEN = os.environ.get('TWITTER_BEARER_TOKEN')


def tweet(message: str, image_path: str = None):
    client = tweepy.Client(TWITTER_BEARER_TOKEN, TWITTER_API_KEY, TWITTER_API_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    auth = tweepy.OAuth1UserHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    if image_path:
        media = api.simple_upload(filename=image_path, media_category='tweet_image')
        client.create_tweet(text=message, media_ids=[media.media_id_string])
        print("Tweeted: " + message + " with image: " + image_path)
    else:
        client.create_tweet(text=message)
        print("Tweeted: " + message)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cat_dir = os.path.join(current_dir,'cat.jpeg')
    tweet("Hello world!",cat_dir)
