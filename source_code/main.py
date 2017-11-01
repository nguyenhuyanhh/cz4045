"""Wrapper for all operations."""

from __future__ import division, print_function

import os
import re
import sys

import pandas as pd

from dataset import get_truths, report
from stem_and_pos import stem_and_pos
from tokenizer import evaluate, tokenize_get_code, tokenize_v2

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
RAW_DIR = os.path.join(CUR_DIR, 'raw_data')
if not os.path.exists(RAW_DIR):
    os.makedirs(RAW_DIR)
DATA_DIR = os.path.join(CUR_DIR, 'tagged_data/')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def tokenize_and_eval():
    """Tokenize and evaluate the implementend tokenizer on the annotated dataset."""
    data = pd.read_csv(os.path.join(RAW_DIR, 'TokenTagRaw.csv'))

    ovr_len_truth = 0
    ovr_len_tokens = 0
    ovr_accr = 0
    for id_ in data['Id']:
        # get truths and tokens
        truth = get_truths(id_)
        text = data[data['Id'] == id_]['Body'].values[0]
        # remove code tags from tokens
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


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Invalid arguments! Exiting...')
    elif sys.argv[1] == 'report':
        # report dataset stats
        report()
    elif sys.argv[1] == 'stempos':
        # stemming and POS tagging on dataset
        stem_and_pos()
    elif sys.argv[1] == 'tokenize':
        # tokenize and evaluate
        tokenize_and_eval()
