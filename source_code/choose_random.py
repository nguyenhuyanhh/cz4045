import os
import re

import numpy as np
import pandas as pd

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(CUR_DIR, 'tagged_data/')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

OUT_SIZE = 100
SEED = 42

np.random.seed(SEED)
df = pd.read_csv(os.path.join(CUR_DIR, "QueryResults.csv"))

out = df.reindex(np.random.permutation(df.index))
out = out[:OUT_SIZE]
out.sort_index(by=['Id'],inplace=True)

out.to_csv('TokenTagRaw.csv',index=False)

for id_ in out['Id']:
    with open(os.path.join(DATA_DIR, '{}.txt'.format(id_)), 'w') as file_:
        body_txt = out[out['Id'] == id_]['Body'].values[0]
        regex_data = re.sub(r'(</?(?!code)(?:[a-zA-Z]+[1-6]?)\s*(?:\w+?="[\W\w]+?")?\s*>)', ' ', body_txt)
        file_.write(regex_data)

# out = out['Body']
# regex_data = [re.sub(r"<(?!\/?code).*?>", r"", i) for i in out]

# with open('TokenTagText.txt','w+') as textFile:
#     for line in regex_data:
#         textFile.write(line)
