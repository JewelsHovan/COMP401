import pandas as pd
import os

excel_files = ['output_Q.xlsx', 'output_QH.xlsx', 'output_QPH.xlsx']
Q_p_value_threshold = 1e-30  # Example threshold
QH_p_value_threshold = 1e-31  # Example threshold
QPH_p_value_threshold = 1e-25  # Example threshold
Q_residue_threshold = 28  # Example threshold
QH_residue_threshold = 40  # Example threshold
QPH_residue_threshold = 200  # Example threshold

def write_filtered_proteins_to_fasta(output_file, signature, top_sequences, masked=False):
    with open(output_file, 'w') as fasta_file:
        for excel_file in excel_files:
            # Read each sheet in the Excel file
            with pd.ExcelFile(excel_file) as xls:
                for sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name)
                    # Filter proteins based on signature
                    filtered_df = df[df['Signature'] == signature]
                    # Sort proteins by p-value (ascending) and residue length (ascending)
                    sorted_df = filtered_df.sort_values(['P Value', 'Residue Length'], ascending=[False, False])
                    
                    # Get the top N sequences
                    top_sequences_df = sorted_df.head(top_sequences)

                    # Write filtered proteins to the fasta file, avoiding duplicates
                    for _, row in top_sequences_df.iterrows():
                        if masked:
                            seq = row['Masked Sequence']
                        else:
                            seq = row['Protein Sequence']

                        fasta_file.write(f">{row['Sequence Name']}_{row['Start Position']}_{row['End Position']}\n")
                        fasta_file.write(f"{seq}\n")
                            
    print("Finished writing to", output_file)


top_sequences = 15
write_filtered_proteins_to_fasta('Alignments/Alignment_Fastas/Sorted_5/q_prots.fasta', 'Q', top_sequences)
write_filtered_proteins_to_fasta('Alignments/Alignment_Fastas/Sorted_5/qh_prots.fasta', 'QH', top_sequences)
write_filtered_proteins_to_fasta('Alignments/Alignment_Fastas/Sorted_5/qph_prots.fasta', 'QPH', top_sequences)
write_filtered_proteins_to_fasta('Alignments/Alignment_Fastas/Sorted_5/q_masked.fasta', 'Q', top_sequences, masked=True)
write_filtered_proteins_to_fasta('Alignments/Alignment_Fastas/Sorted_5/qh_masked.fasta', 'QH', top_sequences, masked=True)
write_filtered_proteins_to_fasta('Alignments/Alignment_Fastas/Sorted_5/qph_masked.fasta', 'QPH', top_sequences, masked=True)