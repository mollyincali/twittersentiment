"""
exploring 2.8 millions customer support tweets
text analysis on tweets
"""
import pandas as pd 
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

def create_stop_words():
    """ Create unique list of stop words
    Args:
        None
    Returns:
        [list]: Unique list of stop words
    """
    stop_words = stopwords.words('english') 
    additional_stop_words = ['https', 'co', '115821', '115850', '115830', '115913', 'de', 'amp',
                            'applesupport', 'amazonhelp', 'uber_support', 'americanair', 'tmobilehelp']
    for word in additional_stop_words:
        stop_words.append(word)
    return stop_words

def get_top_words(corpus, stop_words, n, ngram = (1, 1)):
    """ Use CountVectorizer to get top n words from tweet list
    Args:
        corpus [list]: List of tweets
        stop_words [list]: List of stop words to remove
        n [int]: Number of words to return 
    Returns:
        [list]: List of top n frequently used words
    """
    vec = CountVectorizer(lowercase = True, strip_accents = 'ascii', stop_words = stop_words, ngram_range=ngram)
    bow = vec.fit_transform(corpus)
    sum_words = bow.sum(axis = 0)
    word_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    word_freq = sorted(word_freq, key = lambda x: x[1], reverse = True)
    return word_freq[:n]

if __name__ == '__main__':
    #-- SET UP
    stop_words = create_stop_words()
    cust_sent1 = pd.read_json('../data/custsent1.json')
    cust_sent2 = pd.read_json('../data/custsent2.json')
    
    #-- GET TOP WRODS
    cus1 = get_top_words(cust_sent1['text'], stop_words, 10)
    cus2 = get_top_words(cust_sent2['text'], stop_words, 10)
    cus1bi = get_top_words(cust_sent1['text'], stop_words, 10, (2,2))
    cus2bi = get_top_words(cust_sent2['text'], stop_words, 10, (2,2))

    #-- GRAPH
    top_word_bar(cus1bi, 'Top Bigrams in Customer Message1')
    top_word_bar(cus2bi, 'Top Bigrams in Customer Message2')
    top_word_bar(cus1, 'Top Words in Customer Message1')
    top_word_bar(cus2, 'Top Words in Customer Message2')