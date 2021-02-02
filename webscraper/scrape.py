# Import requests (to download the page)
import requests

# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup

import time
import glob
import re
import os





SOURCE_URLS = {
    "jeffersonhealthcare": "https://jeffersonhealthcare.org/covid-19-vaccine/",
}

tmpdir = os.path.dirname(os.path.realpath(__file__)) + '/website-dumps/'

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
    soup = scrape(SOURCE_URLS['jeffersonhealthcare'])

    mydivs = soup.findAll("div", {"class": "vc_row"})[1].get_text()
    data = '\r\n'.join([x for x in mydivs.splitlines() if x.strip()])
    return data





SOURCE_FUNCTIONS = {
    "jeffersonhealthcare": scrape_jeffhealthcare,
}

# set up folder structure to save page dumps for each source in their own subdirectory
try:
    os.mkdir(tmpdir)
except:
    pass

for name in SOURCE_URLS:
    path = os.path.join(tmpdir, name)
    try:
        os.mkdir(path)
    except:
        pass

import difflib

while True:
    for name in SOURCE_URLS:
        data = SOURCE_FUNCTIONS[name]()
        ts = time.time()

        list_of_files = glob.glob(tmpdir + name + '/' + '*')
        if list_of_files:
            latest_file_name = max(list_of_files)
            latest_file = open(latest_file_name, 'r')

            stream = latest_file.read().splitlines()[2:]
            datastream = data.splitlines()

            if (stream == datastream):
                print('no change')
                continue
            else:
                print('detected change')

                d = difflib.Differ()
                result = list(d.compare(stream, datastream))
                print(result)

        filename = os.path.join(tmpdir, name + '/' + str(int(ts)))
        curtime = time.strftime('%X %x %Z')
        towrite = str(int(ts)) + '\n' + curtime + '\n' + data

        f = open(filename, 'w+')
        f.write(towrite)
        f.close()
        print('new dump at ' + curtime)  
        

    time.sleep(10)