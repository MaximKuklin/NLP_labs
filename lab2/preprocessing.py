from pymystem3 import Mystem
from nltk.tokenize import sent_tokenize
import nltk
from nltk.corpus import stopwords

stopwords.words("russian")
import re
import string
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import json
from tqdm import tqdm
from random import shuffle
from nltk.corpus import stopwords

# nltk.download('punkt')
# nltk.download('russian')


LABELS = {
    'ekonomika': 0,
    'kultura': 1,
    'obschestvo': 2,
    'politika': 3
}

STOP_WORDS = stopwords.words('russian')


def split_on_sentences(text) -> list:
    return sent_tokenize(text, language='russian')


def lemmatize_text(text, mystem=None):
    if mystem is None:
        mystem = Mystem()

    text = nltk.word_tokenize(text)
    lemmas = [mystem.lemmatize(word)[0] for word in text]
    # text = ' '.join(lemmas)
    return lemmas


def delete_punctuation(text):
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    return regex.sub("", text)


def filter_stop_words(lemmas):
    filtered = [word for word in lemmas if word not in STOP_WORDS]
    return filtered


def filter_text(text):
    document = re.sub(r'\W', ' ', text)

    # remove all single characters
    document = re.sub(r'\s+[а-яА-Я]\s+', ' ', document)

    # Remove single characters from the start
    document = re.sub(r'\^[а-яА-Я]\s+', ' ', document)

    # Substituting multiple spaces with single space
    document = re.sub(r'\s+', ' ', document, flags=re.I)

    # Removing prefixed 'b'
    document = re.sub(r'^b\s+', '', document)

    # Remove digits from text
    # document = re.sub(" \d+", "", document)

    # Converting to Lowercase
    document = document.lower()

    return document


def preprocess(text, **kwargs):
    text = delete_punctuation(text)
    text = filter_text(text)

    lemmas = lemmatize_text(text, **kwargs)
    filtered_lemmas = filter_stop_words(lemmas)

    text = ' '.join(filtered_lemmas[4:])

    return text


def parse_data(json_path='../lab1/parsed_news_kuklin_maxim.json'):
    mystem = Mystem()

    texts = []
    labels = []

    with open(json_path, 'r') as f:
        data = json.load(f)['catalog']

    for element in tqdm(data):
        text = element['text']
        category = element['category']

        if category in LABELS.keys():
            texts.append(preprocess(text, mystem=mystem))
            labels.append(LABELS[category])

    return texts, labels


def vectorize_texts(texts, test=False):

    if test:
        tfIdfVectorizer = TfidfVectorizer()
        vectors = tfIdfVectorizer.fit_transform(texts)
    else:
        tfIdfVectorizer = TfidfVectorizer()
        vectors = tfIdfVectorizer.transform(texts)

    return vectors
