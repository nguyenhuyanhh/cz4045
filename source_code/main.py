"""Wrapper for all operations."""

from __future__ import division, print_function

import os
import re
import sys

import pandas as pd

from dataset import get_truths, report
from tokenizer import evaluate, tokenize_get_code, tokenize_v2

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
RAW_DIR = os.path.join(CUR_DIR, 'raw_data')
if not os.path.exists(RAW_DIR):
    os.makedirs(RAW_DIR)
DATA_DIR = os.path.join(CUR_DIR, 'tagged_data/')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def get_english_words():
    """Get a set of English words, utilising different means."""
    try:
        if sys.platform in ['linux', 'linux2', 'darwin']:
            # unix has this wonderful builtin dictionary
            # at /usr/share/dict/words
            with open('/usr/share/dict/words', 'r') as dict_:
                words = [x.strip() for x in dict_.readlines()]
                print('Using Unix dictionary...')
                return set(words)
        else:
            raise OSError
    except BaseException:
        from nltk.corpus import brown
        print('Using Brown corpus...')
        return set(brown.words())


def tokenize_dataset():
    """Tokenize the whole dataset and print out most common tokens."""
    from collections import Counter

    # tokenize whole dataset
    data = pd.read_csv(os.path.join(RAW_DIR, 'QueryResults.csv'))
    ovr_tokens = []
    for id_ in data['Id']:
        # get tokens, remove code tags if exists
        text = data[data['Id'] == id_]['Body'].values[0]
        tokens = [re.sub(r'</?code>', '', x) for x in tokenize_v2(text)]
        ovr_tokens += tokens

    # print out top non-english, non-digit/punctuation tokens
    counter = Counter(ovr_tokens)
    keys = counter.keys()
    english_words = get_english_words()
    for key in keys:
        # drop english, punctuation and digits-only keys
        if re.match(r"^[\W\d]+$", key) or key.lower() in english_words:
            counter.pop(key)
    print(counter.most_common(50))


def tokenize_eval():
    """Tokenize and evaluate the implemented tokenizer on the annotated dataset."""
    data = pd.read_csv(os.path.join(RAW_DIR, 'TokenTagRaw.csv'))

    ovr_len_truth = 0
    ovr_len_tokens = 0
    ovr_accr = 0
    for id_ in data['Id']:
        # get truths and tokens, remove code tags if exists
        truth = get_truths(id_)
        text = data[data['Id'] == id_]['Body'].values[0]
        tokens = [re.sub(r'</?code>', '', x) for x in tokenize_v2(text)]
        ovr_len_truth += len(truth)
        ovr_len_tokens += len(tokens)
        # evaluate single post
        accr, pre, rec, f1_ = evaluate(tokens, truth)
        ovr_accr += accr
        print('Id: {}, precision: {:.3f}, recall: {:.3f}, f1: {:.3f}'.format(
            id_, pre, rec, f1_))
    # overall evaluation
    pre = ovr_accr / ovr_len_tokens
    rec = ovr_accr / ovr_len_truth
    f1_ = 2 * pre * rec / (pre + rec)
    print('Overall: precision: {:.3f}, recall: {:.3f}, f1: {:.3f}'.format(
        pre, rec, f1_))


def get_libraries(num=10):
    """Get the most common libraries used in the dataset."""
    from collections import Counter

    # regexes
    import_reg = re.compile(r'((?:from [^\s]+ import)|(?:import [^\s]+))')
    lib_reg = re.compile(
        r'((?<=from )(?:[^\s]+)(?= import)|(?<=import )(?:[^\s]+))')

    # read data
    data = pd.read_csv(os.path.join(RAW_DIR, 'QueryResults.csv'))

    # extract top libraries
    library_list = []
    for content in data['Body']:
        code_blocks = [x for x in tokenize_get_code(content) if 'import ' in x]
        if code_blocks:
            for block in code_blocks:
                temp = import_reg.findall(block)
                for tmp in temp:
                    library_list += lib_reg.findall(tmp)
    return Counter(library_list).most_common(num)


def usage():
    """Print command-line usage."""
    print('usage: main.py [report|stempos|test|tokenize|eval|common]')
    print('\t report \t report dataset stats')
    print('\t stempos \t stemming and POS tagging on dataset')
    print('\t test \t\t test the tokenizer')
    print('\t tokenize \t tokenize the dataset, output irregular tokens')
    print('\t eval \t\t evaluate the tokenizer on annotated dataset')
    print('\t common \t get the most common libraries from the dataset')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Invalid arguments! Exiting...')
        usage()
    elif sys.argv[1] == 'report':
        # report dataset stats
        report()
    elif sys.argv[1] == 'stempos':
        # stemming and POS tagging on dataset
        from stem_and_pos import stem_and_pos
        stem_and_pos()
    elif sys.argv[1] == 'test':
        # testing
        import unittest
        import test
        unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromModule(test))
    elif sys.argv[1] == 'tokenize':
        # tokenize the dataset
        tokenize_dataset()
    elif sys.argv[1] == 'eval':
        # evaluate the tokenizer
        tokenize_eval()
    elif sys.argv[1] == 'common':
        # get the most common libraries from the dataset
        get_libraries()
    else:
        print('Invalid arguments! Exiting...')
        usage()
