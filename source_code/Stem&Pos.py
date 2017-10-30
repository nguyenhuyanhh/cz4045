import nltk as nltk
import pandas as pd
import re as re
import itertools
from collections import Counter
import os

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
RAW_DIR = os.path.join(CUR_DIR, 'raw_data')
# read data
data = pd.read_csv(os.path.join(RAW_DIR, 'QueryResults.csv'))

# sentence tokenize
sent_tokenized_data = [nltk.sent_tokenize(
    re.sub(r"<.*?>", r"", i)) for i in data.iloc[:, 3]]
print(sent_tokenized_data)

# word tokenize each row
tokenized_data = [nltk.word_tokenize(i[0]) for i in sent_tokenized_data]
#tokenized_data = [nltk.word_tokenize(re.sub(r"<.*?>|\W", r" ", i)) for i in data.iloc[:,0]]
print(tokenized_data)

# regex tokenizer
#regexstm = [nltk.regexp_tokenize(i,r"<code>[\W\w]*?<\/code>|(\d+\.\d+)|(\w+)(?=n't)|(n't)|('s)|([^\s\w]+)|(\w+)|(\w+\.\w+)",gaps=True) for i in data.iloc[:,3]]
# print(regexstm)

# POS tagging
pos_tagged = nltk.pos_tag_sents(tokenized_data)
print(pos_tagged)

# remove stopwords
no_stopwords = [[word for word in sent if word not in nltk.corpus.stopwords.words(
    'english')] for sent in tokenized_data]

# Stemming data
#stemmed_data  = [[nltk.stem.PorterStemmer().stem(word) for word in sent if word not in nltk.corpus.stopwords.words('english')] for sent in tokenized_data]
stemmed_data = [[nltk.stem.PorterStemmer().stem(word) for word in sent]
                for sent in no_stopwords]

# count words before stem
temporary = list(itertools.chain.from_iterable(no_stopwords))
counted = Counter(temporary)
print(counted.most_common(40))

# count words after stem
temporary = list(itertools.chain.from_iterable(stemmed_data))
counted = Counter(temporary)
print(counted.most_common(40))
