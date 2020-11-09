'''
sentiment analysis class
'''
import pandas as pd 

class VaderSentiment():
    ''' label tweet as negative, neutral, or positive and produce a compound float '''
    def __init__(self):
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        self.vader = SentimentIntensityAnalyzer()

    def predict(self, df):
        ''' return new dataframe with prediction columns on tweet '''
        sentiment_df = pd.DataFrame(columns = ['neg','neu','pos', 'compound', 'tweet_id'])
        total = 0
        for row, tweet in enumerate(df['text']):
            prob = self.vader.polarity_scores(tweet)
            sentiment_df = sentiment_df.append({'neg':prob['neg'], 'neu':prob['neu'],
                                'pos':prob['pos'], 'compound':prob['compound'], 
                                'tweet_id':df.iloc[row, 2]}, ignore_index=True)
            total += 1
            if total % 50000 == 0:
                print(f'{total} rows complete')
        return sentiment_df

if __name__ == "__main__":
    pass