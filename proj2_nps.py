## proj_nps.py
## Skeleton for Project 2, Fall 2018
## ~~~ modify this file, but don't rename it ~~~
from secrets import google_places_key

from bs4 import BeautifulSoup
from alternate_advanced_caching import Cache
import requests
from datetime import datetime

import json
## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NationalSite():
    def __init__(self, type, name, desc, url=None):
        self.type = type
        self.name = name
        self.description = desc
        self.url = url

        # needs to be changed, obvi.
        self.address_street = '123 Main St.'
        self.address_city = 'Smallville'
        self.address_state = 'KS'
        self.address_zip = '11111'

    # NationalSite  class should have a __str__ method that returns a string of the following form: <name> (<type>): <address string>
    # Isle Royale (National Park): 800 East Lakeshore Drive, Houghton, MI 49931
    def __str__(self):
        return '''{} ({}): {}, {}, {} {}'''.format(self.name, self.type, self.address_street, self.address_city, self.address_state, self.address_zip)

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NearbyPlace():
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

## Must return the list of NationalSites for the specified state
## param: the 2-letter state abbreviation, lowercase
##        (OK to make it work for uppercase too)
## returns: all of the NationalSites
##        (e.g., National Parks, National Heritage Sites, etc.) that are listed
##        for the state at nps.gov
## The function should return a list of NationalSite instances that are in that state.
def get_sites_for_state(state_abbr):
    ###################
    #     CONFIG      #
    ###################
    cache_file = "nps.json"
    site="nps"
    topic=state_abbr
    cache = Cache(cache_file)
    base = "https://www.nps.gov/state/{}/index.htm".format(state_abbr)

    #######################
    #     RUN PROGRAM     #
    #######################
    UID = create_id(site, topic)
    response = cache.get(UID)

    if response == None:
        response = requests.get(base).text
        cache.set(UID, response, 1)

    soup = BeautifulSoup( response, 'html.parser')
    parks = soup.find( id="list_parks").find_all(class_='clearfix')

    ### Information you should get for each National Site will include the site name, site type, and the physical (or mailing) address. 
    national_park_list = []
    for park in parks:
        site_name = park.find('h3').text
        site_type = park.find('h2').text
        site_desc = park.find('p').text

        address_url = park.find_all('a')[2].get('href')
        response_add = requests.get(address_url).text
        soup_add = BeautifulSoup( response_add, 'html.parser')
        # site_address = soup_add.find(class_='physical-address')

        address_street = soup_add.find(itemprop='streetAddress').text
        address_city = soup_add.find(itemprop='addressLocality').text
        address_state = soup_add.find(itemprop='addressRegion').text
        address_zip = soup_add.find(itemprop='postalCode').text

        temp = [site_name, site_type, site_desc, address_street, address_city, address_state, address_zip]
        national_park_list.append(temp)
    for i in national_park_list:
        print("""{},{},{},{},{},{},{}""".format( i[0], i[1], i[2], i[3], i[4], i[5], i[6]))

def create_id(site, topic):
    return "{}_{}_{}.json".format(site, topic, str(datetime.now()).replace(' ', ''))


national_parks = get_sites_for_state("MI")



### Part 2 ###
########################################################################################################
if google_places_key == "" or not google_places_key:
    print("Your google api key is missing from the file. Enter your google api key where directed and save the program!")
    exit()

cache_file = "part2.json"
site="google"
topic="nearby"
cache = Cache(cache_file)

## Must return the list of NearbyPlaces for the specifite NationalSite
## param: a NationalSite object
## returns: a list of NearbyPlaces instance within 10km of the given site
##          if the site is not found by a Google Places search, this should
##          return an empty list
def get_nearby_places_for_site(national_site):
    baseurl = "https://maps.googleapis.com/maps/api/place/nearbysearch/output?parameters"
    params_diction = {}
    params_diction["api_key"] = google_places_key
    params_diction["radius"] = 10000
    params_diction["name"] = national_site.name + ' ' + national_site.type

    UID = create_id(site, topic)
    response = cache.get(UID)

    if response == None:
        response = requests.get(base, params_diction)
        cache.set(UID, response, 1)

    print(response)

# nearby_places_result = get_nearby_places_for_site("moutains")
# print(nearby_places_result)



## Must plot all of the NationalSites listed for the state on nps.gov
## Note that some NationalSites might actually be located outside the state.
## If any NationalSites are not found by the Google Places API they should
##  be ignored.
## param: the 2-letter state abbreviation
## returns: nothing
## side effects: launches a plotly page in the web browser
def plot_sites_for_state(state_abbr):
    pass

## Must plot up to 20 of the NearbyPlaces found using the Google Places API
## param: the NationalSite around which to search
## returns: nothing
## side effects: launches a plotly page in the web browser
def plot_nearby_for_site(site_object):
    pass
