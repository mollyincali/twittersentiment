"""
exploring 2.8 millions customer support tweets
functions for graphing results 
"""
import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()

def make_hist(df1, df2):
    fig, ax = plt.subplots(figsize = (20,10))
    
    ax.hist(df1['compound'], bins = 50, 
            alpha = 0.8, label = 'Customer Message1', color='royalblue')
    ax.hist(df2['compound'], bins = 50, 
            alpha = 0.4, label = 'Customer Message2', color='green')
    ax.set_title('Compound Score of Tweet', fontsize=30)
    ax.set_ylabel('Number of Tweets', fontsize = 20)
    ax.set_xlabel('Compound Score', fontsize = 20)
    plt.legend()
    plt.show();

def make_date_line(company_df, customer_df, graph = None):
    comp_dates = company_df.created_at.dt.date
    cus_dates = customer_df.created_at.dt.date
    
    comp_dates = comp_dates.value_counts().reset_index().sort_values(by = 'index')
    cus_dates = cus_dates.value_counts().reset_index().sort_values(by = 'index')

    if graph == None:
        fig, ax = plt.subplots(figsize = (20, 10))
        ax.scatter(comp_dates['index'], comp_dates['created_at'], color = 'royalblue')
        ax.scatter(cus_dates['index'], cus_dates['created_at'], color = 'green')
        ax.set_title('Number of Tweets by Day', fontsize=30)
        ax.set_ylabel('Number of Tweets', fontsize = 20)
        ax.set_xlabel('Date', fontsize = 20)
        plt.show();
    
    else:
        cus_dates['date'] = pd.to_datetime(cus_dates['index'])
        comp_dates['date'] = pd.to_datetime(comp_dates['index'])
        
        cus_dates2 = cus_dates[cus_dates['date'] > '2017-08-31']
        comp_dates2 = comp_dates[comp_dates['date'] > '2017-08-31']

        fig, ax = plt.subplots(figsize = (20, 10))
        ax.scatter(comp_dates2['index'], comp_dates2['created_at'], 
                    color = 'royalblue', label = 'Company')
        ax.scatter(cus_dates2['index'], cus_dates2['created_at'], 
                    color = 'green', label = 'Customer')
        ax.set_title('Number of Tweets by Day', fontsize=30)
        ax.set_ylabel('Number of Tweets', fontsize = 20)
        ax.set_xlabel('Date', fontsize = 20)
        ax.legend()
        plt.show();

def top_word_bar(tuple_list, title):
    words = []
    num = []
    
    for i in tuple_list[::-1]:
        words.append(i[0])
        num.append(i[1])

    fig, ax = plt.subplots(figsize = (20, 10))
    ax.barh(words, np.array(num), color = 'royalblue')
    ax.set_title(f'{title}', fontsize = 30)
    ax.set_yticklabels(words, fontsize = 15)
    ax.set_xlabel('Number of Occurrences', fontsize = 20)
    ax.set_ylabel('Top Words', fontsize = 20)
    plt.show()

if __name__ == "__main__":
    pass