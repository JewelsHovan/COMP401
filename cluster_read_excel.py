import pandas as pd
import os
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
import matplotlib.pyplot as plt


excel_files = ['output_Q.xlsx', 'output_QH.xlsx', 'output_QPH.xlsx']
Q_p_value_threshold = 1e-28  # Example threshold
QH_p_value_threshold = 1e-28  # Example threshold
QPH_p_value_threshold = 1e-25  # Example threshold
Q_residue_threshold = 35  # Example threshold
QH_residue_threshold = 45  # Example threshold
QPH_residue_threshold = 200  # Example threshold

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
    print("Finished writing to", output_file)

def get_filtered_proteins(signature, p_value_threshold, residue_threshold):
    filtered_proteins = pd.DataFrame(columns=['Species', 'Sequence Name', 'Protein Sequence', 'Signature'])

    for excel_file in excel_files:
        # Read each sheet in the Excel file
        with pd.ExcelFile(excel_file) as xls:
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name)
                # Filter proteins based on signature, p-value, and residue threshold
                filtered_df = df[(df['Signature'] == signature) &
                                 (df['P Value'] <= p_value_threshold) &
                                 (df['Residue Length'] <= residue_threshold)]
                filtered_proteins = pd.concat([filtered_proteins, filtered_df[['Species', 'Sequence Name', 'Protein Sequence', 'Signature']]])

    return filtered_proteins.reset_index(drop=True)

def kmer_similarity(seq1, seq2, k=3):
    kmers1 = set([seq1[i:i+k] for i in range(len(seq1) - k + 1)])
    kmers2 = set([seq2[i:i+k] for i in range(len(seq2) - k + 1)])
    return len(kmers1.intersection(kmers2)) / len(kmers1.union(kmers2))

def find_representative_sequences(signature_clusters, filtered_data):
    representative_sequences = []

    for cluster_id in signature_clusters['Cluster'].unique():
        cluster_signatures = signature_clusters[signature_clusters['Cluster'] == cluster_id]['Signature']
        cluster_sequences = filtered_data[filtered_data['Signature'].isin(cluster_signatures)]

        max_similarity = 0
        representative_seq = None
        for i, row1 in cluster_sequences.iterrows():
            seq1 = row1['Protein Sequence']
            mean_similarity = 0
            for _, row2 in cluster_sequences.iterrows():
                seq2 = row2['Protein Sequence']
                mean_similarity += kmer_similarity(seq1, seq2)
            mean_similarity /= len(cluster_sequences)
            if mean_similarity > max_similarity:
                max_similarity = mean_similarity
                representative_seq = seq1
        representative_sequences.append(representative_seq)

    return representative_sequences

q_filtered_data = get_filtered_proteins('Q', Q_p_value_threshold, Q_residue_threshold)
qh_filtered_data = get_filtered_proteins('QH', QH_p_value_threshold, QH_residue_threshold)
qph_filtered_data = get_filtered_proteins('QPH', QPH_p_value_threshold, QPH_residue_threshold)
filtered_data = pd.concat([q_filtered_data, qh_filtered_data, qph_filtered_data])

unique_signatures = filtered_data['Signature'].unique()
similarity_matrix = pd.DataFrame(index=unique_signatures, columns=unique_signatures)

for signature1 in unique_signatures:
    seq1 = filtered_data.loc[filtered_data['Signature'] == signature1, 'Protein Sequence'].iloc[0]
    for signature2 in unique_signatures:
        seq2 = filtered_data.loc[filtered_data['Signature'] == signature2, 'Protein Sequence'].iloc[0]
        similarity_matrix.loc[signature1, signature2] = kmer_similarity(seq1, seq2)

# Convert similarity matrix to distance matrix
distance_matrix = 1 - similarity_matrix

# Perform hierarchical clustering
Z = linkage(squareform(distance_matrix), method='average')

# Plot the dendrogram
plt.figure(figsize=(10, 6))
dendrogram(Z, labels=unique_signatures, leaf_rotation=90)
plt.show()
# Set a clustering threshold
threshold = 0.6

# Extract clusters
clusters = fcluster(Z, threshold, criterion='distance')

# Assign each signature to its corresponding cluster
signature_clusters = pd.DataFrame({'Signature': unique_signatures, 'Cluster': clusters})
signature_clusters.to_csv('signature_clusters.csv', index=False)

# Find representative sequences for each cluster
representative_sequences = find_representative_sequences(signature_clusters, filtered_data)

# Write representative sequences to FASTA files
fasta_output_dir = 'Representative_FASTAs'
os.makedirs(fasta_output_dir, exist_ok=True)

for signature, seq in zip(signature_clusters['Signature'], representative_sequences):
    output_file = os.path.join(fasta_output_dir, f"{signature}_rep.fasta")
    with open(output_file, 'w') as fasta_file:
        fasta_file.write(f">{signature}_representative\n")
        fasta_file.write(f"{seq}\n")

print("Finished writing representative sequences to FASTA files.")

# Generate fasta files for each signature
write_filtered_proteins_to_fasta('Alignments/Alignment_Fastas/q_prots.fasta', 'Q', Q_p_value_threshold, Q_residue_threshold)
write_filtered_proteins_to_fasta('Alignments/Alignment_Fastas/qh_prots.fasta', 'QH', QH_p_value_threshold, QH_residue_threshold)
write_filtered_proteins_to_fasta('Alignments/Alignment_Fastas/qph_prots.fasta', 'QPH', QPH_p_value_threshold, QPH_residue_threshold)
write_filtered_proteins_to_fasta('Alignments/Alignment_Fastas/q_masked.fasta', 'Q', Q_p_value_threshold, Q_residue_threshold, masked=True)
write_filtered_proteins_to_fasta('Alignments/Alignment_Fastas/qh_masked.fasta', 'QH', QH_p_value_threshold, QH_residue_threshold, masked=True)
write_filtered_proteins_to_fasta('Alignments/Alignment_Fastas/qph_masked.fasta', 'QPH', QPH_p_value_threshold, QPH_residue_threshold, masked=True)