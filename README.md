# Independent Research Project: COMP401
## Conservation of Intrinsically Disordered Protein Regions in Drosophila Species
This repository contains the work for an independent research project in COMP401, which focuses on the analysis of intrinsically disordered protein regions (IDRs) conservation across different Drosophila species. The main tool utilized in this project is UniProtBot, a Python-based automation tool that simplifies the process of downloading and analyzing proteome and transcriptome datasets from UniProt.

### UniProtBot Capabilities
UniProtBot streamlines the following tasks:

- Downloading proteome and transcriptome datasets for multiple Drosophila species from UniProt.
- Extracting and processing fasta files from the downloaded datasets.
- Running the fLPS2.0 software to annotate compositional bias in protein sequences.
- Analyzing and comparing the results across different species to determine the conservation of IDRs.
### Getting Started
To use UniProtBot for your own research project, follow these steps:

- Clone this repository to your local machine.
- Install the required dependencies from the requirements.txt file.
- Set up the configuration file with the appropriate file paths and parameters.
- Run the main script to execute the desired tasks, such as downloading proteomes, transcriptomes, or running fLPS2.0.
### Configuration
The config.yaml file allows you to customize various parameters, such as:

- Input and output folders for proteome and transcriptome data
- fLPS2.0 command line options
- Species to be analyzed
- Sleep time between running fLPS2.0 on different files
- Make sure to update the configuration file with the appropriate values for your project.

### Contributing
If you would like to contribute to this project or have any suggestions, please feel free to create an issue or submit a pull request.
