from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from tweets import get_tweets
from process import get_processed
from features import get_features
from learn import get_accuracy
from learn import get_classifications
import json


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
    features = get_features(processed, options)
    return jsonify(features=features)

@app.route('/_learn')
def _learn():
    features = json.loads(request.args.get('features'))
    options = json.loads(request.args.get('options'))
    choices = json.loads(request.args.get('choices'))
    metrics = get_accuracy(choices)
    return jsonify(metrics=metrics)

@app.route('/_test')
def _test():
    classifications = get_classifications(json.loads(request.args.get('tweets')))
    return jsonify(classifications=classifications)

@app.route('/_report')
def _report():
    report = "report of comparisons"
    return jsonify(report=report)

if __name__ == '__main__':
	app.run(debug=True)














