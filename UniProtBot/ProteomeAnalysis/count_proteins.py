from collections import Counter
import re
import glob
from Bio import SeqIO

# Define a function to extract protein identifier tags from a single file
def extract_protein_identifiers(filename):
    with open(filename, "r") as fasta_file:
        sequences = fasta_file.read()
    protein_identifiers = re.findall(r">.*?(?=\s)", sequences)
    return protein_identifiers

def extract_protein_sequences(filename):
    with open(filename, "r") as fasta_file:
        sequences = fasta_file.read()
    protein_sequences = sequences.split(">")[1:]
    protein_sequences = [seq[seq.find("\n")+1:].replace("\n", "") for seq in protein_sequences]
    return protein_sequences

def extract_protein_match_tag(filename):
    with open(filename, "r") as fasta_file:
        sequences = fasta_file.read()
    protein_sequences = sequences.split(">")[1:]
    protein_dict = {}
    for seq in protein_sequences:
        identifier, sequence = seq.split("\n", 1)
        identifier = ">" + identifier
        sequence = sequence.replace("\n", "")
        protein_dict[sequence] = identifier
    return protein_dict

def match_sequence(sequence, fasta_files):
    matched_ids = []
    for file in fasta_files:
        for record in SeqIO.parse(file, 'fasta'):
            if sequence in record.seq:
                matched_ids.append(record.id)
    return matched_ids

# Define a list of filenames to process
#filenames = glob.glob("/home/julienh/Desktop/COMP401/Proteomes/Drosophila/*.fasta")
filenames = glob.glob("*.fasta")

# Extract protein identifier tags from each file and combine them into a single list
all_protein_sequences = []
for filename in filenames:
    protein_sequences = extract_protein_sequences(filename)
    all_protein_sequences.extend(protein_sequences)

"""
all_proteins_dict = {}
for filename in filenames:
    protein_dict = extract_protein_match_tag(filename)
    all_proteins_dict.update(protein_dict)
"""

# Count the occurrences of each protein identifier tag
protein_counts = Counter(all_protein_sequences)
# Get the most frequent protein identifier tags and their counts
most_common_proteins = protein_counts.most_common(25)

# Print the results
with open("most_common_proteins.txt", "w") as file:
    for protein, count in most_common_proteins:
        file.write(f"{protein} occurs {count} times.\n")
