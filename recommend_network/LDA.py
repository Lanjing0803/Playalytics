import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim.corpora import Dictionary
from gensim.models import LdaModel

#first clean the dataset
file_path = 'dataset/steam_store_data_2024.csv'
df = pd.read_csv(file_path)
df = df.dropna(subset=['allReviews'])
positive_reviews_df = df[df['allReviews'].str.contains('Positive')]
description_column = positive_reviews_df[['description']]
description_column.to_csv('dataset/positive_reviews_descriptions.csv', index=False)

#then analyze the topics in descriptions
df = pd.read_csv('dataset/positive_reviews_descriptions.csv')
custom_stop_words = {'new', 'take', 'game','world','ever','play','critically','final','acclaimed','featuring',}
stop_words = set(stopwords.words('english'))
stop_words.update(custom_stop_words)
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(str(text).lower())  
    tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return tokens


df['tokens'] = df['description'].apply(preprocess_text)

dictionary = Dictionary(df['tokens'])

# Filter out words here (custmoize as needed)
dictionary.filter_extremes(no_below=6, no_above=0.5)
corpus = [dictionary.doc2bow(tokens) for tokens in df['tokens']]
num_topics =3  
lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)

for topic_id, topic_words in lda_model.print_topics():
    print(f'Topic {topic_id}: {topic_words}')



