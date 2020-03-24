import csv
import subprocess

from mtgsdk import Card

ROOT_FOLDER = "/home/sztylet/Desktop/mtg/"
DATABASE_PATH = ROOT_FOLDER + 'mtg_collection.csv'
NEW_DATABASE_PATH = ROOT_FOLDER + 'mtg_collection_update.csv'

MTG_SETS = {"dtk", "ddo", "m15", "m14", "m13", "m12", "ktk", "m11", "bfz", "m10", "ori", "c14", "exo (ex)",
            "uds (cg)", "jou", "rtr", "gpt", "usg (uz)", "chk", "ulg (gu)", "dka", "nph", "isd", "mrd", "dgm",
            "ddj", "rav", "10e", "ths", "tsp", "lrw", "bng", "avr", "mma", "roe", "con", "ala", "ddl",
            "mbs", "csp", "som", "mor", "hop", "wwk", "zen", "frf", "ahk"}

MY_TO_MTG_PROPERTY_TRANSLATION_MAP = {
    "name": "name",
    "colors": "colors",
    "mana cost": "mana_cost",
    "types": "types",
    "subtypes": "subtypes",
    "rarity": "rarity",
    "toughness": "toughness",
    "power": "power",
    "converted mana cost": "cmc",
    "short set": "set",
    "set": "set_name",
    "id in set": "number",
    "multiverse id": "multiverse_id",
    "english text": "text",
    "english flavor": "flavor",
}
MANDATORY_PROPERTIES_FOR_ALL = [
    "name", "types", "rarity", "set", "short set", "id in set", "multiverse id"
]
SPECIFIC_PROPERTIES_PER_TYPE = {
    "Creature": ["colors", "mana cost", "converted mana cost", "toughness", "power", "subtypes", "english text"],
    "Land": []
}


def csv_header_check(ods_columns):
    for column_name in MY_TO_MTG_PROPERTY_TRANSLATION_MAP.keys():
        assert column_name in ods_columns, f"input csv does not have column named: '{column_name}'"

    for column_name in ods_columns:
        if column_name not in MY_TO_MTG_PROPERTY_TRANSLATION_MAP.keys():
            print(f"additional property: {column_name} found")


def get_my_property_from_mtg_card(card, ods_property):
    mtg_value = getattr(card, MY_TO_MTG_PROPERTY_TRANSLATION_MAP[ods_property])
    if not mtg_value:
        return ''
    elif type(mtg_value) == list:
        return str(mtg_value)
    else:
        return mtg_value


def update_all_properties(card_record):
    card_remote_data = Card.where(
        set=card_record["short set"].lower()).where(
        number=card_record["id in set"]).all()[0]

    for my_property in MY_TO_MTG_PROPERTY_TRANSLATION_MAP.keys():
        if card_record[my_property] == '':
            card_record[my_property] = get_my_property_from_mtg_card(card_remote_data, my_property)

# cards = Card.where(set='frf').where(number=2).all()


with open(DATABASE_PATH, newline='') as csv_in, open(NEW_DATABASE_PATH, newline='', mode="w+") as csv_out:
    card_database_reader = csv.DictReader(csv_in)
    card_properties = card_database_reader.fieldnames
    csv_header_check(card_properties)

    database_update_writer = csv.DictWriter(csv_out, fieldnames=card_properties)
    database_update_writer.writeheader()

    for card_record in card_database_reader:
        for mandatory_property in MANDATORY_PROPERTIES_FOR_ALL:
            if not card_record[mandatory_property]:
                update_all_properties(card_record)
                break
        print(card_record)
        database_update_writer.writerow(card_record)

subprocess.run("cvlc /home/sztylet/Downloads/old-car-engine_daniel_simion.mp3", shell=True)
