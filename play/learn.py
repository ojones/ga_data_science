import pickle, json, os
import urllib
opener = urllib.URLopener()
myurl = "https://s3-us-west-2.amazonaws.com/ozclassifiers/web_classifier.p"
myfile = opener.open(myurl)
# import urllib.request
# with urllib.request.urlopen(myurl) as f:
#     myfile = pickle.load(f)
# from sklearn.externals import joblib

# web_classfier_file_path = 'data/classifiers/me_uni_pp_100' 
web_classfier_file_path = '/app/play/data/web_classifier.p'  
web_classfier_file_path2 = 'data/web_classifier.p'  


def get_saved_classifier():
    # print(os.getcwd())
    # os.chdir(os.path.dirname(__file__))
    # print(os.getcwd())
    # print("++++++++++")
    # print("1" + str(os.path.isfile(web_classfier_file_path)))
    # print("2" + str(os.path.isfile(web_classfier_file_path2)))
    # with open(web_classfier_file_path, 'rb') as f:
    # 	print("this part works")
    # 	print("======================")
    clf = None
    try:
    	clf = myfile # pickle.load(myfile) #open(web_classfier_file_path, 'rb'))
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