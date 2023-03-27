import matplotlib.pyplot as plt
import ast
import argparse
import os

parser = argparse.ArgumentParser(description='Read Count file and graph data')
parser.add_argument('input_file', type=str, help="The input file path of the count file")
parser.add_argument('output_folder', type=str, help="The output forder path of the graph figures saved")
args = parser.parse_args()

input_file = args.input_file
output_folder = args.output_folder

input_file_base = os.path.basename(input_file)
output_path = os.path.join(output_folder, input_file_base.replace('_count.out', "_visual.png"))

# Biases data
with open(input_file, 'r') as rf:
    lines = rf.readlines()
    for i in range(len(lines)):
        if lines[i].startswith("Counter of all Biases Types"):
            biases_data = ast.literal_eval(lines[i+1].strip())
        if lines[i].startswith("Counter of all Signatures"):
            signatures_data = ast.literal_eval(lines[i+1].strip())
        if lines[i].startswith("Top 5 Residue Counts"):
            residue_counts_data = ast.literal_eval(lines[i+1].strip())

# bias
biases_labels = [x[0] for x in biases_data]
biases_counts = [x[1] for x in biases_data]
# Signatures data
signatures_labels = [x[0] for x in signatures_data]
signatures_counts = [x[1] for x in signatures_data]
# Residue counts data
residue_counts_labels = [x[0] for x in residue_counts_data]
residue_counts_values = [x[1] for x in residue_counts_data]

# create subplots
figs, axs = plt.subplots(1,3,figsize=(15,5))

# Plot biases as a pie chart
def plot_biases(ax, biases_counts, biases_labels):
    ax.pie(biases_counts, labels=biases_labels, autopct='%1.1f%%')
    ax.set_title('Compositionally Biased Regions by Biases')

# Plot signatures as a bar chart
def plot_signatures(ax, signatures_labels, signatures_counts):
    ax.bar(signatures_labels, signatures_counts)
    ax.set_xticklabels(signatures_labels, rotation=45, ha='right')
    ax.set_xlabel('Signature')
    ax.set_ylabel('Number of Biased Regions')
    ax.set_title('Compositionally Biased Regions by Signatures')

# Plot residue counts as a line chart
def plot_residue_counts(ax, residue_counts_labels, residue_counts_values):
    ax.plot(residue_counts_labels, residue_counts_values)
    ax.set_xlabel('Residue Number')
    ax.set_ylabel('Number of Biased Regions')
    ax.set_title('Compositionally Biased Regions by Residue Counts')

plot_biases(axs[0], biases_counts, biases_labels)
plot_signatures(axs[1], signatures_labels, signatures_counts)
plot_residue_counts(axs[2], residue_counts_labels, residue_counts_values)
plt.tight_layout()
plt.savefig(output_path)

# print out values 
print(biases_data)
print(signatures_data)
print(residue_counts_data)