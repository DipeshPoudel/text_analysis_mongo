import os
from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem import WordNetLemmatizer
from helpers import pymongo_get_database
from helpers import ini_config_reader

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

config = ini_config_reader.read_config()
tweet_topic = config['topic_config']['topic_title']
db_name = pymongo_get_database.get_database()
collection_name = db_name[f'cleaned_tweet_{tweet_topic}']

app = Dash(__name__)

fetched = collection_name.find()
pre_text = ''.join([text_data['cleaned_tweet_text'] for text_data in fetched])
new_tokens = word_tokenize(pre_text)
new_tokens = [t.lower() for t in new_tokens]
new_tokens = [t for t in new_tokens if t not in stopwords.words('english')]
new_tokens = [t for t in new_tokens if t.isalpha()]
lemmatizer = WordNetLemmatizer()
new_tokens = [lemmatizer.lemmatize(t) for t in new_tokens]

# counts the words, pairs and trigrams
counted = Counter(new_tokens)

# creates 3 data frames and returns thems
word_freq = pd.DataFrame(counted.items(), columns=['word', 'frequency']).sort_values(by='frequency', ascending=False)
fig1 = px.bar(word_freq.head(30), x="word", y="frequency")
app.layout = html.Div(children=[
    html.H1(children='Text Analysis'),
    html.H2(children='Most Frequent Words'),
    html.Div(children='''
        Word Frequency Count
    '''),

    dcc.Graph(
        id='word-frequency',
        figure=fig1
    )
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
