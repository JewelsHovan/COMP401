from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import  BeautifulSoup
from time import sleep
import argparse

# command line arguments
parser = argparse.ArgumentParser(description='Retrieve the fasta file of cDNA of organism id in UniProt')
parser.add_argument('organism_id', type=int, help="Organism ID to retrieve cDNA fasta file")
args = parser.parse_args()

# setting up chrome webdriver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)

# get the entry_id from uniprot search using organism id
organism_id = args.organism_id
search_url = f"https://www.uniprot.org/proteomes?query={organism_id}"
driver.get(search_url)
sleep(5)
page_source= driver.page_source

# parse content 
soup = BeautifulSoup(page_source, 'html.parser')
table = soup.find('table')
rows = table.find_all('tr')
second_row = rows[1]
anchors = second_row.find_all('a')
entry_id = anchors[0].text
print(entry_id)

# from first table entry 
ref_url = f"https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/{entry_id}/"
driver.get(ref_url)
sleep(3)

# download the dna fasta file
try:
    download_link = driver.find_element(By.XPATH, "/html/body/pre/a[12]")
    download_link.click()
    sleep(10)
except Exception as e:
    print(e)
