import pickle, json, os
# from sklearn.externals import joblib

# web_classfier_file_path = 'data/classifiers/me_uni_pp_100' 
web_classfier_file_path = '/app/play/data/web_classifier.p'  
web_classfier_file_path2 = 'data/web_classifier.p'  
web_classfier_file_path3 = 'play/data/web_classifier.p' 


def get_saved_classifier():
    # f = open(web_classfier_file_path, 'rb')
    # data = pickle.load(f)
    # f.close()
    # return data
    print(os.getcwd())
    os.chdir(os.path.dirname(__file__))
    print(os.getcwd())
    print("++++++++++")
    print("1" + str(os.path.isfile(web_classfier_file_path)))
    print("2" + str(os.path.isfile(web_classfier_file_path2)))
    print("3" + str(os.path.isfile(web_classfier_file_path3)))
    clf = pickle.load(open(web_classfier_file_path, 'rb'))
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