import matplotlib.pyplot as plt

# przykładowe dane – podmień na swoje:
depths = [1, 2, 3, 4, 5, 6]
nodes = [50, 320, 2100, 15000]
prunes = [5, 80, 600, 4500]

plt.figure()
plt.plot(depths, nodes, marker='o')
plt.title("Liczba odwiedzonych węzłów vs głębokość")
plt.xlabel("Głębokość")
plt.ylabel("Węzły")
plt.grid(True)
plt.show()

plt.figure()
plt.plot(depths, prunes, marker='o')
plt.title("Liczba przycięć (alpha-beta) vs głębokość")
plt.xlabel("Głębokość")
plt.ylabel("Przycięcia")
plt.grid(True)
plt.show()
