import re

def strip_punctuation(tweet):
    tweet ="".join(c for c in tweet if c not in ('!','.','"','\'', '-'))
    return tweet


def pre_process(tweets):
    # lower case
    tweets = [i.lower() for i in tweets]
    # remove punctuation
    tweets = [strip_punctuation(i) for i in tweets]
    # remove additional white spaces
    tweets = [re.sub('[\s]+', ' ', i) for i in tweets]
    #look for 2 or more repetitions of character and replae with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    tweets = [pattern.sub(r"\1\1", i) for i in tweets]
    #check if the word starts with an alphabet
    #val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
    return tweets

def replace_urls(tweets):
    tweets = [re.sub('((mailto\:|(news|(ht|f)tp(s?))\://){1}\S+)','URL',i) for i in tweets]
    return tweets

def replace_unames(tweets):
    tweets = [re.sub('@[^\s]+','AT_USER',i) for i in tweets]
    return tweets

def replace_hashtags(tweets):
    tweets = [re.sub(r'#([^\s]+)', r'\1',i) for i in tweets]
    return tweets

def process(tweets, options):
    for option in options:
        if (option == 'urls'):
            tweets = replace_urls(tweets)
        if (option == 'unames'):
            tweets = replace_unames(tweets)
        if (option == 'hashtags'):
            tweets = replace_hashtags(tweets)
    return tweets


def get_processed(tweets, options):
    pre_processed = pre_process(tweets)
    processed = process(pre_processed, options)
    return processed