import argparse
import logging
import sys
from collections import defaultdict
from pathlib import Path

from mtgsdk import Card as MtgCard
import pandas as pd
import numpy as np

from tools.mtg_database.commons import SETS_PATH, CARDS_DATA_DIR


def get_set_filename(set_name: str) -> str:
    for char_to_be_replaced, replacement in ((' ', '_'), (':', '_'), ('\\', '_'), ('/', '_')):
        set_name = set_name.replace(char_to_be_replaced, replacement)
    return f"{set_name}.csv"


def set_logging_level(level: str):
    logging.basicConfig(stream=sys.stdout, level=level.upper())


def download_set_cards(set_info: pd.Series, cards_data_workspace: Path):
    set_data_path = cards_data_workspace / get_set_filename(set_info["name"])
    if set_data_path.exists():
        logging.debug(f"{set_data_path} already exists")
        return

    cards_dict = defaultdict(list)
    for mtg_card in MtgCard.where(set=set_info["code"]).all():
        for k, v in mtg_card.__dict__.items():
            cards_dict[k].append(v)
    if not cards_dict:
        logging.warning(f"\"{set_info['name']}\" does not contain any cards")
        return

    cards_df = pd.DataFrame(cards_dict)
    cards_df.sort_values(by="name", inplace=True)
    cards_df.to_csv(set_data_path, index=False)
    logging.info(f"'{set_data_path}' saved")


def main(workspace: Path):
    cards_data_workspace = workspace / CARDS_DATA_DIR
    if not workspace.exists():
        raise EnvironmentError(f"workspace {workspace} does not exist!")
    if not cards_data_workspace.exists():
        cards_data_workspace.mkdir(parents=True)

    sets_df = pd.read_csv(workspace / SETS_PATH)
    set_names_df = sets_df.loc[:, ["code", "name"]]
    num_of_sets = len(set_names_df)

    for i in range(num_of_sets):
        mtg_set = set_names_df.iloc[i]
        download_set_cards(mtg_set, cards_data_workspace)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='get cards data from magicthegathering.io')
    parser.add_argument('workspace', type=Path, help='workspace path (should be same for other scripts)')
    parser.add_argument('--logging', required=False, choices=["debug", "info", "warning", "error"], type=str, help='logs verbosity')
    args = parser.parse_args()
    if args.logging:
        set_logging_level(args.logging)

    main(args.workspace)
