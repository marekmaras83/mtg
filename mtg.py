import subprocess

import pyexcel_ods3
import json
from mtgsdk import Card
from playsound import playsound

MTG_SETS = {"dtk", "ddo", "m15", "m14", "m13", "m12", "ktk", "m11", "bfz", "m10", "ori", "c14", "exo (ex)",
            "uds (cg)", "jou", "rtr", "gpt", "usg (uz)", "chk", "ulg (gu)", "dka", "nph", "isd", "mrd", "dgm",
            "ddj", "rav", "10e", "ths", "tsp", "lrw", "bng", "avr", "mma", "roe", "con", "ala", "ddl",
            "mbs", "csp", "som", "mor", "hop", "wwk", "zen", "frf", "ahk"}

ODS_TO_MTG_PROPERTY_TRANSLATION_MAP = {
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

def ods_header_check(ods_columns):
    for column_name in ODS_TO_MTG_PROPERTY_TRANSLATION_MAP.keys():
        if column_name not in ods_columns:
            ods_columns.append(column_name)

    for column_name in ods_columns:
        if column_name not in ODS_TO_MTG_PROPERTY_TRANSLATION_MAP.keys():
            print(f"additional property: {column_name} found")


def get_ods_property_from_mtg_card(card, ods_property):
    mtg_value = getattr(card, ODS_TO_MTG_PROPERTY_TRANSLATION_MAP[ods_property])
    if not mtg_value:
        return ''
    elif type(mtg_value) == list:
        return str(mtg_value)
    else:
        return mtg_value


def update_all_properties(ods_columns, card_record):
    card_remote_data = Card.where(
        set=card_record[ods_columns.index("short set")].lower()).where(
        number=card_record[ods_columns.index("id in set")]).all()[0]

    for ods_property, sdk_property in ODS_TO_MTG_PROPERTY_TRANSLATION_MAP.items():
        property_ods_index = ods_columns.index(ods_property)
        if card_record[property_ods_index] == '':
            card_record[property_ods_index] = get_ods_property_from_mtg_card(card_remote_data, ods_property)

# cards = Card.where(set='frf').where(number=2).all()

NEW_ODS_PATH = '/home/sztylet/Desktop/mtg_collection.ods'
ODS_PATH = '/home/sztylet/Desktop/mtg_collection_update.ods'

ods_data = pyexcel_ods3.get_data(ODS_PATH)

ods_columns = ods_data["Sheet1"][0]
ods_header_check(ods_columns)

for card_record in ods_data["Sheet1"]:
    if card_record:
        if len(card_record) < len(ods_columns):
            card_record.extend([''] * (len(ods_columns) - len(card_record)) )

        for mandatory_property in MANDATORY_PROPERTIES_FOR_ALL:
            if not card_record[ods_columns.index(mandatory_property)]:
                update_all_properties(ods_columns, card_record)
                break
        print(card_record)

pyexcel_ods3.save_data(NEW_ODS_PATH, ods_data)
subprocess.run("cvlc /home/sztylet/Downloads/old-car-engine_daniel_simion.mp3", shell=True)
