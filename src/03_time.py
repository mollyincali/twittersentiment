"""
exploring 2.8 millions customer support tweets
analysis of response time from company
"""
import pandas as pd 
import numpy as np
from graphing import * 

def get_time_df(cust_sent1, company):
    """[summary]
    Args:
        cust_sent1 [dataframe]
        company [dataframe]
    Returns:
        [dataframe] with how many minutes company took took to respond to message1
    """
    #get tweet_id of message1
    message1_id = list(cust_sent1['tweet_id'])
    #only get responses that are to message1
    comp_response = company[company['in_response_to_tweet_id'].isin(message1_id)] 
    #some companies have multiple responses, want first
    comp_response = company.groupby('in_response_to_tweet_id').agg({'created_at':'min', 'author_id':'min'}).reset_index()

    time = pd.merge(cust_sent1, comp_response, how = 'inner', left_on = 'tweet_id', right_on = 'in_response_to_tweet_id')
    time['created_at_y'] = time['created_at_y'].dt.tz_localize(None)
    time['diff'] = time['created_at_y'] - time['created_at_x']
    time['diffmin'] = time['diff'].astype('timedelta64[m]')
    
    avg_comp_response = time.groupby('author_id').agg({"diffmin":"mean"}).reset_index()
    return time_df, avg_comp_response

def get_message2(cust_sent2):
    mess2_tweets = list(cust_sent2.tweet_id) 
    mess2 = company[company['in_response_to_tweet_id'].isin(mess2_tweets)][['author_id','in_response_to_tweet_id']] 
    mess2 = pd.merge(cust_sent2, mess2, how = 'inner', left_on = 'tweet_id', right_on = 'in_response_to_tweet_id') 
    message2 = sent_mess2.groupby('author_id').agg({'compound':'mean'}).reset_index()
    return message2

if __name__ == "__main__":
    #-- DF SETUP
    cust_sent1 = pd.read_json("../data/custsent1.json")
    cust_sent2 = pd.read_json("../data/custsent2.json")
    company = pd.read_json('../data/company.json')
    cust = pd.read_json('../data/customer.json')
    
    time, avg_comp_response = get_time_df(cust_sent1, company)
    message2 = get_message2(cust_sent2)

    #-- GRAPH
    company_time_compound(avg_comp_response, message2)

    top10 = ['AmazonHelp', 'AppleSupport', 'Uber_Support', 'SpotifyCares', 'Deblta', 
            'Tesco', 'AmericanAir', 'TMobileHelp', 'comcastcares', 'British_Airways']
    

