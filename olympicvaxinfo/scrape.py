# Import requests (to download the page)
import requests

# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup

import time
import datetime
import glob
import re
import os



sleeptime = 10

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
        print("bad")
        return soup

    mydivs = soup.findAll("div", {"class": "vc_row"})[1].get_text()
    data = '\r\n'.join([x for x in mydivs.splitlines() if x.strip()])
    return data

def cameronlambert(name):
    soup = scrape(SOURCE_URLS[name])
    if soup == "Error":
        print("worked")
        return soup

    mydivs = soup.find("p").get_text()
    #data = '\r\n'.join([x for x in mydivs.splitlines() if x.strip()])
    return mydivs

def bainbridgeprepares(name):
    soup = scrape(SOURCE_URLS[name])
    print(soup)
    
    return "Error"
    #mydivs = soup.find("div", {"id": "welcomeText"})
    #data = '\r\n'.join([x for x in mydivs.splitlines() if x.strip()])


# set up folder structure to save page dumps for each source in their own subdirectory

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
        list_of_files = glob.glob(tmpdir + name + '/' + '*')
        if list_of_files:
            latest_file_name = max(list_of_files)
            latest_file = open(latest_file_name, 'r')

            stream = latest_file.read().splitlines()[2:-2]
            datastream = data.splitlines()

            if (stream == datastream):
                print('no change')
                continue
            else:
                print('detected change')

                d = difflib.Differ()
                result = list(d.compare(stream, datastream))
                #print(result)

        curtime = time.strftime('%X %x %Z')
        timestamp_name = str(int(time.mktime(datetime.datetime.strptime(curtime[:-4], "%H:%M:%S %m/%d/%y").timetuple())))
        filename = os.path.join(tmpdir, name + '/' + timestamp_name)
        towrite = name + ': ' + curtime + '\n' + SOURCE_URLS[name] + '\n' + data + '\n\n' + timestamp_name

        print(filename)
        f = open(filename, 'w+')
        f.write(towrite)
        f.close()
        print('new dump at ' + curtime)

        


        os.system('python3 manage.py new-post-from-file --path ' + filename + ' --category ' + category_IDs[name])        

    print("sleeping for " + str(sleeptime) + " seconds")
    time.sleep(sleeptime)