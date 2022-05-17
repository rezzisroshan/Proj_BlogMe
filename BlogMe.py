import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Importing the data
data = pd.read_excel('articles.xlsx')

# Finding out the total number of sources
sources = data.groupby('source_name').count()
data.groupby(['source_name'])['engagement_reaction_count'].sum()

# Removing a column
data = data.drop('engagement_comment_plugin_count',axis=1)

# Function for flagging a specific keyword in the 'Title' column
def keywordflag(keyword):
    flag = []
    length = len(data)
    for h in range(0,length):
        try:
            heading = data['title'][h]
            if keyword in heading:
                flag.append(1)
            else:
                flag.append(0)
        except:
            flag.append(0)
    return flag

# Checking how many titles have 'murder' in them    
column_flag = keywordflag('murder')

# Adding the keyword flag column to data
data['Keyword Flag']= pd.Series(column_flag)

# Initialization
vader = SentimentIntensityAnalyzer()

positive_sentiment = []
negative_sentiment = []
neutral_sentiment = []
text = []

lenn = len(data)

# Loop for finding out the sentiment scores of each title 
for x in range(0,lenn):
    try:
        text = data['title'][x]
        sent = vader.polarity_scores(text)
        positive_sentiment.append(sent['pos'])
        negative_sentiment.append(sent['neg'])
        neutral_sentiment.append(sent['neu'])
    except:
        positive_sentiment.append(0)
        negative_sentiment.append(0)
        neutral_sentiment.append(0)

# Adding the sentiment value columns to the data
positive_sentiment = pd.Series(positive_sentiment)
negative_sentiment = pd.Series(negative_sentiment)
neutral_sentiment = pd.Series(neutral_sentiment) 
      
data['Positive sentiment'] = positive_sentiment
data['Negative sentiment'] = negative_sentiment
data['Neutral sentiment'] = neutral_sentiment

# Exporting to Excel
data.to_excel('BlogMe_cleaned.xlsx', sheet_name='BlogMeData', index=False)
