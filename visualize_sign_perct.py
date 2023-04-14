import pandas as pd
import matplotlib.pyplot as plt

# Create a dictionary with the data
data = {
    "Species Name": [
        "Drosophila_pseudoobscura", "Drosophila_melanogaster", "Drosophila_rhopaloa", "Drosophila_mauritiana",
        "Drosophila_yakuba", "Drosophila_kikkawai", "Drosophila_albomicans", "Drosophila_ananassae",
        "Drosophila_hydei", "Drosophila_virilis", "Drosophila_mojavensis", "Drosophila_lebanonensis",
        "Drosophila_guanche", "Drosophila_erecta", "Drosophila_persimilis", "Drosophila_navojoa",
        "Drosophila_simulans", "Drosophila_willistoni", "Drosophila_grimshawi", "Drosophila_busckii",
        "Drosophila_sechellia"
    ],
    "Q Signature Percentages": [
        22.60, 16.55, 15.27, 17.00, 16.15, 17.47, 22.60, 15.75, 21.55, 19.39, 19.28, 16.59, 17.29,
        15.42, 12.31, 20.48, 9.81, 15.33, 18.38, 17.18, 10.18
    ],
    "QH Signature Percentages": [
        2.10, 1.60, 1.32, 1.77, 1.63, 1.60, 1.96, 1.34, 1.29, 0.98, 1.15, 1.30, 1.57, 1.69, 1.16,
        1.26, 1.00, 1.30, 1.63, 0.97, 1.11
    ],
    "QPH Signature Percentages": [
        0.18, 0.14, 0.13, 0.15, 0.15, 0.23, 0.06, 0.10, 0.08, 0.04, 0.05, 0.11, 0.12, 0.16, 0.08,
        0.08, 0.10, 0.06, 0.09, 0.08, 0.09
    ]
}

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)

# Set the index to the species names
df.set_index("Species Name", inplace=True)

# Plot the bar chart
ax = df.plot.bar(rot=90, figsize=(15, 6))
ax.set_ylabel("Signature Percentage")
ax.set_title("Signature Percentages Across Drosophila Species")
plt.tight_layout()
plt.savefig("figures/Signature_Percentages_Bar_Chart.png", bbox_inches="tight")
plt.show()