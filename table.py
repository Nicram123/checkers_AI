import pandas as pd
import numpy as np

# Wczytanie
df = pd.read_csv("pomiar_warcaby_out.csv")

# Grupowanie statystyk
grouped = df.groupby(["depth", "is_optimize"]).agg(
    mean_time=("time", "mean"),
    std_time=("time", "std"),
    mean_nodes=("nodes", "mean"),
    mean_prunes=("prunes", "mean")
).reset_index()

# -------------------------------
# TABELA 1: Bez alpha-beta
# -------------------------------
tabela1 = grouped[grouped.is_optimize == 0][[
    "depth", "mean_time", "std_time"
]].rename(columns={
    "depth": "Głębokość",
    "mean_time": "Średni czas bez αβ [s]",
    "std_time": "Odchylenie std bez αβ [s]"
})

# -------------------------------
# TABELA 2: Z alpha-beta + speedup
# -------------------------------

tabela2 = grouped[grouped.is_optimize == 1][[
    "depth", "mean_time", "std_time"
]].rename(columns={
    "depth": "Głębokość",
    "mean_time": "Średni czas z αβ [s]",
    "std_time": "Odchylenie std z αβ [s]"
})

# Dodajemy kolumnę speedup
speedup_list = []
for d in tabela2["Głębokość"]:
    t_no = grouped[(grouped.depth == d) & (grouped.is_optimize == 0)]["mean_time"]
    t_yes = grouped[(grouped.depth == d) & (grouped.is_optimize == 1)]["mean_time"]
    if len(t_no) > 0 and len(t_yes) > 0:
        speedup_list.append(t_no.values[0] / t_yes.values[0])
    else:
        speedup_list.append(np.nan)

tabela2["Przyspieszenie"] = speedup_list

# -------------------------------
# TABELA 3: Węzły i prunes
# -------------------------------
depths = sorted(df["depth"].unique())

rows = []
for d in depths:
    no_opt = grouped[(grouped.depth == d) & (grouped.is_optimize == 0)]
    opt = grouped[(grouped.depth == d) & (grouped.is_optimize == 1)]
    
    nodes_no = no_opt["mean_nodes"].values[0] if len(no_opt) else np.nan
    nodes_yes = opt["mean_nodes"].values[0] if len(opt) else np.nan
    prunes_yes = opt["mean_prunes"].values[0] if len(opt) else np.nan
    
    rows.append([d, nodes_no, nodes_yes, prunes_yes])

tabela3 = pd.DataFrame(rows, columns=[
    "Głębokość",
    "Odwiedzone węzły bez αβ",
    "Odwiedzone węzły z αβ",
    "Przycięcia z αβ"
])

# -------------------------------
# ZAPISYWANIE TABEL DO Excela
# -------------------------------
with pd.ExcelWriter("tabele_warcaby.xlsx") as writer:
    tabela1.to_excel(writer, sheet_name="Bez_alpha_beta", index=False)
    tabela2.to_excel(writer, sheet_name="Z_alpha_beta", index=False)
    tabela3.to_excel(writer, sheet_name="Wezly_i_prunes", index=False)

print("Gotowe! Plik tabele_warcaby.xlsx został wygenerowany.")
