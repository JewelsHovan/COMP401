import yaml
import subprocess
import shutil
import gzip
import os
import glob
from typing import Dict

class UniProtBot:
    """
    An all-purpose bot for several features specifically designed for Drosophila proteome and research on intrinsically disordered proteins.
    It has many features:
    - Using fLPS2.0 program to annotate compositionally biased regions from fasta files
        - Annotating the fasta files 
        - Visualizing count information from biased regions
    
    - Prot Scraper to scrape proteome/transcriptome from a search keyword (organism, species, protein)
    """

    def __init__(self, config = "configs/config.yaml"):
        self.config = os.path.join(os.getcwd(), config)
        self.config_dict = self.load_config()

    # ======================== Helper/Setup Methods ========================

    def load_config(self):
        """Load the configuration file."""
        try:
            with open(self.config, "r") as f:
                config_dict = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            print(f"Error loading config file: {str(e)}")
            config_dict = {}
        return config_dict
    
    def set_current_directory(self):
        self.current_dir = self.config_dict["CurrentDirectory"]
    
    def return_current_directory(self):
        return self.current_dir
    
    def make_directory(self, dir_name, dir_path):
        """Creates a new directory in the current directory. Returns dir_path of new directory
        """
        os.chdir(dir_path)
        try:
            os.mkdir(dir_name)
        except Exception as e:
            print(f"Error creating directory: {str(e)}")
        return os.path.join(dir_path, dir_name)
    
    def last_worked_species(self):
        return self.config_dict["LastWorkedSpecies"]

    def get_data_dir(self):
        return self.config_dict["DataDir"]
    
    def modify_config(self, param_name, new_value):
        """Modifies a specified parameter in the configuration file."""
        self.config_dict[param_name] = new_value
        try:
            with open(self.config, 'w') as file:
                yaml.dump(self.config_dict, file)
        except Exception as e:
            print(f"Error updating config file: {str(e)}")

    def get_config(self):
        """Returns the current configuration dictionary."""
        return self.config_dict

    def get_config_species(self, species_name):
        """Returns the configuration dictionary for a specific species."""
        species_config_path = os.path.join(os.path.dirname(self.config), species_name)
        with open(f"{species_config_path}.yaml", "r") as rf:
            species_config = yaml.load(rf, Loader=yaml.FullLoader)

        return species_config
    
    def setup_directories(self, dir_path: str):
        """Create the Transcriptome, Proteome, Filtered, and Annotated directories."""
        subdirectories = ['Transcriptome', 'Proteome', 'Filtered', 'Annotated']

        subdir_dict = {}
        for subdirectory in subdirectories:
            subdirectory_path = os.path.join(dir_path, subdirectory)
            if not os.path.exists(subdirectory_path):
                subdir_dict[subdirectory] = subdirectory_path
                os.makedirs(subdirectory_path)

        return subdir_dict 

    def create_config(self, species_name, dict):
        config_path = os.path.join(os.path.dirname(self.config), species_name)
        with open(f'{config_path}.yaml', "w") as wf:
            yaml.dump(dict, wf)
    
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

    # ======================== Proteome Analysis Methods ========================
    
    def run_protscraper(self):
        """Runs the protscraper program to scrape proteome/transcriptome from a search keyword (organism, species, protein)."""
        subprocess.run(["python", "protscraper.py", self.config_dict["protscraper_config"]])
    
    def run_fLPS2(self):
        """Runs the fLPS2.0 program to annotate compositionally biased regions from fasta files."""
        subprocess.run(["python", "fLPS2.0.py", self.config_dict["fLPS2_config"]])
    
    def download_transcripts(self, organism_id_file: str, download_path: str):
        try:
            with open(organism_id_file) as rf:
                text = rf.readlines()
                drosophila_ids = [line.split(' ')[0].strip(':') for line in text]
                get_transcript_script = os.path.join(self.config_dict["Analysis"], "get_transcript.py")
                for id in drosophila_ids:
                    subprocess.run(["python3", get_transcript_script, id, download_path])
        except Exception as e:
            print(f"Error downloading transcripts: {str(e)}")

    def download_proteomes(self, organism_ids_file: str, download_path: str):
        """Downloads proteomes for a list of organism IDs using the get_proteomes.py script."""
        try:
            with open(organism_ids_file, "r") as f:
                organism_ids = [line.split(' ')[0].strip(':') for line in f]

            get_proteome_script = os.path.join(self.config_dict["Analysis"], "get_proteomes.py") # path for script
            for organism_id in organism_ids:
                subprocess.run(["python3", get_proteome_script, organism_id, download_path])

        except Exception as e:
            print(f"Error downloading proteomes: {str(e)}")
    
    def visualize_files(self, output_path, files):
        """
        Runs visualize.py on each file in the specified list of files.

        Args:
        output_path (str): The output path for the graph figures saved.
        files (list[str]): A list of file paths to be processed by visualize.py.
        """
        try:
            for f in files:
                subprocess.run(["python", "visualize.py", f, output_path])
        except Exception as e:
            print(f"Error running visualize.py: {str(e)}")

    def unzip_file(self, input_file, output_path: str, archive_path: str):
        """Unzips a given gzipped fasta file to a specified output path and moves the gzipped file to the archive path."""
        
        # Create the output folder if it does not exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Create the archive folder if it does not exist
        if not os.path.exists(archive_path):
            os.makedirs(archive_path)

        # Open the gz file and extract its contents to a new file in the output folder
        output_name = input_file.split('.')[0]
        with gzip.open(input_file, "rb") as f_in, open(os.path.join(output_path, f"{output_name}.fasta"), "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

        # Move the gzipped file to the archive folder
        shutil.move(input_file, os.path.join(archive_path, os.path.basename(input_file))) 

    def unzip_all_files(self, species_name: str, type_folder: str):
        # Get the downloaded gzip file paths
        species_config = self.get_config_species(species_name)
        gzip_files = [f for f in os.listdir(species_config[type_folder]) if f.endswith(".gz")]
        
        # Unzip the downloaded files
        for gzip_file in gzip_files:
            input_file = os.path.join(species_config[type_folder], gzip_file)
            self.unzip_file(input_file, species_config[type_folder], self.config_dict["ArchiveDir"])

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
