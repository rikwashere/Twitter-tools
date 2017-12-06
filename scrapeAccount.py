from twython.exceptions import TwythonError
from connectTwitter import connectTwitter
import time
import json
import sys

def crawlAccount(target):
	""" crawl targeted twitter account, save tweets to csv """

	# connect Twitter api
	twitter = connectTwitter()	
	try:
		user_timeline = twitter.get_user_timeline(screen_name=target, count=200, include_rts=False, exclude_replies=False)
	except TwythonError:
		sys.exit('Received 404 for %s. Account does not exist or is banned.' % target)
	
	user_timeline = twitter.get_user_timeline(screen_name=target, count=200, include_rts=True, exclude_replies=False)	
	tweets = []
	ids = []


	# stop this loop
	while len(set(ids)) == len(ids):
		for tweet in user_timeline:
			ids.append(tweet['id'])			
			tweets.append(tweet)
			with open('data/%s-tweets.json' % target, 'a') as json_out:
				json.dump(tweet, json_out)
				json_out.write('\n')

		print 'Found %i tweets so far. %i unique.' % (len(ids), len(set(ids)))
		
		time.sleep(5)
		user_timeline = twitter.get_user_timeline(screen_name=target, count=200, max_id=min(ids) - 1, include_rts=True, exclude_replies=False)	
	else:
		sys.exit('No new tweets found. Ending scraper.')
	
if __name__ == "__main__":
	if len(sys.argv) > 1:
		crawlAccount(sys.argv[1])
	else:
		target = raw_input('Crawl what account?\n> ')
		crawlAccount(target)