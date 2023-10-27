# Pandas is optimized for row-columnar data. tables nad csv's into chart.

import pandas as pd
#data frame comes with a veritable slew of methods
df = pd.read_json('data/nobel_winners.json')
df.head() # peaks at first 5 records

df.columns
df.index

df = df.set_index("name") # quote marks '/" are important
df.loc['Albert Einstein'] # gets Albert's record
df.reset_index()
df.iloc[0] # gets record at 0
df.ix[0] # deprecated
column = df.sex # or df['sex']

df = df.groupby('category')
df.get_group('Physics')
# Apply boolean mask
df.category == 'Physics'
phy_group = df.get_group('Physics')
phy_group.head()
