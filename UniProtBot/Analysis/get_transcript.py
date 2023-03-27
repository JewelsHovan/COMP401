import argparse
import os
from bs4 import BeautifulSoup
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
from time import sleep


@contextmanager
def setup_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)
    try:
        yield driver
    finally:
        driver.quit()


def get_entry_id(organism_id, driver):
    search_url = f"https://www.uniprot.org/proteomes?query={organism_id}"
    driver.get(search_url)
    sleep(4)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    second_row = rows[1]
    anchors = second_row.find_all('a')
    entry_id = anchors[0].text

    return entry_id


def get_ref_url(entry_id, driver):
    ref_url = f"https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/{entry_id}/"
    driver.get(ref_url)
    sleep(3)
    return ref_url

def download_fasta(ref_url, download_path):
    try:
        response = requests.get(ref_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        
        fasta_link = None
        for link in links:
            if link.text.endswith('DNA.fasta.gz'):
                fasta_link = link['href']
                break

        if fasta_link is not None:
            fasta_url = ref_url + fasta_link
            response = requests.get(fasta_url)
            file_name = os.path.join(download_path, fasta_link)
            with open(file_name, 'wb') as f:
                f.write(response.content)
        else:
            print("Fasta file not found.")

    except Exception as e:
        print(e)

def main(organism_id, download_path):
    with setup_chrome_driver() as driver:
        entry_id = get_entry_id(organism_id, driver)
        print(entry_id)
        ref_url = get_ref_url(entry_id, driver)
        # change the directory 
        download_fasta(ref_url, download_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve the fasta file of proteome of organism id in UniProt')
    parser.add_argument('organism_id', type=int, help="Organism ID to retrieve cDNA fasta file")
    parser.add_argument('download_path', type=str, help="The download path of the gzip fasta files")
    args = parser.parse_args()
    main(args.organism_id, args.download_path)
