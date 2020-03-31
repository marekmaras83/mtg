import pandas as pd
import numpy as np

COLLECTION = "/home/sztylet/Desktop/mtg/assistant_database/main.csv"
df = pd.read_csv(
    filepath_or_buffer=COLLECTION,
    dtype={
        "Count": np.int32,
        "Card Number": np.int32,
    }
).sort_values(by=["Edition", "Card Number"])
# print(df[df["Card Number"].isna()][["Name", "Edition"]])
# exit(0)

cards_sum = df["Count"].sum()
print(f"operation started with: {cards_sum} cards")

selection_filter = df["Count"] > 4
toomuchness_df = pd.DataFrame(df[selection_filter])
selected_indexes = toomuchness_df.index
interesting_columns = ["Count", "Name", "Edition", "Card Number"]

print(f"\noriginal main:\n{df.loc[selected_indexes, interesting_columns].head(5)}")

toomuchness_df["Count"] = toomuchness_df["Count"] - 4
print(f"\ntoomuchness:\n{toomuchness_df[interesting_columns].head(5)}")

df.loc[selected_indexes, "Count"] = 4
print(f"\nmain:\n{df.loc[selected_indexes, interesting_columns].head(5)}")

df_cards_sum = df["Count"].sum()
toomuchness_card_sum =toomuchness_df["Count"].sum()

print(f"cards before: {cards_sum}")
print(f"cards after split: {df_cards_sum} in main, {toomuchness_card_sum} in toomuchness")
assert cards_sum == df_cards_sum + toomuchness_card_sum


toomuchness_df.to_csv(path_or_buf="/home/sztylet/Desktop/mtg/toomuchness.csv", index=False)
df.to_csv(path_or_buf="/home/sztylet/Desktop/mtg/main_after_split.csv", index=False)
