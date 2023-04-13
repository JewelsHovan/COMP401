import pandas as pd
import os

excel_files = ['output_Q.xlsx', 'output_QH.xlsx', 'output_QPH.xlsx']
Q_p_value_threshold = 1e-30  # Example threshold
QH_p_value_threshold = 1e-30  # Example threshold
QPH_p_value_threshold = 1e-20  # Example threshold
Q_residue_threshold = 35  # Example threshold
QH_residue_threshold = 75  # Example threshold
QPH_residue_threshold = 500  # Example threshold

# Create a function to filter and write proteins to a fasta file
def write_filtered_proteins_to_fasta(output_file, signature, p_value_threshold, residue_threshold, masked=False):
    unique_sequences = set()  # Keep track of unique sequences
    with open(output_file, 'w') as fasta_file:
        for excel_file in excel_files:
            # Read each sheet in the Excel file
            with pd.ExcelFile(excel_file) as xls:
                for sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name)
                    # Filter proteins based on signature, p-value, and residue threshold
                    filtered_df = df[(df['Signature'] == signature) &
                                     (df['P Value'] <= p_value_threshold) &
                                     (df['Residue Length'] <= residue_threshold)]
                    # Write filtered proteins to the fasta file, avoiding duplicates
                    for _, row in filtered_df.iterrows():
                        if masked:
                            seq = row['Masked Sequence']
                        if not masked:
                            seq = row['Protein Sequence']
                        if seq not in unique_sequences:
                            fasta_file.write(f">{row['Sequence Name']}_{row['Start Position']}_{row['End Position']}\n")
                            fasta_file.write(f"{seq}\n")
                            unique_sequences.add(seq)  # Add the sequence to the set of unique sequences


# Generate fasta files for each signature
write_filtered_proteins_to_fasta('Alignments/Alignment_Fastas/q_prots.fasta', 'Q', Q_p_value_threshold, Q_residue_threshold)
write_filtered_proteins_to_fasta('Alignments/Alignment_Fastas/qh_prots.fasta', 'QH', QH_p_value_threshold, QH_residue_threshold)
write_filtered_proteins_to_fasta('Alignments/Alignment_Fastas/qph_prots.fasta', 'QPH', QPH_p_value_threshold, QPH_residue_threshold)
write_filtered_proteins_to_fasta('Alignments/Alignment_Fastas/q_masked.fasta', 'Q', Q_p_value_threshold, Q_residue_threshold, masked=True)
write_filtered_proteins_to_fasta('Alignments/Alignment_Fastas/qh_masked.fasta', 'QH', QH_p_value_threshold, QH_residue_threshold, masked=True)
write_filtered_proteins_to_fasta('Alignments/Alignment_Fastas/qph_masked.fasta', 'QPH', QPH_p_value_threshold, QPH_residue_threshold, masked=True)