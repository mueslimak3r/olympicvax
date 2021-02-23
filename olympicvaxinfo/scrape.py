# Import requests (to download the page)
import requests

# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup

import time
import datetime
import glob
import os
from sendmail import sendmail, testmail
from diffoutputs import diffoutputs
from scrape_bainbridge import scrape_bainbridge
import json

import colorama
from colorama import Fore, Style



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
    "jeffersonhealthcare": 2,
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
        print(Style.DIM + "downloaded" + Style.NORMAL)
        soup = BeautifulSoup(response.text, "html.parser")
        return (soup)
    except:
        print(Fore.RED + "response error!" + Fore.RESET)
        return ("Error") 

def jeffersonhealthcare(name):
    soup = scrape(SOURCE_URLS[name])
    if soup == "Error":
        print(Fore.RED + "jeffersonhealthcare: scraper error" + Fore.RESET)
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
        print(Fore.RED + "islanddrug: scraper error" + Fore.RESET)
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
        print(Fore.RED + "cameronlambert: scraper error" + Fore.RESET)
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

colorama.init()

if "ISSERVER" in os.environ:
    print(Fore.RED + 'RUNNING ON SERVER' + Fore.RESET)
    if not "SECRET_KEY" in os.environ:
        print(Fore.RED + "'SECRET_KEY' not in environ" + Fore.RESET)
        exit()
else:
    print(Fore.RED + 'RUNNING IN TEST MODE' + Fore.RESET)

if "SECRET_KEY" in os.environ:
    os.system('python3 manage.py save-top-posts-to-file --path ' + tmpdir)
else:
    print(Fore.YELLOW + "Warning: 'SECRET_KEY' not in environ" + Fore.RESET)

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
        print(Style.BRIGHT + "name: " + name + Style.NORMAL)
        data = locals()[name](name)
        if data == "Error":
            continue
        #print(tmpdir + name + '/' + '*')
        #print(data)
        list_of_files = glob.glob(tmpdir + name + '/' + '*')
        diffresult = ""
        diff_sample = ""
        if list_of_files:
            latest_file_name = max(list_of_files)
            latest_file = open(latest_file_name, 'r')

            stream = "\n".join(latest_file.read().splitlines()[2:-2])
            datastream = "\n".join(data.splitlines())
            diffresult, diff_sample = diffoutputs(stream, datastream, category_diff_margins[name])
            if diffresult == 'exact match' or diffresult == 'error':
                continue
        else:
            diffresult = 'significant change'
        curtime = time.strftime('%X %x %Z')
        timestamp_name = str(int(time.mktime(datetime.datetime.strptime(curtime[:-4], "%H:%M:%S %m/%d/%y").timetuple())))
        filename = os.path.join(tmpdir, name + '/' + timestamp_name)
        towrite = curtime + '\n' + SOURCE_URLS[name] + '\n' + data + '\n\n' + timestamp_name

        print(filename)
        f = open(filename, 'w+')
        f.write(towrite)
        f.close()
        print(Fore.GREEN + 'change detected. Saved to file at ' + curtime + Fore.RESET) 
        if diffresult == 'significant change':
            print(Fore.YELLOW + 'change posted to database' + Fore.RESET)
            if "ISSERVER" in os.environ and "SECRET_KEY" in os.environ:
                sendmail(name, SOURCE_URLS[name], diff_sample, curtime)
                os.system('python3 manage.py new-post-from-file --path ' + filename + ' --category ' + category_IDs[name])
            else:
                testmail(name, SOURCE_URLS[name], diff_sample, curtime)
    print(Fore.BLUE + "sleeping for " + str(sleeptime) + " seconds" + Fore.RESET)
    time.sleep(sleeptime)
