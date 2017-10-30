"""Wrapper for all operations."""

from __future__ import print_function, division

import os
import re
import sys

import pandas as pd

from dataset import get_truths, report
from tokenizer import evaluate, tokenize_v2

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


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Invalid arguments! Exiting...')
    elif sys.argv[1] == 'report':
        # report dataset stats
        report()
    elif sys.argv[1] == 'tokenize':
        # tokenize and evaluate
        tokenize_and_eval()
