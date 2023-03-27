from uniprotbot import UniProtBot
import os

def main():
    uniprot_bot = UniProtBot()

    def download_proteome():
        ''' Download a list of proteome fasta files from UniProt.org based off a list of organisms IDs'''
        input_dir = "Input"
        
        print(f"To download the proteomes of the species: {uniprot_bot.last_worked_species()}")
        print("A text file of the organism IDs is required")
        print("Here are a list of the files in Input/")

        # List all files in the input directory
        files = os.listdir(input_dir)

        # Filter the files to only include .txt files
        txt_files = [f for f in files if f.endswith(".txt")]

        if len(txt_files) == 0:
            print("No files in Input/ please make a text file and with each new line corresponding to the organism ID of the species")
            return

        # Display the files with numbered options
        for idx, txt_file in enumerate(txt_files, start=1):
            print(f"{idx}. {txt_file}")

        selected_option = int(input("Which option to choose?: "))

        # Check if the selected option is valid
        if 1 <= selected_option <= len(txt_files):
            selected_file = txt_files[selected_option - 1]
            print(f"You selected: {selected_file}")
            # call download_transcripts method of UniProtBot
            file_path = os.path.join(uniprot_bot.config_dict["InputDir"], selected_file) # file path of txt file
            species_config = uniprot_bot.get_config_species(uniprot_bot.last_worked_species())
            download_path = species_config["Proteome"]
            uniprot_bot.download_proteomes(file_path, download_path)

            # unzip and archive gzip files
            uniprot_bot.unzip_all_files(uniprot_bot.config_dict["LastWorkedSpecies"], "Proteome")
        else:
            print("Invalid option, please try again.")

    def download_transcriptome():
        ''' Download a list of transcriptome fasta files from UniProt.org based off a list of organisms IDs'''
        input_dir = "Input"

        print(f"To download the transcriptomes of the species: {uniprot_bot.last_worked_species()}")
        print("A text file of the organism IDs is required")
        print("Here are a list of the files in Input/")

        # List all files in the input directory
        files = os.listdir(input_dir)

        # Filter the files to only include .txt files
        txt_files = [f for f in files if f.endswith(".txt")]

        if len(txt_files) == 0:
            print("No files in Input/ please make a text file and with each new line corresponding to the organism ID of the species")
            return

        # Display the files with numbered options
        for idx, txt_file in enumerate(txt_files, start=1):
            print(f"{idx}. {txt_file}")

        selected_option = int(input("Which option to choose?: "))

        # Check if the selected option is valid
        if 1 <= selected_option <= len(txt_files):
            selected_file = txt_files[selected_option - 1]
            print(f"You selected: {selected_file}")
            # call download_transcripts method of UniProtBot
            file_path = os.path.join(uniprot_bot.config_dict["InputDir"], selected_file) # file path of txt file
            species_config = uniprot_bot.get_config_species(uniprot_bot.last_worked_species())
            download_path = species_config["Transcriptome"]
            uniprot_bot.download_transcripts(file_path, download_path)

            # unzip and archive gzip files
            uniprot_bot.unzip_all_files(uniprot_bot.config_dict["LastWorkedSpecies"], "Transcriptome")
        else:
            print("Invalid option, please try again.")

    def run_fLPS2():
        print("fLPS2.0 is a software used to annotate composotionally biased regions in sequences")
        uniprot_bot.run_fLPS2()

    def modify_config():
        param_name = input("Enter the parameter name: ")
        new_value = input("Enter the new value: ")
        uniprot_bot.modify_config(param_name, new_value)

    def get_config():
        config = uniprot_bot.get_config()
        print(config)

    def count_annotations():
        pass

    def visualize_files():
        output_path = input("Enter the output path: ")
        file_count = int(input("Enter the number of files to process: "))
        files = []
        for i in range(file_count):
            file_path = input(f"Enter the path for file {i + 1}: ")
            files.append(file_path)
        uniprot_bot.visualize_files(output_path, files)
    

    options = {
        "1": download_transcriptome,
        "2": download_proteome,
        "3": run_fLPS2,
        "4": count_annotations,
        "5": visualize_files,
        "6": modify_config,
        "7": get_config
    }

    # interactive loop
    while True:
        print("\nWelcome to UniProtBot!")
        last_worked = uniprot_bot.last_worked_species()
        if last_worked == "None":
            print("No species previously worked on\n Do you want to setup directories for a new species?")
            option_continue = input("\nEnter your choice (y/n): ")
            if option_continue.lower() == "y":
                input_species = input("What is the name of the species?: ").capitalize()
                species_path = uniprot_bot.make_directory(input_species, uniprot_bot.get_data_dir())
                uniprot_bot.modify_config("LastWorkedSpecies", input_species)
                uniprot_bot.modify_config("CurrentDirectory", species_path)
                subdir_dict = uniprot_bot.setup_directories(species_path)
                uniprot_bot.create_config(input_species, subdir_dict)
        else:
            print(f"Last worked species: {uniprot_bot.last_worked_species()}")

        # options
        print("Select an option from the list below:")
        print("1. Download Transcriptome Sequences")
        print("2. Download Proteome Sequences")
        print("3. Annotate with fLPS2")
        print("4. Count Annotation Files")
        print("5. Visualize Annotation Files")
        print("6. Modify Config")
        print("7. Print Current Config")
        print("0. Exit")

        option = input("\nEnter your choice (0-7): ")
        if option == "0":
            print("Exiting UniProtBot.")
            break
        elif option in options:
            options[option]()
        else:
            print("Invalid choice. Please enter a number between 0 and 7.")

if __name__ == "__main__":
    main()