from datetime import datetime, timedelta
import os
import math

import pandas as pd
import tweepy
import praw


def getDataFromSources(formData):
    NUMBER_OF_SOURCES = 2
    dataArray = []
    errorList = []

    if 'checkboxSourceTwitter' in formData:
        twitterResult = searchTwitter(formData)

        if isinstance(twitterResult, pd.DataFrame):
            dataArray.append(twitterResult)
        else:
            errorList.append(twitterResult)

    if 'checkboxSourceReddit' in formData:
        redditResult = searchReddit(formData)

        if isinstance(redditResult, pd.DataFrame):
            dataArray.append(redditResult)
        else:
            errorList.append(redditResult)

    if len(errorList) > 0 and len(errorList) == NUMBER_OF_SOURCES:
        return errorList

    return pd.concat(dataArray).sample(n = int(formData['inputLimit']))

def searchTwitter(formData):
    consumer_key = os.environ.get('TWITTER_API_KEY')
    consumer_secret = os.environ.get('TWITTER_API_KEY_SECRET')
    access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

    if None in [consumer_key, consumer_secret, access_token, access_token_secret]:
        return 'Could not find authentications for the Twitter API'

    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        tweepyAPI = tweepy.API(auth, wait_on_rate_limit = True)

        qtd = int(formData['inputLimit'])

        tweets = tweepy.Cursor(
            tweepyAPI.search,
            q = str(formData['inputKeyword']),
            lang = 'en',
            count = qtd,
            result_type = 'recent',
            # until = 'YYYY-MM-DD', # Keep in mind that the search index has a 7-day limit. In other words, no tweets will be found for a date older than one week.
            include_entities = False,
        ).items(qtd)

        tweetsList = [[tweet.created_at, tweet.user.screen_name, tweet.text] for tweet in tweets]
        dfTweepy = pd.DataFrame(tweetsList, columns=['Created At', 'Name', 'Text'])
        dfTweepy['Created At'] = pd.to_datetime(dfTweepy['Created At']).dt.date
        dfTweepy['Source'] = 'Twitter'

        return dfTweepy
    except:
        return 'Could not retrieve data via Twitter API'


def searchReddit(formData):
    client_id = os.environ.get('REDDIT_CLIENT_ID')
    client_secret = os.environ.get('REDDIT_SECRET')

    if None in [client_id, client_secret]:
        return 'Could not find authentications for the Reddit API'

    try:
        reddit = praw.Reddit(
            client_id = client_id,
            client_secret = client_secret,
            user_agent = "tcc-bi-master-0.1"
        )

        submissions = reddit.subreddit('wallstreetbets').search(
            str(formData['inputKeyword']),
            sort = 'new',
            limit = int(formData['inputLimit']),
            time_filter='week'
        )

        prawRows = [[submission.created_utc, submission.author, submission.title] for submission in submissions]
        dfPraw = pd.DataFrame(prawRows, columns = ['Created At', 'Name', 'Text'])
        dfPraw['Created At'] = dfPraw['Created At'].apply(lambda row: datetime.fromtimestamp(row))
        dfPraw['Created At'] = pd.to_datetime(dfPraw['Created At']).dt.date
        dfPraw['Source'] = 'Reddit'

        return dfPraw
    except:
        return 'Could not retrieve data via Reddit API'