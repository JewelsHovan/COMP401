from uniprotbot import UniProtBot

def main():
    uniprot_bot = UniProtBot()

    def run_protscraper():
        uniprot_bot.run_protscraper()

    def run_fLPS2():
        uniprot_bot.run_fLPS2()

    def run_transcripts():
        uniprot_bot.run_transcripts()

    def unzip_files():
        input_file = input("Enter the input file path: ")
        output_path = input("Enter the output path: ")
        uniprot_bot.unzip_files(input_file, output_path)

    def modify_config():
        param_name = input("Enter the parameter name: ")
        new_value = input("Enter the new value: ")
        uniprot_bot.modify_config(param_name, new_value)

    def get_config():
        config = uniprot_bot.get_config()
        print(config)

    def visualize_files():
        output_path = input("Enter the output path: ")
        file_count = int(input("Enter the number of files to process: "))
        files = []
        for i in range(file_count):
            file_path = input(f"Enter the path for file {i + 1}: ")
            files.append(file_path)
        uniprot_bot.visualize_files(output_path, files)

    options = {
        "1": run_protscraper,
        "2": run_fLPS2,
        "3": run_transcripts,
        "4": unzip_files,
        "5": modify_config,
        "6": get_config,
        "7": visualize_files,
    }

    while True:
        print("\nWelcome to UniProtBot!")
        print("Select an option from the list below:")
        print("1. Run ProtScraper")
        print("2. Run fLPS2")
        print("3. Run Transcripts")
        print("4. Unzip Files")
        print("5. Modify Config")
        print("6. Get Config")
        print("7. Visualize Files")
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