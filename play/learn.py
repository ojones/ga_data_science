import pickle, json, os
import urllib
# import urllib.request
# with urllib.request.urlopen(myurl) as f:
#     myfile = pickle.load(f)


def get_saved_classifier():
	opener = urllib.URLopener()
	myurl = "https://s3-us-west-2.amazonaws.com/ozclassifiers/web_classifier.p"
	print(" ")
	print("please work damnit")
	print(" ")
	myfile = opener.open(myurl)
    clf = None
    try:
    	clf = myfile
    except Exception as e:
    	print(e)
    	print("what the fuck ever")
    print("----------")
    return clf
    # return joblib.load(web_classfier_file_path)

def get_accuracy(choices):

	classifier = get_classifier(choices)

	metrics = {
		'accuracy': classifier + ' accuracy'
		, 'pos_fmeasure': classifier + ' pos_fmeasure'
		, 'neg_fmeasure': classifier + ' neg_fmeasure'
	}

	return metrics

def get_classifications(tweets):
	print('tweets')
	print(tweets)

	print('start retreiving')
	classifier = get_saved_classifier()

	print("classifications: ")
	classifications = classifier.predict(tweets).tolist()
	print(classifications)

	return classifications