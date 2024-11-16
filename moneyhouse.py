import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

login = os.environ.get('MONEYHOUSE_LOGIN')
password = os.environ.get('MONEYHOUSE_PASSWORD')

class Moneyhouse:
    driver = None

    def get_selenium_driver(self):
        if self.driver is not None:
            return self.driver
        
        options = Options()
        options.add_argument('--headless')  # Führt den Browser im Hintergrund aus
        options.add_argument('--disable-gpu')  # Deaktiviert die GPU-Beschleunigung, um Ressourcen zu sparen
        driver = webdriver.Chrome(options=options)  # Verwenden Sie hier den Pfad zum heruntergeladenen Webdriver
        self.driver = driver
        
        driver.get('https://www.moneyhouse.ch/de/login?redirectUrl=%2F')

        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'cmpbntyestxt'))
            )
            cookie_button.click()
        except NoSuchElementException:
            pass

        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'email'))
        )
        email_field.send_keys(login)

        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'password'))
        )
        password_field.send_keys(password)

        # Wait for the login button to be clickable
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@type="submit"]'))
        )
        login_button.click()
        
        return self.driver
    
    def search_moneyhouse(self, query):
        driver = self.get_selenium_driver()
        
        driver.get('https://www.moneyhouse.ch/de/search?q=' + query + '&tab=companies')


        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'companies'))
        )

        suup = BeautifulSoup(driver.page_source, 'html.parser')

        companies = suup.select('#companies .responsive-table .row-person-data>a')

        company_data = [
            {
                'name': company.text,
                'url': company['href']
            }
            for company in companies
        ]
        
        return company_data

    def get_moneyhouse_company_info(self, url):
        driver = self.get_selenium_driver()
        
        driver.get('https://www.moneyhouse.ch' + url)

        suup = BeautifulSoup(driver.page_source, 'html.parser')
        main_div = suup.find('div', class_='l-grid center')

        info_divs = main_div.find_all('div', class_='l-grid-cell')

        company_info = {}

        for div in info_divs:
            key = div.find('h4', class_='key').text.strip()
            value = div.find('span').text.strip()
            company_info[key] = value
            
        company_status = suup.find('div', class_='company-status')
            
        return {
            'alter_der_firma': company_info.get('Alter der Firma'),
            'umsatz': company_info.get('Umsatz in CHF'),
            'groesse': company_info.get('Mitarbeiter'),
            'status': company_status.find('span').text.strip()
        }


if __name__ == '__main__':
    moneyhouse = Moneyhouse()
    
    print(moneyhouse.get_moneyhouse_company_info('/de/company/cudos-ag-5193583291'))