import os
import gzip
import shutil
import glob

def unzip_file(input_file, output_folder):
    # Create the output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the gz file and extract its contents to a new file in the output folder
    output_name = input_file.split('.')[0]
    with gzip.open(input_file, "rb") as f_in, open(os.path.join(output_folder, f"{output_name}.fasta"), "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)


if __name__ == "__main__":
    gz_files = glob.glob("*.gz")
    output_folder = "/home/julienh/Desktop/COMP401/Transcriptome/Drosophila"
    for file in gz_files:
        unzip_file(file, output_folder)
