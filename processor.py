from bs4 import BeautifulSoup
import pandas as pd
import json
import sys

def to_df(file):
	# load json
	tweets = json.load(open(file, 'r'))
	tweet_dicts = []

	for tweet in tweets:
		tweet_dict = {
						'created_at' : tweet['created_at'],
						'id' : tweet['id_str'],
						'text' : tweet['text'],
						'client': BeautifulSoup(tweet['source'], 'html.parser').text,
						'screen_name' : tweet['user']['screen_name'],
						'userid' : tweet['user']['id_str'],
						'quote_count' : tweet['qoute_count'] if tweet.has_key('quote_count') else 0,
						'reply_count' : tweet['reply_count'] if tweet.has_key('reply_count') else 0,
						'retweet_count' : tweet['retweet_count'],
						'favorite_count' : tweet['favorite_count'],
						'tweet_type' : 'status_update'
					}

		if tweet.has_key('quoted_status'):
			tweet_dict['tweet_type'] = 'quote'
			tweet_dict['tweet_quoted_status'] = tweet['quoted_status']['id']
		elif tweet.has_key('retweeted_status'):
			tweet_dict['tweet_type'] = 'retweet'
			tweet_dict['tweet_retweeted_status'] = tweet['retweeted_status']['id_str']
			tweet_dict['tweet_retweeted_user'] = tweet['retweeted_status']['user']['screen_name']
		if tweet['in_reply_to_status_id_str']:
			tweet_dict['tweet_type'] = 'reply'
			tweet_dict['tweet_replied_to_tweet'] = tweet['in_reply_to_status_id_str']
			tweet_dict['tweet_replied_to_user'] = tweet['in_reply_to_screen_name']

		entities = tweet['entities']

		if len(entities['hashtags']) > 0:
			tweet_dict['hashtags'] = [h['text'] for h in entities['hashtags']]
		if len(entities['urls']) > 0:
			tweet_dict['urls'] = [url['expanded_url'] for url in entities['urls']]
		if len(entities['user_mentions']) > 0:	
			tweet_dict['mentions'] = [u['screen_name'] for u in entities['user_mentions']]

		tweet_dicts.append(tweet_dict)

	df = pd.DataFrame(tweet_dicts)
	df.index = pd.to_datetime(df.created_at)

	return df


if __name__ == '__main__':
	if len(sys.argv) > 1:
		target = sys.argv[1]
	else:
		target = raw_input('Load which Twitter file in a DataFrame?\n> ')

	df = to_df(target)