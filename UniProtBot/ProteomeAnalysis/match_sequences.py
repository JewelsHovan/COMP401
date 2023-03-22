from Bio import SeqIO
import glob

def match_sequence(sequence, fasta_files):
    matched_ids = []
    for file in fasta_files:
        for record in SeqIO.parse(file, 'fasta'):
            if sequence in record.seq:
                matched_ids.append(record.id)
    return matched_ids

filenames = glob.glob('*.fasta') # fasta files
all_matched_tags_dict = {}
with open("most_common_proteins.txt", "r") as rfile:
    lines = rfile.readlines()
    for line in lines:
        sequence = line.split(" ")[0] # separate by whitespace
        matched_tags = match_sequence(sequence, filenames)
        all_matched_tags_dict[sequence] = matched_tags

with open("most_common_tags.txt", "w") as wfile:
    for key, value in all_matched_tags_dict.items():
        wfile.write("-".join(value) + " " + key + "\n")