import csv
import os
def save_measurement(depth, time_value, nodes, prunes):
    file_path = "pomiar_warcaby.csv"
    file_exists = os.path.isfile(file_path)
    with open(file_path, "a", newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["depth", "time", "nodes", "prunes"])
        writer.writerow([depth, time_value, nodes, prunes])