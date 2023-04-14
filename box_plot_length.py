import pandas as pd
import matplotlib.pyplot as plt

species_id_to_name = {
    "46245": "Drosophila_pseudoobscura",
    "7227": "Drosophila_melanogaster",
    "1041015": "Drosophila_rhopaloa",
    "7226": "Drosophila_mauritiana",
    "7245": "Drosophila_yakuba",
    "30033": "Drosophila_kikkawai",
    "7291": "Drosophila_albomicans",
    "7217": "Drosophila_ananassae",
    "7224": "Drosophila_hydei",
    "7244": "Drosophila_virilis",
    "7230": "Drosophila_mojavensis",
    "7225": "Drosophila_lebanonensis",
    "7266": "Drosophila_guanche",
    "7220": "Drosophila_erecta",
    "7234": "Drosophila_persimilis",
    "7232": "Drosophila_navojoa",
    "7240": "Drosophila_simulans",
    "7260": "Drosophila_willistoni",
    "7222": "Drosophila_grimshawi",
    "30019": "Drosophila_busckii",
    "7238": "Drosophila_sechellia",
}

def extract_sequence_lengths(file_names, species_id_to_name):
    sequence_lengths = {}

    for file_name in file_names:
        with pd.ExcelFile(file_name) as xls:
            sheets = xls.sheet_names

        for sheet in sheets:
            species_id = str(sheet.split('_')[1])
            species_name = species_id_to_name[species_id]

            if species_name not in sequence_lengths:
                sequence_lengths[species_name] = []

            df = pd.read_excel(file_name, sheet_name=sheet)
            sequence_lengths[species_name].extend(df['Sequence Length'].tolist())

    return sequence_lengths



def plot_sequence_length_boxplots(sequence_lengths):
    fig, ax = plt.subplots()
    data = [lengths for lengths in sequence_lengths.values()]
    labels = [species for species in sequence_lengths.keys()]
    
    ax.boxplot(data, labels=labels)
    ax.set_xlabel('Species')
    ax.set_ylabel('Sequence Length')
    ax.set_title('Distribution of Sequence Lengths')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

file_names = ['output_Q.xlsx', 'output_QH.xlsx', 'output_QPH.xlsx']

sequence_lengths = extract_sequence_lengths(file_names, species_id_to_name)
plot_sequence_length_boxplots(sequence_lengths)
