from collections import defaultdict

from mtgsdk import Set as MtgSet
import pandas as pd

df_dict_data = defaultdict(list)
for mtg_set in MtgSet.all():
    for k, v in mtg_set.__dict__.items():
        df_dict_data[k].append(v)

print(df_dict_data)
pd.DataFrame(df_dict_data).to_csv("sets.csv", index=False)
