import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

# Load stopwords from file
with open('chinese_stopwords.txt', 'r', encoding='utf-8') as f:
    stopwords_file = f.read().splitlines()

# Define the set of words to exclude
stopwords_additional = ['本文', '文章', '影响', '效应', '作用', '经济', 
    '研究', '发现', '分析', '模型', '数据', '问题', '理论', '实证', '政策', 
    '效应', '方法', '探讨', '讨论', '因素', '结论', '建议', '提出', '结果', 
    '市场', '关系', '降低', '提高', '上升', '下降', '提升', '减低', '增长', 
    '增加', '基于', '来自', '视角', '证据', '中国', '我国', '专题', 
    '五', '六', '七', '八', '九', '十']

# Merge the two stopword lists
stopwords = set(stopwords_file + stopwords_additional)

# Load data from Excel file
df = pd.read_excel('chinese_journals.xlsx', engine='openpyxl')

# Convert ABSTRACT, TITLE, and KEYWORDS columns to string
df['ABSTRACT'] = df['ABSTRACT'].astype(str)
df['TITLE'] = df['TITLE'].astype(str)
df['KEYWORDS'] = df['KEYWORDS'].astype(str)

# Remove punctuation, whitespace, and other non-Chinese characters
df['cleaned_abstracts'] = df['ABSTRACT'].str.replace('[^\u4e00-\u9fa5]', '', regex=True)
df['cleaned_titles'] = df['TITLE'].str.replace('[^\u4e00-\u9fa5]', '', regex=True)

# Segment words and remove stopwords
df['segmented_abstracts'] = df['cleaned_abstracts'].apply(lambda x: ' '.join([word for word in jieba.cut(x) if word not in stopwords]))
df['segmented_titles'] = df['cleaned_titles'].apply(lambda x: ' '.join([word for word in jieba.cut(x) if word not in stopwords]))
df['keywords_list'] = df['KEYWORDS'].apply(lambda x: ' '.join([word for word in x.split('；') if word not in stopwords]))

# Filter for years 2020-2023
df = df[df['YEAR'].between(2020, 2023)]

# Define the dictionary of words to translate
translations = {'经济研究': 'Economic Research Journal', '经济学（季刊）': 'China Economic Quarterly', '世界经济': 'The Journal of World Economy'}

# Function to generate and save word cloud
def generate_word_cloud(data, title):
    wordcloud = WordCloud(font_path='C:/Windows.old/Windows/Fonts/simhei.ttf', background_color='white').generate(' '.join(data))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    # Replace the Chinese words in the title with their English translations
    for chinese, english in translations.items():
        title = title.replace(chinese, english)

    # Define the directory for the images
    img_dir = "popular_topics_cn"
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)

    plt.title(f'Word Cloud for {title}')
    plt.savefig(f'{img_dir}/wordcloud_{title}.png', dpi=300, bbox_inches='tight')
    plt.clf()

# Generate word clouds for each year
for year in range(2020, 2024):
    generate_word_cloud(df[df['YEAR'] == year]['segmented_abstracts'], f'Abstract of Year {year}')
    generate_word_cloud(df[df['YEAR'] == year]['segmented_titles'], f'Title of Year {year}')
    generate_word_cloud(df[df['YEAR'] == year]['keywords_list'], f'Keywords of Year {year}')

# Generate word clouds for each journal
for journal in df['JOURNAL'].unique():
    generate_word_cloud(df[df['JOURNAL'] == journal]['segmented_abstracts'], f'Abstract of {journal}')
    generate_word_cloud(df[df['JOURNAL'] == journal]['segmented_titles'], f'Title of {journal}')
    generate_word_cloud(df[df['JOURNAL'] == journal]['keywords_list'], f'Keywords of {journal}')