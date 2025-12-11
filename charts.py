import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("pomiar_warcaby_out.csv")
grouped = df.groupby(["depth", "is_optimize"]).agg(
    mean_time=("time", "mean"),
    std_time=("time", "std"),
    mean_nodes=("nodes", "mean"),
    mean_prunes=("prunes", "mean")
).reset_index()

# -------------------------
# WYKRES 1: Średni czas działania
# -------------------------
plt.figure(figsize=(8,5))

for label, subset in grouped.groupby("is_optimize"):
    name = "Z alpha-beta" if label == 1 else "Bez alpha-beta"
    plt.bar(
        subset["depth"] + (0.2 if label == 1 else -0.2),
        subset["mean_time"],
        width=0.4,
        label=name
    )

plt.xlabel("Głębokość")
plt.ylabel("Średni czas [s]")
plt.title("Średni czas działania minimaxa")
plt.legend()
plt.grid(axis="y", alpha=0.3)
plt.savefig("wykres_sredni_czas.png", dpi=200)
plt.show()

# -------------------------
# WYKRES 2: Odchylenie standardowe czasu
# -------------------------
plt.figure(figsize=(8,5))

for label, subset in grouped.groupby("is_optimize"):
    name = "Z alpha-beta" if label == 1 else "Bez alpha-beta"
    plt.bar(
        subset["depth"] + (0.2 if label == 1 else -0.2),
        subset["std_time"],
        width=0.4,
        label=name
    )

plt.xlabel("Głębokość")
plt.ylabel("Odchylenie standardowe czasu [s]")
plt.title("Odchylenie czasu działania minimaxa")
plt.legend()
plt.grid(axis="y", alpha=0.3)
plt.savefig("wykres_std_czas.png", dpi=200)
plt.show()


# -------------------------
# WYKRES 3: Przyspieszenie działania alpha-beta
# speedup = czas_bez / czas_z
# -------------------------
speedup = []

depths = sorted(df["depth"].unique())

for d in depths:
    t_no = grouped[(grouped.depth == d) & (grouped.is_optimize == 0)]["mean_time"].values
    t_yes = grouped[(grouped.depth == d) & (grouped.is_optimize == 1)]["mean_time"].values
    if len(t_no) > 0 and len(t_yes) > 0:
        speedup.append(t_no[0] / t_yes[0])
    else:
        speedup.append(np.nan)

plt.figure(figsize=(8,5))
plt.plot(depths, speedup, marker="o", linewidth=2)
plt.xlabel("Głębokość")
plt.ylabel("Przyspieszenie (czas bez / czas z)")
plt.title("Przyspieszenie działania algorytmu dzięki alpha-beta")
plt.grid(True, alpha=0.3)
plt.savefig("wykres_przyspieszenie.png", dpi=200)
plt.show()


# -------------------------
# WYKRES 4: Średnia liczba odwiedzonych węzłów
# -------------------------
plt.figure(figsize=(8,5))

for label, subset in grouped.groupby("is_optimize"):
    name = "Z alpha-beta" if label == 1 else "Bez alpha-beta"
    plt.plot(
        subset["depth"],
        subset["mean_nodes"],
        marker="o",
        linewidth=2,
        label=name
    )

plt.xlabel("Głębokość")
plt.ylabel("Średnia liczba odwiedzonych węzłów")
plt.title("Porównanie liczby odwiedzonych węzłów")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("wykres_wezly.png", dpi=200)
plt.show()


# -------------------------
# WYKRES 5: Średnia liczba przycięć (prunes)
# -------------------------
plt.figure(figsize=(8,5))

subset = grouped[grouped.is_optimize == 1]  # tylko z optymalizacją
plt.bar(subset["depth"], subset["mean_prunes"], width=0.5)

plt.xlabel("Głębokość")
plt.ylabel("Średnia liczba przycięć (prunes)")
plt.title("Liczba przycięć alpha-beta w zależności od głębokości")
plt.grid(axis="y", alpha=0.3)
plt.savefig("wykres_prunes.png", dpi=200)
plt.show()

print("Wszystkie wykresy zapisano!")
