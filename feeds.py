from newsapi import NewsApiClient
import tweepy
import datetime as dt
import pandas as pd

auth = tweepy.OAuthHandler(
    'sTdMg4nUSf4brak6uuBOZJg4M',
    'b8WQYukt00Kgl6kdTxMnx4OVlCTcD28EtsT4d2X9SOb9JomuRK')
auth.set_access_token('1392363164-8tTU3tZByrZKVg2Sq7DP7kDSaN9CKkYkJGXhpzw',
                      'woxdgDzBQ568OqGHXoItQCrs29d3LvtkZ7drL89WdX23e')

newsapi = NewsApiClient(api_key='22b35c71e16d41e5856cd1c78f7e132f')



def refresh_news(query, source):
    sources = newsapi.get_sources()
    source_df = pd.DataFrame(data=sources['sources'])
    source_df.columns = ['source_id', 'name', 'description', 'homepage', 'category', 'language', 'country']
    top_headlines = newsapi.get_top_headlines(
        q=query,
        sources=source,
    )
    news_data = []
    for news in top_headlines['articles']:
        data = {
            'source_id': news['source']['id'],
            'source_name': news['source']['name'],
            'title': news['title'],
            'desc': news['description'],
            'url': news['url'],
            'img': news['urlToImage'],
            'published': news['publishedAt']
        }
        news_data.append(data)
    news_df = pd.DataFrame(news_data)
    news_df = pd.merge(news_df,source_df,on='source_id')
    news_df.sort_values(by='published', ascending=False)
    news_json = news_df.to_dict(orient='records')
    return news_json


def refresh_tweets():
    api = tweepy.API(auth)

    public_tweets = api.search(q=['COVID-19'],
                               lang='en',
                               result_type='recent',
                               count=10,
                               tweet_mode='extended')
    tweet_data = []
    for tweet in public_tweets:
        data = {
            'created_at': (tweet.created_at + dt.timedelta(hours=7)).strftime('%A %d %B %Y | %H:%M GMT+7'),
            'tweet': tweet.full_text,
            'username': '@' + tweet.user.screen_name,
            'name': tweet.user.name,
            'pic': tweet.user.profile_image_url_https
        }
        tweet_data.append(data)
    return tweet_data
