# split sentences and return list of words
def get_unigrams(input_list):
    words_list = [i.split() for i in input_list]
    return words_list

# return n-grams from unigram list
def find_ngrams(input_list, n):
    ngrams = zip(*[input_list[i:] for i in range(n)])
    return ngrams

# return bigrams from unigram list via find_ngrams
def get_bigrams(unigrams_list):
    bigrams = [find_ngrams(i, 2) for i in unigrams_list]
    return bigrams

# return dictionary of word list with bool values
def compare_to_word_list(unigrams_list):
    word_list = ['good', 'bad', 'neutral']
    vectors = []
    for i, words in enumerate(unigrams_list):
        vector = {}
        for word in words:
            if (word in word_list):
                vector[word] = True
            else:
                vector[word] = False
        vectors.append(vector)
    return vectors


def get_features(processed, options):
    features = []
    unigrams = get_unigrams(processed)
    for option in options:
        if (option == 'unigrams'):
            features = unigrams
        if (option == 'bigrams'):
            features = get_bigrams(unigrams)
        if (option == 'wordlist'):
            features = compare_to_word_list(unigrams)
    return features

