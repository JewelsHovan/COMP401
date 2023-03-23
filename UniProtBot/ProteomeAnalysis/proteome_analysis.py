import yaml
import os
import subprocess
import glob
from typing import Dict

class ProteomeAnalysis:
    def __init__(self, config: str, dir_path: str = None, set_up: bool = False):
        if set_up:
            self.setup_directories(dir_path)

        # open config file
        with open(config, "r") as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
            self.annotation_folder = self.config['ProteomeAnalysis']['annotation_directory']
            self.proteome_fasta_dir = self.config['ProteomeAnalysis']['directory_proteome_fastas']
            self.transciptome_fasta_dir = self.config['ProteomeAnalysis']['directory_transcriptome_fastas']
            self.filtered_directory = self.config['ProteomeAnalysis']['filtered_directory']

    def setup_directories(self, dir_path: str):
        """Create the Transcriptome, Proteome, Filtered, and Annotated directories."""
        subdirectories = ['Transcriptome', 'Proteome', 'Filtered', 'Annotated']

        for subdirectory in subdirectories:
            subdirectory_path = os.path.join(dir_path, subdirectory)
            if not os.path.exists(subdirectory_path):
                os.makedirs(subdirectory_path)

    def count_annotations(self, range: str):
        """Counts annotations for files in the specified folder and writes the results to a new file."""
        files = glob.glob(f'{self.annotation_folder}/*.out')
        for file in files:
            output_path = os.path.join(self.proteome_fasta_dir, os.path.basename(file).replace('.', '_count.'))
            output = subprocess.run(['python3', '/path/to/your/count_biased.py', file.strip('\n'), range], capture_output=True)
            output_str = output.stdout.decode('utf-8')
            with open(output_path, "w") as wf:
                wf.write(output_str)

    def run_sequences(self):
        """Runs the get_sequences.py script for each pair of fasta and annotated files."""
        with open("/path/to/your/drosophila_paths.txt") as rf:
            for line in rf:
                # paths format: fasta_file-annotated_file
                file_names = line.split('-')
                fasta_file = file_names[0]
                annotated_file = file_names[1]
                subprocess.run(["python3", "/path/to/your/get_sequences.py", fasta_file, annotated_file])

    def set_paths(self):
        """Creates a file with pairs of fasta and annotated file paths."""
        os.chdir("/path/to/your/Alignment")
        output_file = "drosophila_paths.txt"
        write_set: Dict[str, str] = {}  # dictionary to make fasta to annotated path pairs

        for filename in os.listdir("/path/to/your/Drosophila"):
            # file path for fasta proteome sequences
            filepath = os.path.join("/path/to/your/Drosophila/", filename)
            for filename_filtered in os.listdir("/path/to/your/Filtered"):
                # filepath for annotated files
                filepath_filtered = os.path.join("/path/to/your/Filtered/", filename_filtered)
                corrected_file_set = filename_filtered.split('.')[0].split('_')
                corrected_filename = "_".join(corrected_file_set[0:2])
                if filename.split('.')[0] == corrected_filename:  # if filename bases are the same add to dictionary
                    write_set[filepath] = filepath_filtered

        with open(output_file, "w") as wf:
            for key, value in write_set.items():
                wf.write(key + "-" + value + "\n")


