"""
exploring 2.8 millions customer support tweets
statistical analysis on sentiment of tweets
comparing customers first message to a company to their message after company responds 
"""
import pandas as pd 
import numpy as np
from scipy.stats import ttest_ind
from sentiment import *
from graphing import *

def test_int(s):
    """Converts string to int
    Args:
        [string]
    Returns:
        [bool]
    """
    try: 
        int(s)
        return True
    except ValueError:
        return False

def cust_comp_df():
    """ Create customer and company dataframes
    Args:
        None
    Returns:
        [dataframe]: Dataframe of company tweets
        [dataframe]: Dataframe of customer tweets
    """
    t['customer'] = None
    for row, author in enumerate(t['author_id']):
        t_or_f = test_int(author)
        t.at[row, 'customer'] = t_or_f

    company = t[t['customer'] == False]
    customer = t[t['customer'] == True]

    return company, customer

def make_start():
    """ Create dataframe of very first tweet from customer to company and get tweet id
    Args:
        None
    Returns:
        start_df [dataframe]: Dataframe of first tweets
        start_id [array]: Array of unique tweet_id 
    """
    start_df = t[t['in_response_to_tweet_id'].isnull()] 
    start_id = np.array(start_df['tweet_id'])
    return start_df, start_id

def get_tweet_id(company_df, company_response, start_id):
    """[summary]

    Args:
        company_df [dataframe]: Masked dataframe of only company 
        company_response [array]: Array of all tweet_ids from a company
        start_id [array]: Array of tweet_id that start a conversation

    Returns:
        [array]: Array of twee_id message 1 from 
        [array]: Array of tweet_id with company response to message 1
        [array]: Array of tweet_id message 2 from customer
    """
    #Find intersection of start_id and company_response
    cust_message1 = np.intersect1d(company_response, start_id)

    #Make dataframe of company responses to message 1 and remove na values
    df = company_df[company_df['in_response_to_tweet_id'].isin(cust_message1)]
    df1 = df[~df['response_tweet_id'].isna()]
    
    #unpack response_tweet_id, is a list of strings in a variety of lengths 
    cmessage2 = []
    cmessage2_fix = []
    #create two lists: int and list of int
    for t_id in df1['response_tweet_id']:
        if t_id != None and ',' not in t_id:
            cmessage2.append(int(t_id))
        if t_id != None and ',' in t_id:
            cmessage2_fix.append(t_id)
    
    #unpack the list of tweet_id
    for num in cmessage2_fix:
        lst = num.split(',')
        for n in lst:
            cmessage2.append(int(n))
    
    #turn into array of numbers 
    cust_message1 = np.array(df1['in_response_to_tweet_id'])
    company_outreach1 = np.array(df1['tweet_id']) 
    cust_message2 = np.array(cmessage2)
    return cust_message1, company_outreach1, cust_message2

def df_for_sent(tweet_ids):
    """ Return a dataframe ready for sentiment analysis
    Args:
        [array]: Array of unique tweet_id
    Returns:
        [dataframe]: Dataframe of information needed for sentiment analysis
    """
    return t[t['tweet_id'].isin(tweet_ids)][['text', 'tweet_id', 'created_at']].reset_index()

if __name__ == '__main__':
    #-- SET UP DATAFRAMES
    t = pd.read_csv('../data/twcs.csv')
    start_df, start_id = make_start()

    # Use below to START
    # company_df, customer_df = cust_comp_df()
    # customer_df = pd.to_json('../data/customer.json')
    # company_df = pd.to_json('../data/company.json')    

    # Use below after initial run
    customer_df = pd.read_json('../data/customer.json')
    company_df = pd.read_json('../data/company.json')

    #--- GET TWEET_ID
    company_response = np.array(company_df['in_response_to_tweet_id'])
    cust_message1, comp_message1, cust_message2 = get_tweet_id(company_df, company_response, start_id)

    #-- GET TWEETS_TEXT
    cust_df1 = df_for_sent(cust_message1)
    comp_df1 = df_for_sent(comp_message1)
    cust_df2 = df_for_sent(cust_message2)

    #-- SENTIMENT OF TWEETS
    sent = VaderSentiment()
    cust_sent1 = sent.predict(cust_df1)  
    cust_sent2 = sent.predict(cust_df2) 
    # cust_sent1.to_json('../data/custsent1.json')
    # cust_sent2.to_json('../data/custsent2.json')   

    #-- GRAPH
    make_hist(cust_sent1, cust_sent2)
    make_date_line(company_df, customer_df)
    make_date_line(company_df, customer_df, 2)
