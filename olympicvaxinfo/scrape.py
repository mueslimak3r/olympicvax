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
    "cameronlambert": "https://cameronlambert.com/",
    #"bainbridgeprepares": "https://covidbi.timetap.com/",
}

category_IDs = {
    "jeffersonhealthcare": "3",
    "cameronlambert": "6",
    #"bainbridgeprepares": "4",
}

basedir = os.path.dirname(os.path.realpath(__file__))
tmpdir = basedir + '/website-dumps/'

def scrape(url = None):
    if url == None:
        return
    #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # download the homepage
    response = requests.get(url)#, headers=headers)
    # parse the downloaded homepage and grab all text, then,
    soup = BeautifulSoup(response.text, "html.parser")
    return (soup)

def jeffersonhealthcare(name):
    soup = scrape(SOURCE_URLS[name])

    mydivs = soup.findAll("div", {"class": "vc_row"})[1].get_text()
    data = '\r\n'.join([x for x in mydivs.splitlines() if x.strip()])
    return data

def cameronlambert(name):
    soup = scrape(SOURCE_URLS[name])

    mydivs = soup.find("p").get_text()
    #data = '\r\n'.join([x for x in mydivs.splitlines() if x.strip()])
    return mydivs

def bainbridgeprepares(name):
    soup = scrape(SOURCE_URLS[name])
    print(soup)
    exit()
    #mydivs = soup.find("div", {"id": "welcomeText"})
    #data = '\r\n'.join([x for x in mydivs.splitlines() if x.strip()])
    return data

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
        print("name: ", name)
        data = locals()[name](name)
        ts = time.time()
        #print(tmpdir + name + '/' + '*')
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
                #print(result)

        filename = os.path.join(tmpdir, name + '/' + str(int(ts)))
        curtime = time.strftime('%X %x %Z')
        towrite = name + ': ' + curtime + '\n' + SOURCE_URLS[name] + '\n' + data

        print(filename)
        f = open(filename, 'w+')
        f.write(towrite)
        f.close()
        print('new dump at ' + curtime)

        os.system('python3 manage.py test_command --path ' + filename + ' --category ' + category_IDs[name])        

    time.sleep(10)