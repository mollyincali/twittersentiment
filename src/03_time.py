"""
exploring 2.8 millions customer support tweets
analysis of response time from company
"""
import pandas as pd 
import numpy as np
from graphing import * 

def get_time_df(cust_sent1, company):
    """ Get time dataframe and average company response
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
    return time, avg_comp_response.sort_values(by = 'diffmin', inplace = True)


if __name__ == "__main__":
    #-- DF SETUP
    cust_sent1 = pd.read_json("../data/custsent1.json")
    company = pd.read_json('../data/company.json')
    time, avg_comp_response = get_time_df(cust_sent1, company)

    #-- TOP10 COMPANIES 
    top10 = company.groupby('author_id').agg({'tweet_id':'count'}).sort_values(by = 'tweet_id', ascending = False)[:10]
    top10_df = avg_comp_response[avg_comp_response['author_id'].isin(top10.index)]

    #-- GRAPHS
    company_response_time(avg_comp_response) 
    company_response_time(top10_df, xlabel=True)

    

