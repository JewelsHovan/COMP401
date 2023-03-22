from PyQt6.QtCore import QThread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
from enum import Enum

options = webdriver.ChromeOptions() 
options.add_argument("--start-maximized=false")
# to supress the error messages/logs
options.add_experimental_option('excludeSwitches', ['enable-logging'])

class resultType(Enum):
    TABLE = '/html/body/form/div/span/label[2]/input'
    CARDS = '/html/body/form/div/span/label[1]/input'

class ProtScraper:
    def __init__(self, species, min_prot, max_prot, runHeadless = False):
        self.runHeadless = runHeadless
        # filter values inputted
        self.species = species
        self.min_prot = min_prot
        self.max_prot = max_prot

    def initialize_webdriver(self):
        # start driver
        if self.runHeadless: # headless mode 
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options, executable_path=r'/home/julienh/webdrivers/chromedriver.exe')
    
    def goTo(self, weburl):
        self.driver.get(weburl)
    
    def wait(self, wait_time):
        sleep(wait_time)
    
    def enter_result_style(self, type: resultType):
        type_radio = self.driver.find_element(By.XPATH, type.value)
        type_radio.click()

        submit_results_bt = self.driver.find_element(By.XPATH, '/html/body/form/div/section/button')
        submit_results_bt.click()
        
    
    def enter_query(self, query):
        query_input = self.driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/header/div/div[3]/section/form/div[2]/input')
        query_submit = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/header/div/div[3]/section/form/button')
        query_input.clear() # clear the existing search 
        query_input.send_keys(query)
        query_submit.click()
    
    def scroll_down(self):
        table = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/main/table')
        table.click()
        num_rows = len(table.find_elements(By.TAG_NAME, 'tr'))
        print(num_rows)
        scroll_position = 0
        scroll_amount = 10
        while scroll_position < num_rows:
            # simulate the arrow down key press to scroll down the table
            table.send_keys(Keys.ARROW_DOWN * scroll_amount)

            # update the position of the scroll bar
            scroll_position += scroll_amount
        
    
    def save_page_source(self):
        # set the timeout for the explicit wait
        timeout = 10

        # scroll down the page until all table nodes are loaded
        while True:
            # get the height of the page
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            print(last_height)

            # scroll down the page
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # wait for the table nodes to appear
            try:
                WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located((By.XPATH, '//table//tr')))
            except:
                break

            # get the new height of the page
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            # check if we have scrolled to the bottom of the page
            if new_height == last_height:
                break

        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        trs = soup.find_all('tr')
        td_list = []
        for tr in trs:
            td_elements = tr.find_all('td')
            td_text = [td.text for td in td_elements]
            td_text = td_text[1:5]
            td_list.append(td_text)
            
        with open("page.html", 'w') as wf:
            for td in td_list:
                wf.write(str(td))
                wf.write('\n')
        


if __name__ == '__main__':
    scraper = ProtScraper('Drosophila', 10000, 25000)
    scraper.initialize_webdriver()
    scraper.goTo('https://www.uniprot.org/proteomes?dir=descend&query=Drosophila&sort=protein_count')
    scraper.wait(5)
    scraper.enter_result_style(resultType.TABLE)
    scraper.wait(3)
    #scraper.scroll_down()
    #scraper.save_page_source()
    #scraper.wait(15)