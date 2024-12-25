import pandas as pd
import nltk
import os
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

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

# Iterate through each year
for index, row in grouped_by_year.iterrows():
    # Generate word cloud
    wordcloud = WordCloud(width = 1000, height = 500).generate(row['TITLE'])
    
    # Plot the wordcloud
    plt.figure(figsize=(15,8))
    plt.imshow(wordcloud)
    plt.axis("off")
    
    # Save the image
    plt.savefig(f'popular_topics_en/wordcloud_{row["YEAR"]}.png', bbox_inches='tight')
    plt.close()

# Group the data by journal and concatenate all titles in each journal
grouped_by_journal = df.groupby('JOURNAL')['TITLE'].apply(lambda x: ' '.join(x)).reset_index()

# Iterate through each journal
for index, row in grouped_by_journal.iterrows():
    # Generate word cloud
    wordcloud = WordCloud(width = 1000, height = 500).generate(row['TITLE'])
    
    # Plot the wordcloud
    plt.figure(figsize=(15,8))
    plt.imshow(wordcloud)
    plt.axis("off")
    
    # Save the image
    plt.savefig(f'popular_topics_en/wordcloud_{row["JOURNAL"].replace("/", "-")}.png', bbox_inches='tight') # replace / with - in file name
    plt.close()