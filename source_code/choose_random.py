import pandas as pd
import numpy as np
import re

OUT_SIZE = 100
SEED = 42

np.random.seed(SEED)
df = pd.read_csv("QueryResults.csv")

out = df.reindex(np.random.permutation(df.index))
out = out[:OUT_SIZE]
out.sort_index(by=['Id'],inplace=True)

out.to_csv('TokenTagRaw.csv',index=False)

out = out['Body']
regex_data = [re.sub(r"<(?!\/?code).*?>", r"", i) for i in out]

with open('TokenTagText.txt','w+') as textFile:
    for line in regex_data:
        textFile.write(line)
