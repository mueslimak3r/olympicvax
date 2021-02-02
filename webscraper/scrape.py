# Import requests (to download the page)
import requests

# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup

import time
import re

SOURCE_URLS = [
    "https://jeffersonhealthcare.org/covid-19-vaccine/",
]

# This is a pretty simple script. The script downloads the homepage of VentureBeat, and if it finds some text, emails me.
# If it does not find some text, it waits 60 seconds and downloads the homepage again.

def scrape(url = None):
    if url == None:
        return
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # download the homepage
    response = requests.get(url, headers=headers)
    # parse the downloaded homepage and grab all text, then,
    soup = BeautifulSoup(response.text, "html.parser")
    return (soup)

def scrape_jeffhealthcare():
    soup = scrape(SOURCE_URLS[0])

    mydivs = soup.findAll("div", {"class": "vc_row"})[1].get_text()
    print ('\r\n'.join([x for x in mydivs.splitlines() if x.strip()]))

while True:
    scrape_jeffhealthcare()
    time.sleep(60)