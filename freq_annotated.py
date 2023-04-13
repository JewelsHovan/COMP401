import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

file_names = ['output_Q.xlsx', 'output_QH.xlsx', 'output_QPH.xlsx']

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

annotated_regions_count = {}

# Iterate through the file names
for file_name in file_names:
    # Read the Excel file
    with pd.ExcelFile(file_name) as xls:
        sheets = xls.sheet_names

    annotated_regions_count[file_name] = {}

    for sheet in sheets:
        species_id = sheet.split('_')[1]
        species_name = species_id_to_name[species_id]

        # Read the data from the sheet
        df = pd.read_excel(file_name, sheet_name=sheet)

        # Count the number of rows (i.e., annotated regions) for the species
        annotated_regions_count[file_name][species_name] = len(df)


def plot_annotated_frequencies(file_names, annotated_regions_count):
    for file_name in file_names:
        # Create a new figure for each file
        fig, axes = plt.subplots(2, 1, figsize=(12, 12))
        
        # Bar plot
        sns.barplot(x=list(annotated_regions_count[file_name].keys()), y=list(annotated_regions_count[file_name].values()), ax=axes[0])
        axes[0].set_xticklabels(annotated_regions_count[file_name].keys(), rotation=90)
        axes[0].set_xlabel('Species')
        axes[0].set_ylabel('Number of Annotated Regions')
        axes[0].set_title(f'Annotated Region Frequency Across Drosophila species ({file_name.split(".")[0].replace("output_", "") + " Signature"})')

        # Pie chart
        axes[1].pie(annotated_regions_count[file_name].values(), labels=annotated_regions_count[file_name].keys(), autopct='%1.1f%%', startangle=90)
        axes[1].axis('equal')
        axes[1].set_title(f'Annotated Region Frequency Across Drosophila species ({file_name.split(".")[0].replace("output_", "") + " Signature"})')

        # Save the current figure with both bar and pie charts
        plt.tight_layout()
        plt.savefig(f'figures/charts_{file_name.split(".")[0].replace("output_","")}.png', bbox_inches='tight')

        # Show the figure
        plt.show()

def plot_residue_lengths(file_names, annotated_regions_count, species_id_to_name):
    for file_name in file_names:
        # Create a new dataframe to store residue lengths for each species
        residue_lengths_df = pd.DataFrame(columns=['Species', 'Residue Length'])

        # Fill the dataframe with data from the current Excel file
        for species_name in annotated_regions_count[file_name].keys():
            species_id = [k for k, v in species_id_to_name.items() if v == species_name][0]
            df = pd.read_excel(file_name, sheet_name=f'species_{species_id}')
            temp_df = df[['Sequence Name', 'Residue Length']].copy()  # Create a copy of the DataFrame slice
            temp_df.loc[:, 'Species'] = species_name
            residue_lengths_df = pd.concat([residue_lengths_df, temp_df]) 

        # Create a box plot for the residue lengths
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='Species', y='Residue Length', data=residue_lengths_df)
        plt.xticks(rotation=90)
        plt.title(f'Residue Length Distribution Across Species ({file_name})')
        
        # Save the box plot as an image file
        plt.tight_layout()
        plt.savefig(f'figures/residue_lengths_{file_name.split(".")[0].replace("output_", "")}.png', bbox_inches='tight')

        # Show the box plot
        plt.show()

# Uncomment either of the following lines to run the desired function:
if __name__ == "__main__":
    #plot_annotated_frequencies(file_names, annotated_regions_count)
    plot_residue_lengths(file_names, annotated_regions_count, species_id_to_name)
