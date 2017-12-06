from connectTwitter import connectTwitter
import sys

def lookup_user(user):
	twitter = connectTwitter()
	user = twitter.lookup_user(id=user)
	print user['screen_name']

	
if __name__ == "__main__":
	if len(sys.argv) > 1:
		lookup_user(sys.argv[1])
	else:
		while True:
			target = raw_input('Lookup which user?\n> ')
			lookup_user(target)

