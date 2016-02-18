import tweepy

API_KEY = "JjH4MLuHrBIGL9QkJPckblw7j"
API_SECRET = "XSXfA8dBo7qCapfavfriLK72TrP5DcwMqcHzYxO36b03wjRS2N"
ACCESS_TOKEN = "1207732448-b5DoyY1CfiKTiNiE4YMKQ2wsG7C1iaGvgCnObk7"
ACCESS_TOKEN_SECRET = "khnI0gPE5Ey6PqFKyeWZlPc5snVg8b4AAmfxkVFEgm3Ly"

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

def get_raw_tweets(query):
	max_tweets = 5
	searched_tweets = [status for status in tweepy.Cursor(api.search, q=query, lang="en").items(max_tweets)]
	return searched_tweets

def get_just_tweets(tweetObjects):
	justTweets = []
	for obj in tweetObjects:
		justTweets.append(obj.text)
	return justTweets

def get_tweets(keywords):
	raw_tweets = get_raw_tweets(keywords)
	just_tweets = get_just_tweets(raw_tweets)
	return just_tweets