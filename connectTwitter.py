from keys import retrieveKeys
from twython import Twython

def connectTwitter():
	auth = retrieveKeys()

	print 'Authenticating with Twitter... ', 
	twitter = Twython(auth['APP_KEY'], auth['APP_SECRET'])

	if twitter:
		print 'Authenticated.'
	else:
		sys.exit('Error with Twitter API')

	return twitter