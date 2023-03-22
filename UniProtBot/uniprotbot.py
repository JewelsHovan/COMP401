import yaml
import subprocess
import shutil
import gzip
import os

class UniProtBot:
    """
    An all purpose bot for several features specifically designed for Drosophila proteome and research on intrinsically disordered proteins.
    It has many features:
    - Using fLPS2.0 program to annotate compositionally biased regions from fasta files
        - Annotating the fasta files 
        - Visualizing count information from biased regions
    
    - Prot Scraper to scrape proteome/transcriptome from a search keyword (organism, species, protein)
    """

    def __init__(self, config = "configs/config.yaml"):
        self.config = config

        # open config file to 
        with open(self.config, "wr") as f:
            config_dict = yaml.load(f, loader=yaml.FullLoader)
    
            
    
    def run_protscraper(self):
        """
        Runs the protscraper program to scrape proteome/transcriptome from a search keyword (organism, species, protein)
        """
        # open config file to 
        with open(self.config, "wr") as f:
            config_dict = yaml.load(f, loader=yaml.FullLoader)

        # run protscraper
        subprocess.run(["python", "protscraper.py", config_dict["protscraper_config"]])
    
    def run_fLPS2(self):
        """
        Runs the fLPS2.0 program to annotate compositionally biased regions from fasta files
        """
        # open config file to 
        with open(self.config, "wr") as f:
            config_dict = yaml.load(f, loader=yaml.FullLoader)

        # run fLPS2.0
        subprocess.run(["python", "fLPS2.0.py", config_dict["fLPS2_config"]])
    
    def ProteomeAnalysis(self):
        """
        Runs the ProteomeAnalysis program to analyze proteome/transcriptome from a search keyword (organism, species, protein)
        - ProteomeAnalysis can get information like
            - count of signatures
            - 
        """
        # open config file to 
        with open(self.config, "wr") as f:
            config_dict = yaml.load(f, loader=yaml.FullLoader)

        # create ProteomeAnalysis instance
    
    def run_transcripts(self):
        with open("/home/julienh/Desktop/COMP401/Transcriptome/Drosophila/drosophila_id.txt") as rf:
            text = rf.readlines()
            drosophila_ids = [line.split(' ')[0].strip(':') for line in text]
            for id in drosophila_ids:
                subprocess.run(["python3", "/home/julienh/Desktop/COMP401/Transcriptome/get_transcript.py", id])
    
    def unzip_files(self, input_file, output_path: str):
        # Create the output folder if it does not exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Open the gz file and extract its contents to a new file in the output folder
        output_name = input_file.split('.')[0]
        with gzip.open(input_file, "rb") as f_in, open(os.path.join(output_path, f"{output_name}.fasta"), "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    

    def modify_config(self, param_name, new_value):
        with open(self.config, 'r') as file:
            config = yaml.safe_load(file)

        config[param_name] = new_value

        with open(self.config, 'w') as file:
            yaml.dump(config, file)
            