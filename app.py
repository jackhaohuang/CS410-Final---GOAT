from flask import Flask, request, jsonify
import wikipediaapi
import spacy
# Other necessary imports...
import wikipediaapi
import nltk
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import spacy
from collections import Counter
from flask_cors import CORS, cross_origin
import os

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
nltk.download('punkt')
nltk.download('stopwords')

nlp = spacy.load("en_core_web_md")

app = Flask(__name__)
CORS(app)

LINKS = []
TEST = ""

@app.route('/query_course', methods=['POST'])
@cross_origin()
def query_course():
    data = request.json
    course_title = data.get("course_title")
    course_description = data.get("course_description")

    if not course_title or not course_description:
        return jsonify({"error": "Course title and description are required"}), 400

    keywords = extract_keywords(course_title, course_description)
    wikipedia_links = query_wikipedia(keywords)

    if not wikipedia_links:
        keywords = extract_keywords_with_spacy(course_title, course_description)
        wikipedia_links = query_wikipedia(keywords)

    return jsonify({
        "keywords": keywords,
        "wikipedia_links": wikipedia_links
    })

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

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": LINKS})

if __name__ == '__main__':
    app.run()
