import re
import statistics

# Wklej tutaj swój tekst (możesz też wczytać z pliku)
tekst = """

"""

# Wyciągamy wszystkie wartości czasu z tekstu
czasy = [float(match) for match in re.findall(r'Czas:\s*([\d.]+)', tekst)]

# Obliczamy średnią i odchylenie standardowe
srednia = statistics.mean(czasy)
odchylenie = statistics.stdev(czasy)

# Wynik
print(f"Liczba pomiarów: {len(czasy)}")
print(f"Średni czas: {srednia:.4f} s")
print(f"Odchylenie standardowe: {odchylenie:.4f} s")
