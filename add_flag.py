import pandas as pd
df = pd.read_csv("pomiar_warcaby.csv")
df["is_optimize"] = 0
df.loc[0:220, "is_optimize"] = 1
df.to_csv("pomiar_warcaby_out.csv", index=False)
