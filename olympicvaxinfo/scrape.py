# Import requests (to download the page)
import requests

# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup

import time
import datetime
import glob
import os

from sendmail import sendmail

import json




sleeptime = 300

SOURCE_URLS = {
    "jeffersonhealthcare": "https://jeffersonhealthcare.org/covid-19-vaccine/",
    #"cameronlambert": "https://cameronlambert.com/",
    #"bainbridgeprepares": "https://covidbi.timetap.com/businessWeb/csapi/cs/scheduler/handle/covidbi?unpublished=false",
}

category_IDs = {
    "jeffersonhealthcare": "3",
    #"cameronlambert": "6",
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

def cameronlambert(name):
    soup = scrape(SOURCE_URLS[name])
    if soup == "Error":
        print("worked")
        return soup

    mydivs = soup.findAll("a")
    data = ""
    #for div in mydivs:
    for div in range(len(mydivs)):
        tmptext = mydivs[div].get_text()
        tmptext = '\n'.join([x for x in tmptext.splitlines() if x.strip()])
        data = data + '\n\n\n' + tmptext
    #print(data)
    return data

def bainbridgeprepares(name):
    #soup = scrape(SOURCE_URLS[name])


    '''
headers = {
        'authority': 'covidbi.timetap.com',
        'method': 'GET',
        'path': "/businessWeb/csapi/cs/scheduler/handle/covidbi?unpublished=false",
        'scheme': 'https',
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US',
        'authorization': 'Bearer cst:340692:covidbi:r9d0bc0b5a0e746ba9e88232c2e84c391',
        'content-type': 'application/json',
        'cookie': 'JSESSIONID=8C67F44DD48E3D4BCF77042D2764C634.worker1',
        'dnt': '1',
        'referer': "https://covidbi.timetap.com/?fbclid=IwAR2cZCeGl1Uo6zxdMJlv1eDXwugGRuvH3Uu5JT_uipLDdS4IK4B70vlXFgo",
        'sec-ch-ua': 'Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
    }
    '''
    headers = {
        'authority': 'covidbi.timetap.com',
        'method': 'GET',
        'path': "/businessWeb/csapi/cs/scheduler/handle/covidbi?unpublished=false",
        'scheme': 'https',
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US',
        'authorization': 'Bearer cst:340692:covidbi:r9d0bc0b5a0e746ba9e88232c2e84c391',
        'content-type': 'application/json',
        'cookie': '',
        'dnt': '1',
        'referer': "https://covidbi.timetap.com/",
        'sec-ch-ua': 'Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
    }
    response = requests.get(SOURCE_URLS[name], timeout = 5, headers=headers)

    #soup = BeautifulSoup(response.text, "json.parser")
    #soup = json.loads(response.json)
    #dictionary = json.loads(str(response.text))
    #rint(dictionary['welcomeText'])
    print(response)
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
        #print(data)
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
        sendmail("Jeffco Mailing List: New Post", towrite)

        os.system('python3 manage.py new-post-from-file --path ' + filename + ' --category ' + category_IDs[name])        

    print("sleeping for " + str(sleeptime) + " seconds")
    time.sleep(sleeptime)
