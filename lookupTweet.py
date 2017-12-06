from twython.exceptions import TwythonError
from connectTwitter import connectTwitter
import sys

def lookup_tweet(id_str):
	twitter = connectTwitter()
	
	try:
		tweet = twitter.show_status(id=id_str)
		print tweet['text']
	except TwythonError as e:
		print e

	return

def lookup_tweets(ids_list):
	twitter = connectTwitter()

	for chunk in chunks(ids_list):
		tweets = twitter.show_status(id=', '.join(chunk))

		for tweet in tweets:
			print tweet['text']

def chunks(l, n):
	for i in range(0, len(l), n):
		yield l[i:i + n]
	
if __name__ == "__main__":
	if len(sys.argv) > 1:
		lookup_tweet(sys.argv[1])
	else:
		while True:
			target = raw_input('Lookup which tweet?\n> ')
			lookup_tweet(target)

