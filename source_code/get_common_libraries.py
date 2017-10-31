import os
import sys
import csv
import re

#from operator import itemgetter
#sorted(d.items(), key=itemgetter(1)) sorting dictionary based on values

from collections import Counter
from tokenizer import tokenize_get_code

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
RAW_DIR = os.path.join(CUR_DIR, 'raw_data')

IMPORT_REG = re.compile(
    r'((?:from [^\s]+ import)|(?:import [^\s]+))')

LIB_REG = re.compile(
    r'((?<=from )(?:[^\s]+)(?= import)|(?<=import )(?:[^\s]+))')

def get_libraries(num):
    library_list = []
    with open('raw_data/QueryResults.csv', 'r', encoding="utf8", ) as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            cur = tokenize_get_code(row[3])
            for i in range(0,len(cur)):
                temp = cur[i]
                if temp.find("import ") >= 0:
                    temp = IMPORT_REG.findall(temp)
                    for x in temp:
                        library_list += LIB_REG.findall(x)
    library_list = Counter(library_list)
    return library_list.most_common(num)

print(get_libraries(10))

