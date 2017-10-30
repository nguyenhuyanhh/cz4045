import nltk as nltk
import pandas as pd
import re as re
import random as random
import itertools
from collections import Counter

##read data
data = pd.read_csv('QueryResults.csv')

##sentence tokenize
sent_tokenized_data = [nltk.sent_tokenize(re.sub(r"<.*?>", r"", i)) for i in data.iloc[:,3]]
print(sent_tokenized_data)

##word tokenize each row  without removing punctuations
tokenized_data = [nltk.word_tokenize(i[0]) for i in sent_tokenized_data]
print(tokenized_data)

##POS tagging
pos_tagged = nltk.pos_tag_sents(tokenized_data)
print(random.sample(pos_tagged,10))

##word tokenize each row
tokenized_data = [[re.sub(r"[^\w\s]", r"",j) for j in nltk.word_tokenize(i[0])] for i in sent_tokenized_data]
print(tokenized_data)

##remove stopwords
no_stopwords = [[word for word in sent if word not in nltk.corpus.stopwords.words('english')] for sent in tokenized_data]

##Stemming data
stemmed_data = [[nltk.stem.PorterStemmer().stem(word) for word in sent] for sent in no_stopwords]

##count words before stem
temporary = list(itertools.chain.from_iterable(no_stopwords))
counted = Counter(temporary)
print(counted.most_common(21))

##count words after stem
temporary = list(itertools.chain.from_iterable(stemmed_data))
counted = Counter(temporary)
all = counted.most_common(21)
print(all)

##find original words that stemmed to "all"
original_words = []
for i in range(21):
    original_words.append([])
    for sent in no_stopwords:
        for word in sent:
            if nltk.stem.PorterStemmer().stem(word) == all[i][0]:
                if word not in original_words[i]:
                    original_words[i].append(word)
print(original_words)