import pandas as pd

COLLECTION = "/home/sztylet/Desktop/mtg/mtg_collection.csv"
df = pd.read_csv(COLLECTION)

print(df.columns)
owned_sets = set(df["short set"].values)
new_sets = {"GRN", "OGW", "RNA", "C18", "WAR", "SOI", "MH1", "ELD", "BBD", "AER", "HOU", "AKH", "KLD", "DOM", "XLN",
            "BFZ", "CM2", "ORI", "C15",
            "DDN", "DDT", "EMN", "MM3", "CMA", "DDO", "A25", "THB", "RIX", "C19", "CN2", "DDQ", "C14", "C17", "UMA",
            "MM2", "IMA",
            "DGM", "NPH", "SOM", "JOU", "BNG", "RAV", "ROE", "THS", "TSP", "10E", "ZEN", "MRD",
            "DIS", "RTR", "WWK", "GTC", "DDI", "MMA", "DGM", "LRW", "9ED", "DST", "ISD", "WTH", "MBS", "CNS"}
all_sets_in_order = sorted(owned_sets.union(new_sets))
przegrodki = list()
sides = [0, 1]
while all_sets_in_order:
    przegrodka = ['', '']
    for side in sides:
        if not all_sets_in_order:
            break
        przegrodka[side] = all_sets_in_order[0]
        if side == 0:
            all_sets_in_order.pop(0)
    przegrodki.append(przegrodka)
print(przegrodki)
