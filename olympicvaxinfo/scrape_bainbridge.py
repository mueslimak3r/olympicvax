from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import os

import colorama
from colorama import Fore, Style

timeout = 8

def scrape_bainbridge(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1024x1400")

    # download Chrome Webdriver  
    # https://sites.google.com/a/chromium.org/chromedriver/download
    # put driver executable file in the script directory
    chrome_driver = '/usr/bin/chromedriver'#os.path.join(os.getcwd(), "chromedriver")

    try:
        driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver)
    except:
        print(Fore.RED + "bainbridge scraper: timeout" + Fore.RESET)
        return ("Error")
    print(Style.DIM + "chrome driver started" + Style.NORMAL)
    driver.get(url)

    try:
        xyz = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR,'mat-card-content')))
    except TimeoutException:
        print(Fore.RED + "\tJavascript Web Scraper: Timed out" + Fore.RESET)
        return "Error"
    print(Style.DIM + "page loaded" + Style.NORMAL)
    element = driver.find_element(By.TAG_NAME, 'div')

    elements = element.find_elements(By.TAG_NAME, 'mat-card-content')
    lines = []
    for e in elements:
        lines.append(e.text)
    data = ''.join(lines)
    driver.quit()
    return data

if __name__ == '__main__' : 
    data = scrape_bainbridge("https://covidbi.timetap.com/")
    print(data)