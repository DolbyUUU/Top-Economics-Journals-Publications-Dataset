import pandas as pd
import nltk
import os
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter

# Download the stopwords from nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

# Load the excel file
df = pd.read_excel('english_journals.xlsx')

stop_words = set(stopwords.words('english'))

# Function to clean text
def clean_text(text):
    text = text.lower()  # convert text to lowercase
    text = ''.join(c for c in text if not c.isdigit())  # remove digits
    text = ''.join(c for c in text if c.isalpha() or c.isspace())  # remove punctuation
    text = ' '.join(word for word in text.split() if word not in stop_words)  # remove stopwords
    text = ' '.join(word for word in text.split() if len(word) > 1)  # remove single characters
    return text

# Clean the titles
df['TITLE'] = df['TITLE'].apply(clean_text)

# Create directory for wordcloud images
os.makedirs('popular_topics_en', exist_ok=True)

# Group the data by year and concatenate all titles in each year
grouped_by_year = df.groupby('YEAR')['TITLE'].apply(lambda x: ' '.join(x)).reset_index()

# Get the popular keywords from 2020 and 2021
keywords_2020_2021 = []
for index, row in grouped_by_year.iterrows():
    if row["YEAR"] in [2020, 2021]:
        keywords_2020_2021.extend(row['TITLE'].split())

# Get the top 100 most common words in 2020 and 2021
common_words_2020_2021 = [word for word, word_count in Counter(keywords_2020_2021).most_common(100)]

# Iterate through each year
for index, row in grouped_by_year.iterrows():
    if row["YEAR"] in [2022, 2023]:
        # Generate word cloud
        wordcloud = WordCloud(width = 1000, height = 500, stopwords=common_words_2020_2021 + list(STOPWORDS)).generate(row['TITLE'])
        
        # Plot the wordcloud
        plt.figure(figsize=(15,8))
        plt.imshow(wordcloud)
        plt.axis("off")
        
        # Save the image
        plt.savefig(f'emerging_topics_en/wordcloud_{row["YEAR"]}.png', bbox_inches='tight')
        plt.close()