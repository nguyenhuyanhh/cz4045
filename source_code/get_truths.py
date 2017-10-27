import os
import re

def get_truths(id):
    """ returns list of tokens from the tagged file with the given id """
    CUR_DIR = os.path.dirname(os.path.realpath(__file__))
    DATA_DIR = os.path.join(CUR_DIR, 'tagged_data/')

    with open(os.path.join(DATA_DIR, '{}.txt'.format(id)), 'r') as file_:
        if (str(id) == '7771342'):
            token_list = file_.read().split(';')
        else:
            token_list = file_.read().split('~')

    token_list = [i for i in token_list if i and re.match(r'\s*',i).group(0) != i]
    return token_list

if __name__ == '__main__':
    print(get_truths(60243))
