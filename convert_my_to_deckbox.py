import argparse
import csv
from collections import OrderedDict

DECKBOX_CSV_COLUMNS = [
    "Count", "Tradelist Count", "Name", "Foil", "Textless", "Promo", "Signed", "Edition", "Condition", "Language",
    "Card Number"
]
TRANSLATION_MAP = OrderedDict({
    "name": "Name",
    "set": "Edition",
    "id in set": "Card Number",
    "quantity": "Count",
})
DEFAULT_DECKBOX_VALUES = {
    "Tradelist Count": 0,
    "Language": "English",
}


def my_csv_columns_check(column_names):
    for name in TRANSLATION_MAP.keys():
        assert name in column_names, f"ERROR: no '{name}' mandatory column in input csv file"


def convert_my_to_deckbox(my_csv_path, deckbox_csv_path):
    with open(my_csv_path, newline='') as my_csv, open(deckbox_csv_path, newline='', mode="w+") as deckbox_csv:
        my_reader = csv.DictReader(my_csv)
        card_properties = my_reader.fieldnames
        my_csv_columns_check(card_properties)

        deckbox_writer = csv.DictWriter(deckbox_csv, fieldnames=DECKBOX_CSV_COLUMNS)
        deckbox_writer.writeheader()

        for my_card_record in my_reader:
            deckbox_card_record = {
                deckbox_key: my_card_record[my_key] for my_key, deckbox_key in TRANSLATION_MAP.items()
            }
            deckbox_card_record.update({key: value for key, value in DEFAULT_DECKBOX_VALUES.items()})
            deckbox_writer.writerow(deckbox_card_record)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='convert my csv to deckbox inventory csv')
    parser.add_argument('my_csv', type=str, help='input csv in my format')
    parser.add_argument('output_path', type=str, help='output csv path (in deckbox inventory format)')

    args = parser.parse_args()
    convert_my_to_deckbox(args.my_csv, args.output_path)
