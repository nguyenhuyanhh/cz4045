"""Report statistics on the dataset."""

from __future__ import division, print_function

import os

import matplotlib.pyplot as plt
import pandas as pd

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DATA = pd.read_csv(os.path.join(CUR_DIR, 'QueryResults.csv'))


def report():
    """Report statistics."""
    # no of qns and ans
    no_qns = DATA[DATA['PostTypeId'] == 1].shape[0]
    print('Number of questions: {}'.format(no_qns))
    no_ans = DATA[DATA['PostTypeId'] == 2].shape[0]
    print('Number of answers: {}'.format(no_ans))
    print('Average number of answers per questions: {}'.format(no_ans / no_qns))

    # no of ans per qns
    no_ans_per_qn = {}
    for id_ in DATA[DATA['PostTypeId'] == 1]['Id']:
        no_ans_per_qn[id_] = DATA[(DATA['PostTypeId']
                                   == 2) & (DATA['ParentId'] == id_)].shape[0]
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


if __name__ == '__main__':
    report()
