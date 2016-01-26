import pickle, json

web_classfier_file_path = 'data/classifiers/me_uni_pp_100' 

def get_saved_classifier():
    f = open(web_classfier_file_path, 'rb')
    data = pickle.load(f)
    f.close()
    return data

def get_accuracy(choices):

	classifier = get_classifier(choices)

	metrics = {
		'accuracy': classifier + ' accuracy'
		, 'pos_fmeasure': classifier + ' pos_fmeasure'
		, 'neg_fmeasure': classifier + ' neg_fmeasure'
	}

	return metrics

def get_classifications(tweets):
	print 'tweets'
	print tweets

	print 'start retreiving'
	classifier = get_saved_classifier()

	print "classifications: "
	classifications = classifier.predict(tweets).tolist()
	print classifications

	return classifications