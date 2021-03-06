from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import json
import os

from play.tweets import get_tweets
from play.process import get_processed
from play.features import get_features
from play.learn import get_classifications



app = Flask(__name__)

@app.route('/')
def play():
	return render_template("index.html")

@app.route('/_query')
def _query():
    keywords = request.args.get('keywords', "default", type=str)
    tweets = get_tweets(keywords)
    return jsonify(tweets=tweets)

@app.route('/_process')
def _process():
    tweets = json.loads(request.args.get('tweets'))
    options = json.loads(request.args.get('options'))
    processed = get_processed(tweets, options)
    return jsonify(processed=processed)

@app.route('/_features')
def _features():
    processed = json.loads(request.args.get('processed'))
    options = json.loads(request.args.get('options'))
    features = [list(x) for x in get_features(processed, options)]
    return jsonify(features=list(features))

@app.route('/_learn')
def _learn():
    features = json.loads(request.args.get('features'))
    options = json.loads(request.args.get('options'))
    choices = json.loads(request.args.get('choices'))
    # decided to retrieve this data using javascript instead
    # metrics = get_accuracy(choices)
    # return jsonify(metrics=metrics)

@app.route('/_test')
def _test():
    tweets = json.loads(request.args.get('tweets'))
    print("tweets loaded")
    classifications = get_classifications(tweets)
    print("classifications loaded")
    return jsonify(classifications=classifications)

@app.route('/_report')
def _report():
    report = "report of comparisons"
    return jsonify(report=report)

if __name__ == '__main__':
	app.run(debug=True)














