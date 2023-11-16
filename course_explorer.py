import wikipediaapi
import nltk
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import spacy
from collections import Counter


# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Tokenize
    tokens = word_tokenize(text.lower())

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    # Stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]

    return stemmed_tokens

def extract_keywords(text, num_keywords=5):
    # Consider unigrams, bigrams, and trigrams in the vectorizer
    vectorizer = TfidfVectorizer(ngram_range=(1, 3))
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_array = vectorizer.get_feature_names_out()
    tfidf_sorting = tfidf_matrix.toarray().argsort()[0][::-1]

    # Select top n keywords/phrases
    top_keywords = [feature_array[i] for i in tfidf_sorting[:num_keywords * 3]]  # Increase pool size for filtering

    # Rank keywords by length (number of words)
    ranked_keywords = sorted(top_keywords, key=lambda x: len(x.split()), reverse=True)

    # Filter out redundant keywords
    final_keywords = []
    for keyword in ranked_keywords:
        if not any(keyword in other_keyword for other_keyword in final_keywords if keyword != other_keyword):
            final_keywords.append(keyword)
            if len(final_keywords) == num_keywords:
                break

    return final_keywords

def extract_keywords_with_spacy(title, description, num_keywords=5):
    combined_text = title + ". " + description
    # Load a pre-trained spaCy model
    nlp = spacy.load("en_core_web_sm")  # or "en_core_web_md" for more accuracy
    doc = nlp(description)

    # Extract phrases and entities
    phrases = [chunk.text for chunk in doc.noun_chunks]
    entities = [ent.text for ent in doc.ents]
    combined_terms = phrases + entities

    # Count and rank terms
    term_freq = Counter(combined_terms)
    most_common_terms = term_freq.most_common(num_keywords * 2)  # Increase pool size for filtering

    # Filter terms based on Wikipedia page existence
    valid_terms = []
    for term, _ in most_common_terms:
        if is_valid_wikipedia_page(term) and term not in valid_terms:
            valid_terms.append(term)
            if len(valid_terms) == num_keywords:
                break

    return valid_terms

def query_wikipedia(keywords, lang='en'):
    user_agent = "CS410 Course Explorer Project/0.1 (thomas1031@163.com)"
    wiki_wiki = wikipediaapi.Wikipedia(language=lang, user_agent=user_agent)
    pages = []

    for keyword in keywords:
        page = wiki_wiki.page(keyword)
        if page.exists():
            pages.append(page.fullurl)

    return pages

def is_valid_wikipedia_page(title, lang='en'):
    user_agent = "CS410 Course Explorer Project/0.1 (thomas1031@163.com)"
    wiki_wiki = wikipediaapi.Wikipedia(language=lang, user_agent=user_agent)
    page = wiki_wiki.page(title)
    return page.exists()

# Example usage

course_description = "Introduction to artificial intelligence and machine learning. Topics include neural networks, deep learning, and natural language processing."

course_title = "Deep Learning for Computer Vision"
course_description_2 = "Provides an elementary hands-on introduction to neural networks and deep learning with an emphasis on computer vision applications. Topics include: linear classifiers; multi-layer neural networks; back-propagation and stochastic gradient descent; convolutional neural networks and their applications to object detection and dense image labeling; recurrent neural networks and state-of-the-art sequence models like transformers; generative adversarial networks and variational autoencoders for image generation; and deep reinforcement learning. Coursework will consist of programming assignments in a common deep learning framework."

# Preprocess the text
processed_text = ' '.join(preprocess_text(course_description_2))

# Extract keywords
keywords = extract_keywords(processed_text)
keywords_spacy = extract_keywords_with_spacy(course_title, course_description_2)

# Query Wikipedia
wikipedia_links = query_wikipedia(keywords)
wikipedia_links_spacy = query_wikipedia(keywords_spacy)

print("Keywords:", keywords)
print("Keywords (SpaCy):", keywords_spacy)
print("Wikipedia Links:", wikipedia_links)
print("Wikipedia Links (SpaCy):", wikipedia_links_spacy)

