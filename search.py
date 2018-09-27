from connectTwitter import connectTwitter
import time

def searchTwitter(target):
	twitter = connectTwitter()

	response = twitter.search(q='@%s' % target, count=100, )
	results = []
	ids = []

	while response['search_metadata'].has_key('next_results'):
		if response.has_key('statuses'):

			for tweet in response['statuses']:
				ids.append(tweet['id'])
				results.append(tweet)
			
		print 'Crawled %i tweets, %i unique.' % (len(ids), len(set(ids)))

		response = twitter.search(q='@%s' % target, count=100, max_id=min(ids))

		time.sleep(2)
	return results

if __name__ == '__main__':
	target = raw_input('Crawl recent search results for what account?\n> ')
	results = searchTwitter('target')
	