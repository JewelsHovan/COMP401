import re
import pandas as pd
import os
from Bio import SeqIO

# Define the folder containing the annotated files
# List all annotated files in the folder
print(os.getcwd())
folder = "Proteomes/AnnotatedLong_QPH"
annotated_files = [f for f in os.listdir(folder) if f.startswith(
    "drosophila_") and f.endswith(".out")]
annotated_paths = [os.path.join(folder, f) for f in os.listdir(
    folder) if f.startswith("drosophila_") and f.endswith(".out")]

# Masked Sequences Folder
Masked_Folder = "Proteomes/Masked_QPH_fasta"
masked_filepaths = [os.path.join(Masked_Folder, f) for f in os.listdir(
    Masked_Folder) if f.startswith("drosophila_") and f.endswith(".fasta")]

# folder for fasta files
fasta_folder = "Proteomes/Drosophila"
fasta_files = [f for f in os.listdir(
    fasta_folder) if f.startswith("drosophila_")]
fasta_paths = [os.path.join(fasta_folder, f) for f in os.listdir(
    fasta_folder) if f.startswith("drosophila_") and f.endswith(".fasta")]

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


def read_fasta_file(fasta_file):
    sequences = {}
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequence_name = record.id
        sequences[sequence_name] = str(record.seq)
    return sequences

# Define a function to process each annotated file and return a DataFrame


def process_annotated_file(filename, fasta_file, masked_file):
    data = []
    sequences = read_fasta_file(fasta_file)
    masked_sequences = read_fasta_file(masked_file)
    with open(filename, "r") as file:
        lines = file.readlines()

        # get species ID from the file name
        species_id = os.path.splitext(os.path.basename(filename))[
            0].replace("drosophila_", "")
        species_name = species_id_to_name.get(
            species_id, f"Unkown_{species_id}")
        print(species_name)

        for line in lines:
            # Process only the lines starting with "tr|" or "sp|"
            if line.startswith("tr|") or line.startswith("sp|"):
                columns = line.split("\t")
                if len(columns) >= 16:
                    sequence_name = columns[0]
                    sequence_length = columns[1].split("=")[-1]
                    bias_type = columns[2]
                    start_position = columns[4]
                    end_position = columns[5]
                    residue_length = columns[6]
                    p_value = columns[7]
                    signature = re.search(r"\{(.+?)\}", columns[8]).group(1)
                    annotated_region = columns[15]
                    protein_sequence = sequences.get(sequence_name)
                    masked_sequence = masked_sequences.get(sequence_name)

                    data.append([species_name, sequence_name, sequence_length, bias_type, start_position, end_position,
                                residue_length, signature, p_value, annotated_region, protein_sequence, masked_sequence])

    column_names = ['Species', 'Sequence Name', 'Sequence Length', 'Bias Type', 'Start Position', 'End Position',
                    'Residue Length', 'Signature', 'P Value', 'Annotated Region', 'Protein Sequence', 'Masked Sequence']
    df = pd.DataFrame(data, columns=column_names)
    return df


def save_filtered_data_to_excel(filter_signature, output_file):
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for annotated_file in annotated_files:
            filepath = os.path.join(folder, annotated_file)
            species_id = annotated_file.replace(
                "drosophila_", "").replace(".out", "")
            fasta_file = os.path.join(
                fasta_folder, annotated_file.replace(".out", ".fasta"))
            masked_file = os.path.join(
                Masked_Folder, annotated_file.replace(".out", ".fasta"))

            # Process the annotated file and get a DataFrame
            df = process_annotated_file(filepath, fasta_file, masked_file)
            if not df.empty and not df[(df['Bias Type'] == 'SINGLE') | (df['Bias Type'] == 'MULTIPLE')].empty:
                filtered_df = df[((df['Bias Type'] == 'SINGLE') | (
                    df['Bias Type'] == 'MULTIPLE')) & (df['Signature'] == filter_signature)]

                # Save the filtered data as a new sheet in the Excel workbook
                # Only save the sheet if the DataFrame is not empty
                if not filtered_df.empty:
                    filtered_df.to_excel(
                        writer, sheet_name=f"species_{species_id}", index=False)


def get_signature_percentage(filepaths, signature):
    percentages = []
    for filepath in filepaths:
        fasta_file = os.path.join(fasta_folder, os.path.basename(
            filepath.replace(".out", ".fasta")))
        df = process_annotated_file(filepath, fasta_file)
        total_proteins = df['Sequence Name'].nunique()
        signature_proteins = df[df['Signature'] ==
                                signature]['Sequence Name'].nunique()
        percentage = (signature_proteins / total_proteins) * 100
        percentages.append(percentage)
    return percentages


def get_signature_positions(filepaths, signature):
    signature_positions = []
    for filepath in filepaths:
        fasta_file = os.path.join(fasta_folder, os.path.basename(
            filepath.replace(".out", ".fasta")))
        df = process_annotated_file(filepath, fasta_file)
        signature_df = df[df['Signature'] == signature]
        positions = list(
            zip(signature_df['Start Position'], signature_df['End Position']))
        signature_positions.append(positions)
    return signature_positions


def create_fasta_file_for_signature(filepaths, signature, output_fasta_file):
    with open(output_fasta_file, "w") as fasta_file:
        for filepath in filepaths:
            fasta_f = os.path.join(fasta_folder, os.path.basename(
                filepath.replace(".out", ".fasta")))
            masked_file = os.path.join(Masked_Folder, os.path.basename(
                filepath.replace(".out", ".fasta")))
            df = process_annotated_file(filepath, fasta_f, masked_file)
            signature_df = df[df['Signature'] == signature]
            for _, row in signature_df.iterrows():
                fasta_file.write(
                    f">{row['Sequence Name']}_{row['Start Position']}_{row['End Position']}\n")
                fasta_file.write(f"{row['Annotated Region']}\n")


def main(toWrite: bool, toCompare: bool):
    # write excel files
    if toWrite:
        save_filtered_data_to_excel("Q", "output_Q.xlsx")
        save_filtered_data_to_excel("QH", "output_QH.xlsx")
        save_filtered_data_to_excel("QPH", "output_QPH.xlsx")

     # Call the functions here
    if toCompare:
        qph_percentages = get_signature_percentage(annotated_paths, 'QPH')
        for species_id, percentage in enumerate(qph_percentages, start=1):
            print(f"Species {species_id}: {percentage:.2f}%")

        qph_positions = get_signature_positions(annotated_paths, 'QPH')
        for species_id, positions in enumerate(qph_positions, start=1):
            print(f"Species {species_id}: {positions}")

    print("##############################################")
    print("Creating FASTA files for all Q, QH, and QPH domain sequences")
    create_fasta_file_for_signature(
        annotated_paths, 'QPH', 'qph_sequences.fasta')
    create_fasta_file_for_signature(
        annotated_paths, 'QH', 'qh_sequences.fasta')
    create_fasta_file_for_signature(annotated_paths, 'Q', "q_sequences.fasta")


if __name__ == '__main__':
    main(True, False)
