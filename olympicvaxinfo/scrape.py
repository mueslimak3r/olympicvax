# Import requests (to download the page)
import requests

# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup

import time
import datetime
import glob
import os

from sendmail import sendmail
from diffoutputs import diffoutputs
from scrape_bainbridge import scrape_bainbridge
import json




sleeptime = 300

SOURCE_URLS = {
    "jeffersonhealthcare": "https://jeffersonhealthcare.org/covid-19-vaccine/",
    #"cameronlambert": "https://cameronlambert.com/",
    "bainbridgeprepares": "https://covidbi.timetap.com/",
    "islanddrug": "https://islanddrug.com/pages/covidvaccine/",
}

category_IDs = {
    "jeffersonhealthcare": "3",
    #"cameronlambert": "6",
    "bainbridgeprepares": "4",
    "islanddrug": "7",
}

category_diff_margins = {
    "jeffersonhealthcare": 3,
    #"cameronlambert": 1,
    "bainbridgeprepares": 1,
    "islanddrug": 2,
}

basedir = os.path.dirname(os.path.realpath(__file__))
tmpdir = basedir + '/website-dumps/'

def scrape(url = None):
    if url == None:
        return

    try:
        response = requests.get(url, timeout = 5)
        print("downloaded")
        soup = BeautifulSoup(response.text, "html.parser")
        return (soup)
    except:
        print("response error!")
        return ("Error") 

def jeffersonhealthcare(name):
    soup = scrape(SOURCE_URLS[name])
    if soup == "Error":
        print("jeffersonhealthcare: scraper error")
        return "Error"

    mydivs = soup.findAll("div", {"class": "vc_column-inner"})

    data = ""
    #for div in mydivs:
    for div in range(len(mydivs)):
        tmptext = mydivs[div].get_text()
        tmptext = '\n'.join([x for x in tmptext.splitlines() if x.strip()])
        data = data + '\n\n\n' + tmptext
        #print(tmptext)
    #print(data)
    return data

def islanddrug(name):
    soup = scrape(SOURCE_URLS[name])
    if soup == "Error":
        print("islanddrug: scraper error")
        return "Error"

    mydivs = soup.findAll("div", {"class": "entry-content"})

    if mydivs:
        text = mydivs[0].get_text()
        data = '\n'.join([x for x in text.splitlines() if x.strip()])
        return (data)
    return "Error"

def cameronlambert(name):
    soup = scrape(SOURCE_URLS[name])
    if soup == "Error":
        print("worked")
        return soup

    mydivs = soup.findAll("a")
    data = ""
    for div in range(len(mydivs)):
        tmptext = mydivs[div].get_text()
        tmptext = '\n'.join([x for x in tmptext.splitlines() if x.strip()])
        data = data + '\n\n\n' + tmptext
    #print(data)
    return data

def bainbridgeprepares(name):
    data = scrape_bainbridge(SOURCE_URLS[name])
    if data == "Error":
        return "Error"
    return data

os.system('python3 manage.py save-top-posts-to-file --path ' + tmpdir)

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
        if data == "Error":
            continue
        #print(tmpdir + name + '/' + '*')
        #print(data)
        list_of_files = glob.glob(tmpdir + name + '/' + '*')
        if list_of_files:
            latest_file_name = max(list_of_files)
            latest_file = open(latest_file_name, 'r')

            stream = "\n".join(latest_file.read().splitlines()[2:-2])
            datastream = "\n".join(data.splitlines())

            if (diffoutputs(stream, datastream, category_diff_margins[name]) == False):
                continue

        curtime = time.strftime('%X %x %Z')
        timestamp_name = str(int(time.mktime(datetime.datetime.strptime(curtime[:-4], "%H:%M:%S %m/%d/%y").timetuple())))
        filename = os.path.join(tmpdir, name + '/' + timestamp_name)
        towrite = curtime + '\n' + SOURCE_URLS[name] + '\n' + data + '\n\n' + timestamp_name

        print(filename)
        f = open(filename, 'w+')
        f.write(towrite)
        f.close()
        print('new dump at ' + curtime)
        sendmail(name, SOURCE_URLS[name], data, curtime)

        os.system('python3 manage.py new-post-from-file --path ' + filename + ' --category ' + category_IDs[name])        

    print("sleeping for " + str(sleeptime) + " seconds")
    time.sleep(sleeptime)
