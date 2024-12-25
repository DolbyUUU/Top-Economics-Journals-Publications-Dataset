import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load data from Excel file
df = pd.read_excel('chinese_journals.xlsx', engine='openpyxl')

# Convert AUTHOR column to string
df['AUTHORS'] = df['AUTHORS'].astype(str)

# Split data by year
df_2020_2021 = df[df['YEAR'].isin([2020, 2021])]
df_2022_2023 = df[df['YEAR'].isin([2022, 2023])]

# Generate list of authors for each period
authors_2020_2021 = [author for sublist in df_2020_2021['AUTHORS'].apply(lambda x: x.split('，')).tolist() for author in sublist]
authors_2022_2023 = [author for sublist in df_2022_2023['AUTHORS'].apply(lambda x: x.split('，')).tolist() for author in sublist]

# Remove Chinese comma sign and any white spaces
authors_2020_2021 = set([author.replace('，', '').strip() for author in authors_2020_2021])
authors_2022_2023 = [author.replace('，', '').strip() for author in authors_2022_2023]

# Get only the authors that appeared in 2022 and 2023 but not in 2020 and 2021
emerging_authors = [author for author in authors_2022_2023 if author not in authors_2020_2021]

# Calculate frequencies
emerging_author_freq = Counter(emerging_authors)

# Sort authors by frequency
sorted_emerging_authors = sorted(emerging_author_freq.items(), key=lambda item: item[1], reverse=True)

# Print authors with frequencies greater than or equal to 2
for author, freq in sorted_emerging_authors:
    if freq >= 2:
        print(f'{author}: {freq}')

# Generate word cloud
wordcloud = WordCloud(font_path='C:/Windows.old/Windows/Fonts/simhei.ttf', background_color='white').generate_from_frequencies(emerging_author_freq)

# Display the word cloud
plt.imshow(wordcloud, interpolation='bilinear')
plt.title('Word Cloud of Emerging Authors')
plt.axis('off')

# Save the word cloud as an image
plt.savefig('author_emerging_wordcloud_cn.png', dpi=300, bbox_inches='tight')