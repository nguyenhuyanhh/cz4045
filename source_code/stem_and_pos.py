"""Stemming and POS tagging."""

import itertools
import os
import random
import re
from collections import Counter

import nltk
import pandas as pd

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
RAW_DIR = os.path.join(CUR_DIR, 'raw_data')


def stem_and_pos():
    """Stemming and POS tagging for the dataset."""
    # read data
    data = pd.read_csv(os.path.join(RAW_DIR, 'QueryResults.csv'))

    # sentence tokenize
    sent_tokenized_data = [nltk.sent_tokenize(
        re.sub(r"<.*?>", r"", i)) for i in data.iloc[:, 3]]

    # word tokenize each row without removing punctuations
    tokenized_data = [nltk.word_tokenize(i[0]) for i in sent_tokenized_data]

    # POS tagging
    pos_tagged = nltk.pos_tag_sents(tokenized_data)
    print(random.sample(pos_tagged, 10))

    # word tokenize each row
    tokenized_data = [[re.sub(r"[^\w\s]", r"", j) for j in nltk.word_tokenize(
        i[0])] for i in sent_tokenized_data]

    # remove stopwords
    no_stopwords = [[word for word in sent if word not in nltk.corpus.stopwords.words(
        'english')] for sent in tokenized_data]

    # Stemming data
    stemmed_data = [[nltk.stem.PorterStemmer().stem(word) for word in sent]
                    for sent in no_stopwords]

    # count words before stem
    temporary = list(itertools.chain.from_iterable(no_stopwords))
    counted = Counter(temporary)
    print(counted.most_common(21))

    # count words after stem
    temporary = list(itertools.chain.from_iterable(stemmed_data))
    counted = Counter(temporary)
    all_words = counted.most_common(21)
    print(all_words)

    # find original words that stemmed to "all"
    original_words = []
    for i in range(21):
        original_words.append([])
        for sent in no_stopwords:
            for word in sent:
                if nltk.stem.PorterStemmer().stem(word) == all_words[i][0]:
                    if word not in original_words[i]:
                        original_words[i].append(word)
    print(original_words)
