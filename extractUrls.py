from collections import Counter
from urlparse import urlparse
import datetime
import unicodecsv as csv
import json
import sys
import re

class Tweet():
    def __init__(self, tweet):
        self.text = tweet['text']
        self.id = tweet['id']
        self.retweet_count = tweet['retweet_count']
        self.favorite_count = tweet['favorite_count']
        self.created_at = tweet['created_at']
        self.screen_name = tweet['user']['screen_name'].lower()
        self.followers_count = tweet['user']['followers_count']
        self.iso_datetime = datetime.datetime.strptime(self.created_at, "%a %b %d %H:%M:%S +0000 %Y")

        if tweet.has_key('entities'):
        	entities = tweet['entities']
        	if entities.has_key('urls'):
        		self.urls = [url['expanded_url'] for url in entities['urls']]
        		self.has_url = True
        		self.domains = [urlparse(url).netloc for url in self.urls]

    def build_url(self):
    	return 'twitter.com/%s/status/%i' % (self.screen_name, self.id)


def extractUrls(fo):
	with open(fo, 'r') as fo:
		data = [json.loads(line) for line in fo]

	tweets = []

	for tweet in data:
		tweets.append(Tweet(tweet))
	
	urls = []
	for tweet in tweets:
		if tweet.has_url == True:
			for url in tweet.urls:
				urls.append(urlparse(url).netloc)
	print 'Processing %i tweets' % len(tweets)	
	return tweets

def search(queries, tweets):
	matches = []
	for query in queries:
		for tweet in tweets:
			if re.search(query, tweet.text):
				matches.append(tweet)
	
	print 'Found %i matches.' % len(matches)
	
	with open('tweets-%s-matched-%s.csv' % (tweets[0].screen_name, '-'.join(queries)), 'a') as csv_out:
		writer = csv.writer(csv_out, delimiter='\t')
		for match in matches:
			writer.writerow([match.iso_datetime, match.text, match.build_url()])
				
		

if __name__ == "__main__":
	if len(sys.argv) > 1:
		tweets = extractUrls(sys.argv[1])
	else:
		target = raw_input('Extract urls from which tweet file?\n> ')
		tweets = extractUrls(target)