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
    
    # 3. Word cloud
    visualizations.append(create_word_cloud(transcript))
    
    return visualizations

def get_word_frequency(text):
    words = re.findall(r'\b\w+\b', text.lower())
    stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
    words = [word for word in words if word not in stop_words and len(word) > 3]
    return Counter(words).most_common(10)

def create_word_frequency_chart(word_freq):
    words, counts = zip(*word_freq)
    plt.figure(figsize=(12, 6))
    plt.bar(words, counts)
    plt.title('Top 10 Most Frequent Words')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    
    return save_plot_to_base64('Word Frequency Chart', 'Shows the most frequently used words in the podcast.')

def extract_topics(summary):
    # This is a simple implementation. In a real-world scenario, you might want to use
    # more advanced NLP techniques like topic modeling (e.g., LDA)
    topics = re.findall(r'(?<=\n)[^:\n]+(?=:)', summary)
    return Counter(topics)

def create_topic_distribution_chart(topics):
    plt.figure(figsize=(10, 10))
    plt.pie(topics.values(), labels=topics.keys(), autopct='%1.1f%%', startangle=90)
    plt.title('Topic Distribution')
    
    return save_plot_to_base64('Topic Distribution', 'Shows the distribution of main topics discussed in the podcast.')

def create_word_cloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud')
    
    return save_plot_to_base64('Word Cloud', 'Visual representation of the most prominent words in the podcast.')

def save_plot_to_base64(title, description):
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return {
        'title': title,
        'imageUrl': f'data:image/png;base64,{image_base64}',
        'description': description
    }