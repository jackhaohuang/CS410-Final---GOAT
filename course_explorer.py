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

# Load a pre-trained spaCy model with word vectors
nlp = spacy.load("en_core_web_md")  # Using medium model for better accuracy

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

course_title = "Deep Learning for Computer Vision"
course_description = "Provides an elementary hands-on introduction to neural networks and deep learning with an emphasis on computer vision applications. Topics include: linear classifiers; multi-layer neural networks; back-propagation and stochastic gradient descent; convolutional neural networks and their applications to object detection and dense image labeling; recurrent neural networks and state-of-the-art sequence models like transformers; generative adversarial networks and variational autoencoders for image generation; and deep reinforcement learning. Coursework will consist of programming assignments in a common deep learning framework."



def extract_keywords(title, description, num_keywords=5):
    title_doc = nlp(title)
    description_doc = nlp(description)

    # Use noun chunks for more contextual relevance
    noun_chunks = [chunk for chunk in description_doc.noun_chunks if chunk.text.lower() not in title_doc.text.lower()]

    # Calculate similarity scores
    similarity_scores = {chunk.text: title_doc.similarity(chunk) for chunk in noun_chunks}

    # Sort chunks by similarity score
    sorted_keywords = sorted(similarity_scores, key=similarity_scores.get, reverse=True)

    return sorted_keywords[:num_keywords]


keywords = extract_keywords(course_title, course_description)
wikipedia_links = query_wikipedia(keywords)

print("Keywords:", keywords)
print("Wikipedia Links:", wikipedia_links)