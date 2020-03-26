import os

import pandas as pd

DATABASE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/cards.csv"
HEADER = ['name', 'layout', 'mana_cost', 'cmc', 'colors', 'color_identity', 'names', 'type', 'supertypes', 'subtypes', 'types', 'rarity', 'text', 'flavor', 'artist', 'number', 'power', 'toughness', 'loyalty', 'multiverse_id', 'variations', 'watermark', 'border', 'timeshifted', 'hand', 'life', 'release_date', 'starter', 'printings', 'original_text', 'original_type', 'source', 'image_url', 'set', 'set_name', 'id', 'legalities', 'rulings', 'foreign_names']

# pd.read_csv('data.csv')
df = pd.DataFrame(columns=HEADER)
df.to_csv(DATABASE_PATH)
