
from bs4 import BeautifulSoup
import requests
import json
import os
from csv import writer
from tqdm import tqdm, trange
from string import digits
from os.path import exists
from random import randrange
import time

class CityData:
    def __init__(self,name,state):
        self.name = name
        self.state = state
            
    def write_csv(self):
        filename = './data/tourist_attractions.csv'
        if not exists(filename):
            with open(filename, "x") as file:
                file.write("Name,State\n")
        with open(filename, "a", encoding='utf-8') as file:
            file.write(self.info())

    def info(self):
        rep = '"' + '","'.join([self.name, self.state]) + '"\n'    
        return rep

def get_stateurl(source_url,soup):
    #get url linked to each state
    urls=soup.select('div[id="tabs_by_category"]>ul[class="tab-list tab-list-short"] > li > a')
    state_urls={url['href'].split('/')[-1].split('.')[0]:'https:' + url['href'] for url in urls}
    return state_urls

source = "https://www.city-data.com/articles/"
#tabs_by_category
response = requests.get(source).text
soup = BeautifulSoup(response, 'html.parser')
state_urls=get_stateurl(source,soup)


for state_page_name, state_url in tqdm(state_urls.items()):
    filename = './cache/' + state_page_name + '.json'
    if  not exists(filename):
        with requests.get(state_url, stream=True) as x:
            response=x.text
            soup = BeautifulSoup(response, 'html.parser')
    # read the site pages
            site_urls = soup.select('div[id="listing"] > div[class="col-md-4"] > a')
            site_dict = {}
            for site_url in site_urls:
                key = 'https://www.city-data.com' + site_url['href']
                with requests.get('https://www.city-data.com' + site_url['href'], stream=True) as r:# to avoid error
                    value=r.text
                    site_dict[key] = value
                time.sleep(0.1) # add a gap to prevent being blocked
        filename = './cache/' + state_page_name + '.json'
        with open(filename, 'w+') as json_file:
            json.dump(site_dict, json_file, indent=4)
        time.sleep(300)
   
 
        

def get_cache_site_page(state_page_name, site_url):
    # helper function: get response of a site page, return None if not exist
    filename = './cache/' + state_page_name + '.json'
    try:
        with open(filename) as json_file:
            site_dict = json.load(json_file)
            response = site_dict[site_url]
    except:
        return None
    
    return response

def get_site_instance(state_page_name, site_url):
    # get the site instance for a site page from a state_page_name and site_url
    response = get_cache_site_page(state_page_name, site_url)
    soup = BeautifulSoup(response, 'html.parser')
    
    state = state_page_name.translate(str.maketrans('', '', digits))
    title = soup.select('h1[class="city"] > span')[0].contents[0]
    if title.count(' - ') == 2:
        name = title.split(' - ')[0]
    elif title.count(', ') == 2:
        name = title.split(', ')[0]
    else:
        name = title

    touristsite = CityData(name.replace('"', ""),
                              state.replace('"', ""))
    
    return touristsite
def get_cache_sites_for_state_page(state_page_name):
    # get a list of site urls given the state page
    filename = './cache/' + state_page_name + '.json'
    try:
        with open(filename) as json_file:
            site_dict = json.load(json_file)
    except:
        return None
    
    site_list = list(site_dict.keys())
    return site_list


# write to the csv file

for state_page_name, state_url in tqdm(state_urls.items()):
    
    site_list = get_cache_sites_for_state_page(state_page_name)
    filename = './data/tourist_attractions.csv'
    if not exists(filename) :
        for site_url in tqdm(site_list):
            try:
                site = get_site_instance(state_page_name, site_url)
                site.write_csv()
            except:
                pass


