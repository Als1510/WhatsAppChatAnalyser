

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

# for english text
# test_subset is list of words
def word_polarity(test_subset):
    pos_word_list=[]
    neg_word_list=[]

    for word in test_subset:               
        testimonial = TextBlob(word)
        if testimonial.sentiment.polarity >= 0.5:
            pos_word_list.append(word)
        elif testimonial.sentiment.polarity <= -0.5:
            neg_word_list.append(word)
    return pos_word_list, neg_word_list      

# word_polarity(['20170412', 'great', 'bad', 'terrible', 'dog', 'stop', 'good'])

def text_transformation(words_list):
    corpus = []
    for item in words_list:
        new_item = re.sub('[^a-zA-Z]',' ',str(item))
        new_item = new_item.lower()
        if 'https://' in new_item:
            pass
        new_item = new_item.split()
        for i in new_item:
            corpus.append(i)
    return list(set(corpus))

words_sheet = pd.read_csv('Words.csv')
X = words_sheet['Word']
y = words_sheet['Label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

corpus = text_transformation(X_train)
# train
cv = CountVectorizer(ngram_range=(1,2))
traindata = cv.fit_transform(X_train)
X = traindata
y = y_train
rfc = RandomForestClassifier()
rfc.fit(X,y)

# test data
testdata = cv.transform(X_test)
predictions = rfc.predict(testdata)
acc_score = accuracy_score(y_test,predictions)
# print(acc_score)

# working with real data
# converting the messages to words_list
def messages_to_list(df):
    test_df = df[df['User']!='group_notification']
    test_df = test_df[test_df['Message']!='<Media omitted> ']
    test_df = test_df[test_df['Message']!='This message was deleted'] 
    messages = ''
    for i in test_df['Message']:
        messages+=i
    message_words_list = text_transformation(messages.split())
    return message_words_list

message_list = messages_to_list(df)
# print(rfc.predict(cv.transform(message_list)))

# rfc.predict(cv.transform(['bura']))
# array([0], dtype=int64) (this was the output)