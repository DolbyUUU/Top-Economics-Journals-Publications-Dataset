import os
import numpy as np
import pandas as pd
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag
from nltk.corpus import stopwords
from gensim.models import Phrases
from gensim.models.phrases import Phraser

# Download the necessary NLTK data
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

stop_words = set(stopwords.words('english'))

lemmatizer = WordNetLemmatizer()

# Function to convert nltk tag to wordnet tag
def nltk_tag_to_wordnet_tag(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:          
        return None

# Function to lemmatize text based on POS tagging
def lemmatize_text(text):
    nltk_tagged = pos_tag(nltk.word_tokenize(text))  
    wordnet_tagged = map(lambda x: (x[0], nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
    lemmatized_words = []
    for word, tag in wordnet_tagged:
        if tag is not None:
            lemmatized_words.append(lemmatizer.lemmatize(word, tag))
        else:
            lemmatized_words.append(word)
    return " ".join(lemmatized_words)

# Function to clean text
def clean_text(text):
    text = text.lower()  # convert text to lowercase
    text = ''.join(c for c in text if not c.isdigit())  # remove digits
    text = ''.join(c for c in text if c.isalpha() or c.isspace() or c == '_')  # remove punctuation
    text = ' '.join(word for word in text.split() if word not in stop_words)  # remove stopwords
    text = ' '.join(word for word in text.split() if len(word) > 2)  # remove words with fewer than 3 characters
    text = lemmatize_text(text)  # lemmatize text
    return text

# Load the excel file
df = pd.read_excel('english_journals.xlsx')

# Convert titles to a list of words
titles_words = [title.split() for title in df['TITLE']]

# Train a bigram detector
phrases = Phrases(titles_words, min_count=1, threshold=1)
bigram = Phraser(phrases)

# Apply the trained Phraser to the titles
df['TITLE'] = df['TITLE'].apply(lambda x: ' '.join(bigram[x.split()]))

# Clean the titles
df['TITLE'] = df['TITLE'].apply(clean_text)

# Create directory for wordcloud images
os.makedirs('popular_topics_en', exist_ok=True)

# Initialize the CountVectorizer and fit to the entire corpus
count_vectorizer = CountVectorizer(stop_words=stop_words, max_df=0.7)
count_vectorizer.fit(df['TITLE'])

def create_wordcloud(grouped_data, group_name):
    # Iterate through each group
    for index, row in grouped_data.iterrows():
        # Transform the text for this group
        count_matrix = count_vectorizer.transform([row['TITLE']])

        # Get feature names and count scores
        feature_names = count_vectorizer.get_feature_names_out()
        count_scores = count_matrix.toarray()[0]

        # Create a dictionary of words and their count scores
        word_scores = dict(zip(feature_names, count_scores))

        # Generate word cloud
        wordcloud = WordCloud(width=1000, height=500).generate_from_frequencies(word_scores)

        # Plot the wordcloud
        plt.figure(figsize=(15,8))
        plt.imshow(wordcloud)
        plt.axis("off")

        # Save the image
        plt.savefig(f'popular_topics_en/wordcloud_{group_name}_{row[group_name]}.png', bbox_inches='tight')
        plt.close()

# Group the data by year and concatenate all titles in each year
grouped_by_year = df.groupby('YEAR')['TITLE'].apply(lambda x: ' '.join(x)).reset_index()

# Create word clouds by year
create_wordcloud(grouped_by_year, 'YEAR')

# Group the data by journal and concatenate all titles in each journal
grouped_by_journal = df.groupby('JOURNAL')['TITLE'].apply(lambda x: ' '.join(x)).reset_index()

# Create word clouds by journal
create_wordcloud(grouped_by_journal, 'JOURNAL')
