import json
from ast import literal_eval

from flask import Flask
from flask_cors import CORS
from flask import request
import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()
# s = sid.polarity_scores(sentence)

app = Flask(__name__)
CORS(app)
list_videoid = []
list_comments = []
list_sentiment = []


def bestVideoFinder():
    df = pd.DataFrame(list(zip(list_videoid, list_comments, list_sentiment)),
                      columns=['videoid', 'comment', 'sentiment'])
    # print(df)
    df.to_excel('youtube-comments.xlsx')
    g = df.groupby('videoid')
    total = g.count().comment
    sum = g.sum('sentiment')
    no_comments = list(g.count()['comment'])
    new = (total + sum['sentiment']) / 2
    final = list(g.groups.keys())

    abc = new / no_comments
    df2 = pd.DataFrame(list(zip(final, new, abc)), columns=['id', 'pos', 'ratio'])
    max = df2['ratio'].max()

    for index, row in df2.iterrows():
        print(row['id'], row['ratio'])
        if row['ratio'] == max:
            return row['id']

    return "no best video found"


@app.route("/")
def home():
    return "Hello, World!"


# comments = []
@app.route("/sentiment", methods=['POST'])
def sentiment():
    comments = request.data
    comments = literal_eval(comments.decode('utf8'))
    comments = json.dumps(comments, indent=4, sort_keys=True)
    comments = json.loads(comments)
    print(type(comments))
    print(comments)
    for com in comments:
        list_videoid.append(com['id'])
        list_comments.append(com['comment'])
        ans = sid.polarity_scores(com['comment'])
        if ans['compound'] > 0:
            list_sentiment.append(1)
        else:
            list_sentiment.append(-1)

    return bestVideoFinder()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
