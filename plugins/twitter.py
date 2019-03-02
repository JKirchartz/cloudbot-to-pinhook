import re
import random
from datetime import datetime
import tweepy
import requests
import os
import pinhook.plugin
import json

TWITTER_RE = re.compile(r"(?:(?:www.)?twitter.com\/(?:[-_a-zA-Z0-9]+)\/status\/)([0-9]+)", re.I)
COMMAND_RE = re.compile(r"(?:!tw(?:itter|eet)) ?(\w+) (.*?)", re.I)

with open('config.json') as f:
      config = json.load(f)

consumer_key = config["twitter"]["consumer_key"]
consumer_secret = config["twitter"]["consumer_secret"]
oauth_token = config["twitter"]["access_token"]
oauth_secret = config["twitter"]["access_secret"]

print("twitter loaded")

if not all((consumer_key, consumer_secret, oauth_token, oauth_secret)):
    print("missing twitter keys!");
    tw_api = None
else:
    print("tweepy loades")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(oauth_token, oauth_secret)
    tw_api = tweepy.API(auth)


@pinhook.plugin.listener('twitter_url')
def twitter_url(msg):
    m = re.match(TWITTER_RE, msg.text)
    if m:
      print("twitter: match!")
    else:
      print("twitter: not match")
      return

    print("found twitter URL");
    # Find the tweet ID from the URL
    tweet_id = m.group(1)

    if msg.channel == "#discord":
        return

    # Get the tweet using the tweepy API
    if tw_api is None:
        return

    try:
        tweet = tw_api.get_status(tweet_id, tweet_mode='extended')
        user = tweet.user
    except tweepy.error.TweepError:
        return

    # Format the return the text of the tweet
    text = " ".join(tweet._json['full_text'].split())

    if user.verified:
        prefix = "\u2713"
    else:
        prefix = ""

    return "{}@\x02{}\x02 ({}): {}".format(prefix, user.screen_name, user.name, text.decode('utf-8'))



def twitter_get(text):
    """twitter get <user> [n] -- Gets last/[n]th tweet from <user>"""

    if tw_api is None:
        return "This command requires a twitter API key."

    if re.match(r'^\d+$', text):
        # user is getting a tweet by id

        try:
            # get tweet by id
            tweet = tw_api.get_status(tweet_id, tweet_mode='extended')
            tweet = " ".join(tweet._json['full_text'].split())
        except tweepy.error.TweepError as e:
            if "404" in e.reason:
                return "Could not find tweet."
            else:
                return "Error: {}".format(e.reason)

        user = tweet.user

    elif re.match(r'^\w{1,15}$', text) or re.match(r'^\w{1,15}\s+\d+$', text):
        # user is getting a tweet by name

        if text.find(' ') == -1:
            username = text
            tweet_number = 0
        else:
            username, tweet_number = text.split()
            tweet_number = int(tweet_number) - 1

        if tweet_number > 200:
            return "This command can only find the last \x02200\x02 tweets."

        try:
            # try to get user by username
            user = tw_api.get_user(username)
        except tweepy.error.TweepError as e:
            if "404" in e.reason:
                return "Could not find user."
            else:
                return "Error: {}".format(e.reason)

        # get the users tweets
        user_timeline = tw_api.user_timeline(id=user.id, count=tweet_number + 1, tweet_mode="extended")

        # if the timeline is empty, return an error
        if not user_timeline:
            return "The user \x02{}\x02 has no tweets.".format(user.screen_name)

        # grab the newest tweet from the users timeline
        try:
            tweet = user_timeline[tweet_number]
        except IndexError:
            tweet_count = len(user_timeline)
            return "The user \x02{}\x02 only has \x02{}\x02 tweets.".format(user.screen_name, tweet_count)

    elif re.match(r'^#\w+$', text):
        # user is searching by hashtag
        search = tw_api.search(text)

        if not search:
            return "No tweets found."

        tweet = random.choice(search)
        user = tweet.user
    else:
        # ???
        return "Invalid Input"

    # Format the return the text of the tweet
    text = " ".join(tweet._json['full_text'].split())

    if user.verified:
        prefix = "\u2713"
    else:
        prefix = ""

    return "{}@\x02{}\x02 ({}): {}".format(prefix, user.screen_name, user.name, text)

def twpost(text):
    """twitter post <text> -- tweet the text <text>"""
    if tw_api is None:
      return

    try:
      user = tw_api.update_status(text)

    except tweepy.error.TweepError as e:
        if "404" in e.reason:
            return "Could not send tweet."
        else:
            return "Error: {}".format(e.reason)


def twuser(text):
    """twitter info <user> -- Get info on the Twitter user <user>"""

    if tw_api is None:
        return

    try:
        # try to get user by username
        user = tw_api.get_user(text)
    except tweepy.error.TweepError as e:
        if "404" in e.reason:
            return "Could not find user."
        else:
            return "Error: {}".format(e.reason)

    if user.verified:
        prefix = "\u2713"
    else:
        prefix = ""

    if user.location:
        loc_str = " is located in \x02{}\x02 and".format(user.location)
    else:
        loc_str = ""

    if user.description:
        desc_str = " The users description is \"{}\"".format(user.description)
    else:
        desc_str = ""

    return "{}@\x02{}\x02 ({}){} has \x02{:,}\x02 tweets and \x02{:,}\x02 followers.{}" \
           "".format(prefix, user.screen_name, user.name, loc_str, user.statuses_count, user.followers_count,
                     desc_str)


def tweet_image(inp):
    inp = inp.split(' ')
    url = inp[0]
    message = " ".join(inp[1:])
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        tw_api.update_with_media(filename, status=message)
        os.remove(filename)
        return "Tweet posted at https://twitter.com/Bob_Sequious"
    else:
        return "Unable to load image"


#@pinhook.plugin.register('tweet')
def tweet(inp):
    try:
        tw_api.update_status(status=inp.replace('~~', '\n'))
        return "Tweet posted at https://twitter.com/Bob_Sequious"
    except tweepy.error.TweepError:
        return "Tweet exceeds 280 characters [" + str(len(inp.replace("~~"," ")))+"]"

#@pinhook.plugin.register('tsearch')
def search_tweet(inp):
    results = tw_api.search(q=inp)
    for result in results:
        return result.text

#@pinhook.plugin.register('ttrends')
def get_trends(inp):
    results = tw_api.trends_place(23424977)
    data = results[0]
    trends= data['trends']
    names = [trend['name'] for trend in trends]
    trendsName = ', '.join(names)
    return "US Twitter Trends: " + trendsName


def twitter(text):
    '''!twitter [show <user> [#]|info <user> |post <tweet>|image <image url> <tweet>|search <keyword>|trends]'''
    inp = text.split()
    if len(inp):
      if inp[0]=='show' or inp[0]=='get':
          return twitter_get(" ".join(inp[1:]))
      elif inp[0]=='post' or inp[0]=='send':
          return tweet(" ".join(inp[1:]))
      elif inp[0]=='image' or inp[0]=='pic':
          return tweet_image(" ".join(inp[1:]))
      elif inp[0] == 'info':
          return twuser(" ".join(inp[1:]))
      elif inp[0]=='search':
          return search_tweet(" ".join(inp[1:]))
      elif inp[0]=='trends':
          return get_trends(" ".join(inp[1:]))
    return "!twitter [show <user> [#]|info <user> |post <tweet> |image <image url> <tweet> |search <keyword>|trends]"

@pinhook.plugin.register('!tw')
@pinhook.plugin.register('!tweet')
@pinhook.plugin.register('!twitter')
def twitter_cmd(msg):
    print("twitter_cmd run!")
    return pinhook.plugin.message(twitter(msg.arg))

