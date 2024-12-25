import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load data from Excel file
df = pd.read_excel('chinese_journals.xlsx', engine='openpyxl')

# Convert AUTHOR column to string
df['AUTHORS'] = df['AUTHORS'].astype(str)

# Split authors and flatten the list
authors = [author for sublist in df['AUTHORS'].apply(lambda x: x.split('，')).tolist() for author in sublist]

# Remove Chinese comma sign and any white spaces
authors = [author.replace('，', '').strip() for author in authors]

# Calculate frequencies
author_freq = Counter(authors)

# Sort authors by frequency
sorted_authors = sorted(author_freq.items(), key=lambda item: item[1], reverse=True)

# Print authors with frequencies greater than or equal to 3
for author, freq in sorted_authors:
    if freq >= 3:
        print(f'{author}: {freq}')

# Generate word cloud
wordcloud = WordCloud(font_path='C:/Windows.old/Windows/Fonts/simhei.ttf', background_color='white').generate_from_frequencies(author_freq)

# Display the word cloud
plt.imshow(wordcloud, interpolation='bilinear')
plt.title('Word Cloud of Authors')
plt.axis('off')

# Save the word cloud as an image
plt.savefig('author_popular_wordcloud_cn.png', dpi=300, bbox_inches='tight')