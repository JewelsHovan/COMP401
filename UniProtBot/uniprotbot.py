import yaml
import subprocess
import shutil
import gzip
import os

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
        self.config = config
        self.config_dict = self.load_config()

    def load_config(self):
        """Load the configuration file."""
        try:
            with open(self.config, "r") as f:
                config_dict = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            print(f"Error loading config file: {str(e)}")
            config_dict = {}
        return config_dict
    
    def run_protscraper(self):
        """Runs the protscraper program to scrape proteome/transcriptome from a search keyword (organism, species, protein)."""
        subprocess.run(["python", "protscraper.py", self.config_dict["protscraper_config"]])
    
    def run_fLPS2(self):
        """Runs the fLPS2.0 program to annotate compositionally biased regions from fasta files."""
        subprocess.run(["python", "fLPS2.0.py", self.config_dict["fLPS2_config"]])
    
    def ProteomeAnalysis(self):
        """Runs the ProteomeAnalysis program to analyze proteome/transcriptome from a search keyword (organism, species, protein)."""
        pass
    
    def run_transcripts(self):
        with open("/home/julienh/Desktop/COMP401/Transcriptome/Drosophila/drosophila_id.txt") as rf:
            text = rf.readlines()
            drosophila_ids = [line.split(' ')[0].strip(':') for line in text]
            for id in drosophila_ids:
                subprocess.run(["python3", "/home/julienh/Desktop/COMP401/Transcriptome/get_transcript.py", id])
    
    def unzip_files(self, input_file, output_path: str):
        """Unzips a given gzipped fasta file to a specified output path."""
        # Create the output folder if it does not exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Open the gz file and extract its contents to a new file in the output folder
        output_name = input_file.split('.')[0]
        with gzip.open(input_file, "rb") as f_in, open(os.path.join(output_path, f"{output_name}.fasta"), "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    
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
