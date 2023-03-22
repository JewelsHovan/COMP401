from UniProtBot.ProtScraper.prot_scraper import ProtScraper


if __name__ == "__main__":
    scraper = ProtScraper('Drosophila', 10000, 25000)
    scraper.initialize_webdriver()
    scraper.goTo('https://www.uniprot.org/proteomes?dir=descend&query=Drosophila&sort=protein_count')