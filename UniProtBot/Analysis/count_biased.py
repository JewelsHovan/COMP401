from fLPS_record import FLPS_record, FLPS_ledger
import argparse
import os

# command line arguments
parser = argparse.ArgumentParser(description='Read Annotated Fasta File from fLPS2.0 and Count Attributes up to a most common range')
parser.add_argument('input_file', type=str, help="The file path of the fasta file to input")
parser.add_argument('range', type=int, help="Maximum range of most common")
args = parser.parse_args()

input_file = args.input_file
RANGE = args.range

file_name = os.path.basename(input_file)

# from a fasta file counts the protein with the most disordered regions
flps_ledger = FLPS_ledger() # FLPS_ledger object
with open(input_file, "r") as rf:
    lines = rf.readlines()
    # strip non-records
    record_lines = [line for line in lines if not line.startswith("#")]
    record_lines = [line for line in record_lines if not line.startswith('<')]
    # create a FLPS_record object from each line
    for line in record_lines:
        line = line.strip().split("\t")
        seq_name = line[0]
        seq_length = line[1]
        bias_type = line[2]
        lps_num = line[3]
        start_index = line[4]
        end_index = line[5]
        residue_count = line[6]
        p_value = line[7]
        signature = line[8]
        flps_ledger.add_record(FLPS_record(seq_name, seq_length, bias_type, lps_num, start_index, end_index, residue_count, p_value, signature))

flps_ledger_size = flps_ledger.get_size()
print(f"Overview of all the compositionally biased regions from the file {file_name}: with {flps_ledger_size} regions")
print()
print(f"Counter of all Biases Types from the {flps_ledger_size} compositionally biased regions")
print(flps_ledger.count_bias())
print(f"Counter of all Signatures from the {flps_ledger_size} compositionally biased regions")
print(flps_ledger.count_signatures())
print(f"Top 5 Residue Counts from the {flps_ledger_size} compositionally biased regions")
print(flps_ledger.count_residues(10))
print()
print(f"Sequences with most biased regions up to range {RANGE}:")
print("################################################################################")
flps_ledger.get_information(RANGE)
print("################################################################################")