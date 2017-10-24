import pandas as pd
import numpy as np

OUT_SIZE = 100
SEED = 42

np.random.seed(SEED)
df = pd.read_csv("QueryResults.csv")

out = df.reindex(np.random.permutation(df.index))
out = out[:OUT_SIZE]
out.sort_index(by=['Id'],inplace=True)

out.to_csv('TokenTagRaw.csv',index=False)

with open('TokenTagText.txt','w+') as textFile:
    for line in out['Body']:
        textFile.write(line)
