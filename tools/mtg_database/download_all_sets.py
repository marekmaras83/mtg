import argparse
from collections import defaultdict
from pathlib import Path

from mtgsdk import Set as MtgSet
import pandas as pd

from tools.mtg_database.commons import SETS_PATH

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='get all sets from magicthegathering.io and save to csv')
    parser.add_argument('workspace', type=Path, help='workspace path (should be same for other scripts)')
    args = parser.parse_args()

    df_dict_data = defaultdict(list)
    for mtg_set in MtgSet.all():
        for k, v in mtg_set.__dict__.items():
            df_dict_data[k].append(v)

    output_path = args.workspace / SETS_PATH
    pd.DataFrame(df_dict_data).to_csv(output_path, index=False)
    print(f"file saved to '{output_path}'")
