import pandas as pd
import os
path = os.path.join('almost_complete.csv')
df = pd.read_csv(path)
outpath = os.path.join('html_data.html')
df.to_html(outpath)