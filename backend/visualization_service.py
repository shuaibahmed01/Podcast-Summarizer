import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg' before importing pyplot
import matplotlib.pyplot as plt
import io
import base64
from collections import Counter
import re
from wordcloud import WordCloud
import numpy as np

def generate_visualizations(transcript, summary):
    visualizations = []
    
    # 1. Word frequency chart
    word_freq = get_word_frequency(transcript)
    visualizations.append(create_word_frequency_chart(word_freq))
    
    # 2. Topic distribution pie chart
    topics = extract_topics(summary)
    visualizations.append(create_topic_distribution_chart(topics))
    

    
    return visualizations

def get_word_frequency(text):
    words = re.findall(r'\b\w+\b', text.lower())
    stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
    words = [word for word in words if word not in stop_words and len(word) > 3]
    return Counter(words).most_common(10)

def create_word_frequency_chart(word_freq):
    words, counts = zip(*word_freq)
    plt.figure(figsize=(8, 5))  # Reduced size and DPI
    plt.bar(words, counts)
    plt.title('Top 10 Most Frequent Words', fontsize=10)
    plt.xlabel('Words', fontsize=8)
    plt.ylabel('Frequency', fontsize=8)
    plt.xticks(rotation=45, ha='right', fontsize=6)
    plt.yticks(fontsize=6)
    plt.tight_layout()
    
    return save_plot_to_base64('Word Frequency Chart', 'Shows the most frequently used words in the podcast.')

def extract_topics(summary):
    topics = re.findall(r'(?<=\n)[^:\n]+(?=:)', summary)
    return Counter(topics)

def create_topic_distribution_chart(topics):
    plt.figure(figsize=(8,8))  # Reduced size and DPI
    plt.pie(topics.values(), labels=topics.keys(), autopct='%1.1f%%', startangle=90, textprops={'fontsize': 6})
    plt.title('Topic Distribution', fontsize=10)
    plt.tight_layout()
    
    return save_plot_to_base64('Topic Distribution', 'Shows the distribution of main topics discussed in the podcast.')


def save_plot_to_base64(title, description):
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.1)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return {
        'title': title,
        'imageUrl': f'data:image/png;base64,{image_base64}',
        'description': description
    }