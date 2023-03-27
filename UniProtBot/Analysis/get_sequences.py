# using filtered out annotated out files from fLPS2.0
# Retrieve the sequences and output to new file
from Bio import SeqIO
import os
import argparse

# command line arguments
parser = argparse.ArgumentParser(description='Filter lines from a file based on a threshold p-value')
parser.add_argument('fasta_file', type=str, help="Fasta file of organism to input")
parser.add_argument('annotate_file', type=str, help='Annotated file from fLPS2.0')
args = parser.parse_args()

# make sure current directory is FilteredSequences/
os.chdir('/home/julienh/Desktop/COMP401/Proteomes/Alignment/FilteredSequences')
# input files
fasta_file = args.fasta_file
fasta_file = fasta_file.strip('\n')
annotation_file = args.annotate_file
annotation_file = annotation_file.strip('\n')
# output file
output_file = os.path.basename(fasta_file).replace('drosophila', 'poi')

def read_annotated_sequences(fasta_file: str, annotation_file: str, output_file: str) -> None:
    # Read the protein IDs of interest from the annotation file
    protein_ids = set() # add to set
    with open(annotation_file, "r") as f:
        for line in f:
            fields = line.strip().split("\t")
            protein_id = fields[0]
            protein_ids.add(protein_id)

    # Iterate over the FASTA sequences and extract the sequences for the proteins of interest
    with open(output_file, "w") as out_f:
        for record in SeqIO.parse(fasta_file, "fasta"):
            if record.id in protein_ids:
                SeqIO.write(record, out_f, "fasta")

read_annotated_sequences(fasta_file, annotation_file, output_file)
