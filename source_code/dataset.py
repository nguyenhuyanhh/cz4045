"""Dataset operations."""

from __future__ import division, print_function

import os
import re

import pandas as pd

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
RAW_DIR = os.path.join(CUR_DIR, 'raw_data')
DATA_DIR = os.path.join(CUR_DIR, 'tagged_data/')


def report():
    """Report statistics on the dataset."""
    import matplotlib.pyplot as plt

    data = pd.read_csv(os.path.join(RAW_DIR, 'QueryResults.csv'))

    # no of qns and ans
    no_qns = data[data['PostTypeId'] == 1].shape[0]
    print('Number of questions: {}'.format(no_qns))
    no_ans = data[data['PostTypeId'] == 2].shape[0]
    print('Number of answers: {}'.format(no_ans))
    print('Average number of answers per questions: {}'.format(no_ans / no_qns))

    # no of ans per qns
    no_ans_per_qn = {}
    for id_ in data[data['PostTypeId'] == 1]['Id']:
        no_ans_per_qn[id_] = data[(data['PostTypeId']
                                   == 2) & (data['ParentId'] == id_)].shape[0]
    df_ = pd.DataFrame.from_dict(no_ans_per_qn, orient='index')
    count_1_ans = df_[df_[0] == 1].shape[0]
    count_2_ans = df_[df_[0] == 2].shape[0]
    count_3_ans = df_[df_[0] >= 3].shape[0]
    print('Questions with 1 answer: {}'.format(count_1_ans))
    print('Questions with 2 answers: {}'.format(count_2_ans))
    print('Questions with 3 or more answers: {}'.format(count_3_ans))

    # pie chart for aesthetics
    labels = '1 answer', '2 answers', '3 or more answers'
    sizes = [count_1_ans, count_2_ans, count_3_ans]
    plt.figure()
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.savefig(os.path.join(CUR_DIR, 'no_ans_per_qn.png'))
    plt.show()


def choose_random():
    """Choose 100 posts randomly from dataset and write to folder."""
    import numpy as np

    out_size = 100
    np.random.seed(42)
    data = pd.read_csv(os.path.join(RAW_DIR, "QueryResults.csv"))
    out = data.reindex(np.random.permutation(data.index))
    out = out[:out_size]
    out.sort_index(by=['Id'], inplace=True)
    out.to_csv(os.path.join(RAW_DIR, 'TokenTagRaw.csv'), index=False)

    for id_ in out['Id']:
        with open(os.path.join(DATA_DIR, '{}.txt'.format(id_)), 'w') as file_:
            body_txt = out[out['Id'] == id_]['Body'].values[0]
            regex_data = re.sub(
                r'(</?(?!code)(?:[a-zA-Z]+[1-6]?)\s*(?:\w+?="[\W\w]+?")?\s*>)', ' ', body_txt)
            file_.write(regex_data)


def get_truths(id_):
    """Returns list of tokens from the tagged file with the given id."""
    with open(os.path.join(DATA_DIR, '{}.txt'.format(id_)), 'r') as file_:
        if (str(id_) == '7771342'):
            token_list = file_.read().split(';')
        else:
            token_list = file_.read().split('~')
    token_list = [i for i in token_list if i and re.match(
        r'\s*', i).group(0) != i]
    return token_list
