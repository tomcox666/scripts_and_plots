import os
import re
from collections import Counter
import plotly.express as px
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, SnowballStemmer
import textract
import langid
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Function to read text from a file
def read_text_from_file(file_path):
    try:
        text = textract.process(file_path).decode('utf-8')
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""
    return text

# Function to read text from user input
def read_text_from_user():
    text = input("Enter the text: ")
    return text

# Function to detect the language of the text
def detect_language(text):
    lang, confidence = langid.classify(text)
    return lang

# Function to preprocess the text
def preprocess_text(text, lang):
    # Convert the text to lowercase
    text = text.lower()
    
    # Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text)
    
    # Tokenize the text into words
    words = text.split()
    
    # Remove numbers
    words = [word for word in words if not word.isdigit()]
    
    # Remove stopwords
    stop_words = set(stopwords.words(lang))
    words = [word for word in words if word not in stop_words]
    
    # Stem or lemmatize the words
    if lang == 'english':
        lemmatizer = WordNetLemmatizer()
        words = [lemmatizer.lemmatize(word) for word in words]
    else:
        stemmer = SnowballStemmer(lang)
        words = [stemmer.stem(word) for word in words]
    
    return words

# Function to calculate the frequency of each word
def calculate_word_frequencies(words):
    word_freq = Counter(words)
    return word_freq

# Function to find the most common words
def find_most_common_words(word_freq, n):
    most_common = word_freq.most_common(n)
    return most_common

# Function to generate a Plotly wordcloud
def generate_word_cloud(word_freq, color_scheme):
    fig = px.treemap(
        names=list(word_freq.keys()),
        parents=[''] * len(word_freq),
        values=list(word_freq.values()),
        color_discrete_sequence=getattr(px.colors.sequential, color_scheme),
        hover_name=list(word_freq.keys()),
        hover_data={'Frequency': list(word_freq.values())},
    )
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    fig.show()

# Function to generate a WordCloud wordcloud
def generate_wordcloud_wordcloud(word_freq):
    wordcloud = WordCloud(width=800, height=400, random_state=21, max_font_size=110).generate_from_frequencies(word_freq)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()

# Main function
def main():
    choice = input("Do you want to read text from a file (1) or enter it manually (2)? ")
    
    if choice == '1':
        files = os.listdir()
        for i, file in enumerate(files):
            print(f"{i+1}. {file}")
        
        file_index = int(input("Enter the number of the file to read: ")) - 1
        file_path = files[file_index]
        text = read_text_from_file(file_path)
    elif choice == '2':
        text = read_text_from_user()
    else:
        print("Invalid choice. Exiting.")
        return
    
    lang = detect_language(text)
    words = preprocess_text(text, lang)
    word_freq = calculate_word_frequencies(words)
    most_common = find_most_common_words(word_freq, 10)
    
    print("Most common words:")
    for word, freq in most_common:
        print(f"{word}: {freq}")
    
    print("Choose a color scheme:")
    color_schemes = ['Spectral', 'Rainbow', 'YlGnBu', 'YlOrRd', 'Blues', 'Reds', 'Greens', 'Purples', 'Oranges']
    for i, scheme in enumerate(color_schemes):
        print(f"{i+1}. {scheme}")
    
    color_choice = int(input("Enter the number of the color scheme: ")) - 1
    color_scheme = color_schemes[color_choice]

    choice = input("Do you want to generate a Plotly wordcloud (1), a WordCloud wordcloud (2), or both (3)? ")

    if choice == '1':
        generate_word_cloud(word_freq, color_scheme)
    elif choice == '2':
        generate_wordcloud_wordcloud(word_freq)
    elif choice == '3':
        generate_word_cloud(word_freq, color_scheme)
        generate_wordcloud_wordcloud(word_freq)
    else:
        print("Invalid choice. Exiting.")
        return

if __name__ == "__main__":
    main()