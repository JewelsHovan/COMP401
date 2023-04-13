import pandas as pd
import os

excel_files = ['output_Q.xlsx', 'output_QH.xlsx', 'output_QPH.xlsx']
Q_p_value_threshold = 1e-30  # Example threshold
QH_p_value_threshold = 1e-20  # Example threshold
QPH_p_value_threshold = 1e-15  # Example threshold
Q_residue_threshold = 50  # Example threshold
QH_residue_threshold = 250  # Example threshold
QPH_residue_threshold = 500  # Example threshold

# Create a function to filter and write proteins to a fasta file
def write_filtered_proteins_to_fasta(output_file, signature, p_value_threshold, residue_threshold):
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
                    # Write filtered proteins to the fasta file
                    for _, row in filtered_df.iterrows():
                        fasta_file.write(f">{row['Sequence Name']}_{row['Start Position']}_{row['End Position']}\n")
                        fasta_file.write(f"{row['Protein Sequence']}\n")

# Generate fasta files for each signature
write_filtered_proteins_to_fasta('q_prots.fasta', 'Q', Q_p_value_threshold, Q_residue_threshold)
write_filtered_proteins_to_fasta('qh_prots.fasta', 'QH', QH_p_value_threshold, QH_residue_threshold)
write_filtered_proteins_to_fasta('qph_prots.fasta', 'QPH', QPH_p_value_threshold, QPH_residue_threshold)
