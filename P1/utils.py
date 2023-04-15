"""Todo lo necesario para poder cargar el modelo Joblib"""

import joblib
import numpy as np
import pandas as pd
from langdetect import detect
import unicodedata
import re
import inflect
from joblib import Parallel, delayed
import os

import nltk
from nltk.stem import SnowballStemmer
from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.metrics import classification_report

class TextPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.stemmer = SnowballStemmer('spanish')
        self.p = inflect.engine()

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        num_processes = os.cpu_count() or 2
        X_split = np.array_split(X, num_processes)
        X_processed = pd.concat(Parallel(n_jobs=num_processes)(delayed(self.process_data)(split) for split in X_split))
        return X_processed

    def fit_transform(self, X, y=None):
        self.fit(X, y)
        return self.transform(X)
    
    def process_data(self, data):
        data_stemmed = data.apply(self.porter_stemmer_spanish)
        data_processed = data_stemmed.apply(self.preprocessing_parallel)
        data_processed = data_processed.apply(self.join_words)
        return data_processed

    def porter_stemmer_spanish(self, text):
        return [self.stemmer.stem(word) for word in text.split()]

    def join_words(self, words):
        return ' '.join(words)

    def remove_non_ascii(self, words):
        """Remove non-ASCII characters from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            new_words.append(new_word)
        return new_words

    def to_lowercase(self, words):
        """Convert all characters to lowercase from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = word.lower()
            new_words.append(new_word)
        return new_words

    def remove_punctuation(self, words):
        """Remove punctuation from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = re.sub(r'[^\w\s]', '', word)
            if new_word != '':
                new_words.append(new_word)
        return new_words

    def replace_numbers(self, words):
        """Replace all integer occurrences in list of tokenized words with textual representation"""
        new_words = []
        for word in words:
            if word.isdigit():
                new_word = self.p.number_to_words(word)
                new_words.append(new_word)
            else:
                new_words.append(word)
        return new_words

    def preprocessing_parallel(self, words):
        words = self.to_lowercase(words)
        words = self.replace_numbers(words)
        words = self.remove_punctuation(words)
        words = self.remove_non_ascii(words)
        return words
