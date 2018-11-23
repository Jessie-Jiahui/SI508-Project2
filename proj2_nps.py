## proj_nps.py
## Skeleton for Project 2, Fall 2018
## ~~~ modify this file, but don't rename it ~~~
from secrets import google_places_key

from bs4 import BeautifulSoup
from alternate_advanced_caching import Cache
import requests
from datetime import datetime

import json

import plotly
plotly.tools.set_credentials_file(username='JHZHOU', api_key='9odHR7ne1q0Vq52gOPIe')
import plotly.plotly as py
import plotly.graph_objs as go

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NationalSite():
    def __init__(self, site_type, name, desc, address_street, address_city, address_state, address_zip, url=None):
        self.type = site_type
        self.name = name
        self.description = desc
        self.url = url
        self.address_street = address_street
        self.address_city = address_city
        self.address_state = address_state
        self.address_zip = address_zip

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
    def __init__(self, name, lat, lng):
        self.name = name
        self.lat = lat
        self.lng = lng

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
    cache_file = "part1.json"
    url_to_scrape = "https://www.nps.gov/state/{}/index.htm".format(state_abbr)
    cache = Cache(cache_file)

    while cache.get(url_to_scrape) is None:
        html_text = requests.get(url_to_scrape).text
        cache.set(url_to_scrape, html_text, 10)


    soup = BeautifulSoup(cache.get(url_to_scrape), features='html.parser')
    parks = soup.find( id="list_parks").find_all(class_='clearfix')
    

    ### Information you should get for each National Site will include the site name, site type, and the physical (or mailing) address. 
    national_park_list = []
    for park in parks:
        site_name = park.find('h3').text
        site_type = park.find('h2').text
        site_desc = park.find('p').text

        address_url = park.find_all('a')[2].get('href')
        
        cache_file = "part1_address.json"
        url_to_scrape = address_url
        cache = Cache(cache_file)

        while cache.get(url_to_scrape) is None:
            html_text = requests.get(url_to_scrape).text
            cache.set(url_to_scrape, html_text, 10)

        soup_add = BeautifulSoup(cache.get(url_to_scrape), features='html.parser')

        address_street = soup_add.find(itemprop='streetAddress').text
        address_city = soup_add.find(itemprop='addressLocality').text
        address_state = soup_add.find(itemprop='addressRegion').text
        address_zip = soup_add.find(itemprop='postalCode').text

        national_park_list.append(NationalSite(site_type, site_name, site_desc, address_street, address_city, address_state, address_zip))
    return national_park_list

nps_list = get_sites_for_state("MI")
# for i in nps_list:
#     print(i.__str__())


## Must return the list of NearbyPlaces for the specifite NationalSite
## param: a NationalSite object
## returns: a list of NearbyPlaces within 10km of the given site
##          if the site is not found by a Google Places search, this should
##          return an empty list
if google_places_key == "" or not google_places_key:
    print("Your google api key is missing from the file. Enter your google api key where directed and save the program!")
    exit()

# text search function to get the longitude and latitude values needed in nearby search
def get_location_for_site(national_site):
    cache_file = "part2_textsearch.json"
    cache = Cache(cache_file)

    base = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    params_diction = {}
    params_diction["query"] = "{},{}".format(national_site.name, national_site.type)
    params_diction["key"] = google_places_key

    identifier = base + params_diction["query"] + params_diction["key"]

    response = cache.get(identifier)
    while response is None:
        response = json.loads(requests.get(base, params_diction).text)
        cache.set(identifier, response, 10)

    try:
        lat = str((response["results"][0]["geometry"]["location"]["lat"]))
        lng = str((response["results"][0]["geometry"]["location"]["lng"]))
        return lat + ',' + lng
    except:
        return None


def get_nearby_places_for_site(national_site):
    cache_file = "part2_nearbysearch.json"
    cache = Cache(cache_file)

    base = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    params_diction = {}
    params_diction["key"] = google_places_key
    params_diction["location"] = get_location_for_site(national_site)
    params_diction["radius"] = 10000

    identifier = base + params_diction["key"] + params_diction["location"] + str(params_diction["radius"])

    response = cache.get(identifier)
    while response is None:
        response = json.loads(requests.get(base, params_diction).text)
        cache.set(identifier, response, 10)

    nearby_result_list = response["results"]

    nearby_list = []
=======

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

        national_park_list.append(NationalSite(site_type, site_name, site_desc, address_street, address_city, address_state, address_zip))
    return national_park_list

nps_list = get_sites_for_state("MI")
for i in nps_list:
    print(i.__str__())

    for nearby in nearby_result_list:
        name = nearby["name"]
        lat = nearby["geometry"]["location"]["lat"]
        lng = nearby["geometry"]["location"]["lng"]
        nearby_list.append(NearbyPlace(name, lat, lng))

    return nearby_list
    

national_site = nps_list[0]
# get_location_for_site(national_site)
# get_nearby_places_for_site(national_site)


## Must plot all of the NationalSites listed for the state on nps.gov
## Note that some NationalSites might actually be located outside the state.
## If any NationalSites are not found by the Google Places API they should
##  be ignored.
## param: the 2-letter state abbreviation
## returns: nothing
## side effects: launches a plotly page in the web browser

def plot_sites_for_state(state_abbr):
    national_sites = get_sites_for_state(state_abbr)

    lat_vals = []
    lon_vals = []
    text_vals = []

    for national_site in national_sites:
        location = get_location_for_site(national_site)

        if location != None:
            lat_vals.append(location.split(',')[0])
            lon_vals.append(location.split(',')[1])
            text_vals.append(national_site.name)

    min_lat = 10000
    max_lat = -10000
    min_lon = 10000
    max_lon = -10000

    for str_v in lat_vals:
        v = float(str_v)
        if v < min_lat:
            min_lat = v
        if v > max_lat:
            max_lat = v
    for str_v in lon_vals:
        v = float(str_v)
        if v < min_lon:
            min_lon = v
        if v > max_lon:
            max_lon = v
       
    lat_axis = [min_lat - 1, max_lat + 1]
    lon_axis = [min_lon - 1, max_lon + 1]

    center_lat = (max_lat+min_lat) / 2
    center_lon = (max_lon+min_lon) / 2

    data = [ dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = lon_vals,
            lat = lat_vals,
            text = text_vals,
            mode = 'markers',
            marker = dict(
                size = 8,
                symbol = 'star',
            ))]

    layout = dict(
            title = 'National Sites in {}'.format(state_abbr.upper()),
            colorbar = True,
            geo = dict(
                scope='usa',
                projection=dict( type='albers usa' ),
                showland = True,
                landcolor = "rgb(250, 250, 250)",
                subunitcolor = "rgb(100, 217, 217)",
                countrycolor = "rgb(217, 100, 217)", 
                lataxis = {'range': lat_axis},
                lonaxis = {'range': lon_axis},
                center= {'lat': center_lat, 'lon': center_lon },
                countrywidth = 3,
                subunitwidth = 3
            ),
        )

    fig = dict( data=data, layout=layout )
    py.iplot( fig, validate=False, filename='national - sites' )


# plot_sites_for_state("MI")


## Must plot up to 20 of the NearbyPlaces found using the Google Places API
## param: the NationalSite around which to search
## returns: nothing
## side effects: launches a plotly page in the web browser
def plot_nearby_for_site(site_object):
    location = get_location_for_site(site_object)

    if location != None:
        site_object_lat = [location.split(',')[0]]
        site_object_lon = [location.split(',')[1]]
        site_object_name = [site_object.name]

    nearby_sites = get_nearby_places_for_site(site_object)

    lat_vals = []
    lon_vals = []
    text_vals = []

    for nearby_site in nearby_sites:
            lat_vals.append(nearby_site.lat)
            lon_vals.append(nearby_site.lng)
            text_vals.append(nearby_site.name)

    min_lat = 10000
    max_lat = -10000
    min_lon = 10000
    max_lon = -10000

    for str_v in lat_vals:
        v = float(str_v)
        if v < min_lat:
            min_lat = v
        if v > max_lat:
            max_lat = v
    for str_v in lon_vals:
        v = float(str_v)
        if v < min_lon:
            min_lon = v
        if v > max_lon:
            max_lon = v
       
    lat_axis = [min_lat - 1, max_lat + 1]
    lon_axis = [min_lon - 1, max_lon + 1]

    center_lat = (max_lat+min_lat) / 2
    center_lon = (max_lon+min_lon) / 2

    trace1 = dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = site_object_lon,
            lat = site_object_lat,
            text = site_object_name,
            mode = 'markers',
            marker = dict(
                size = 15,
                symbol = 'star',
                color = 'red'
            ))

    trace2 = dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = lon_vals,
            lat = lat_vals,
            text = text_vals,
            mode = 'markers',
            marker = dict(
                size = 8,
                symbol = 'star',
                color = 'blue'
            ))

    data = [trace1, trace2]

    layout = dict(
            title = 'Places near {}'.format(site_object.name.upper()),
            colorbar = True,
            geo = dict(
                scope='usa',
                projection=dict( type='albers usa' ),
                showland = True,
                landcolor = "rgb(250, 250, 250)",
                subunitcolor = "rgb(100, 217, 217)",
                countrycolor = "rgb(217, 100, 217)", 
                lataxis = {'range': lat_axis},
                lonaxis = {'range': lon_axis},
                center= {'lat': center_lat, 'lon': center_lon },
                countrywidth = 3,
                subunitwidth = 3
            ),
        )

    fig = dict( data=data, layout=layout )
    py.iplot( fig, validate=False, filename='nearby - sites' )

# plot_nearby_for_site(national_site)


user_input = input("Here are the commands you can order:\nlist <stateabbr> — e.g. list MI\nnearby <result_number> — e.g. nearby 2\nmap\nexit\nhelp\n\nPlease input your command:")

if user_input[0:4] == "list":
    state = user_input.split(" ")[1]
    national_parks = get_sites_for_state(state)

    for park in national_parks:
        print("{}) {}".format(national_parks.index(park)+1, park.name))

    user_input1 = input("")
    if user_input1 == "exit":
        exit()

    elif user_input1 == "map":
        plot_sites_for_state(state)

        if user_input1 == "exit":
            exit()
    elif user_input1[0:6] == "nearby":
        index = int(user_input1.split(" ")[1])
        national_park = national_parks[index]
        nearby_sites_list = get_nearby_places_for_site(national_park)

        for nearby_site in nearby_sites_list:
            print("{}) {}".format(nearby_sites_list.index(nearby_site)+1, nearby_site))

        user_input2 = input("")
        if user_input2 == "map":
            plot_nearby_for_site(national_parks[index])
        if user_input1 == "exit":
            exit()



