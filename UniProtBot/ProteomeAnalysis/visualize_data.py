import subprocess
import glob

if __name__  == '__main__':
    output_folder = "/home/julienh/Desktop/COMP401/Proteomes/CountAnnotations/Visualize_3"
    files = glob.glob("/home/julienh/Desktop/COMP401/Proteomes/CountAnnotations/Annotations_3/*.out")
    for file in files:
        output = subprocess.run(["python3", "/home/julienh/Desktop/COMP401/Proteomes/CountAnnotations/visualize.py", file, output_folder], capture_output=True)
