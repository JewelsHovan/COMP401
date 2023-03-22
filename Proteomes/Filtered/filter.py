import argparse
import os

# command line arguments
parser = argparse.ArgumentParser(description='Filter lines from a file based on a threshold p-value')
parser.add_argument('threshold', type=float, help="Threshold value to filter")
parser.add_argument('fileinput_name', type=str, help='Name of input file to filter')
args = parser.parse_args()

# filter variables
proteins_of_interest = "Q"
threshold = args.threshold
fileinput_name = args.fileinput_name

def filter_file(threshold: float, file_input: str) -> None:
    with open(file_input, 'r') as infile, open(f'{os.path.basename(file_input).split(".")[0]}_filtered.out', 'w') as outfile:
        for line in infile:
            fields = line.strip().split('\t')
            p_value = float(fields[7])
            protein_rich_in = fields[8]
            if p_value <= threshold and proteins_of_interest in protein_rich_in:
                outfile.write(line)

filter_file(threshold, fileinput_name)


