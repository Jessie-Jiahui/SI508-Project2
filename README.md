# Jiahui Zhou
# SI508-Project2

#### Project Overview
It is a program to scrape and search information about National Sites (Parks, Heritage Sites, Trails, and other entities) from the website nps.gov. It also has the ability to look up nearby places using the Google Places API and to display National Sites and Nearby Places on a map using plotly.

#### RUN proj2_nps.py
-- It shows commands that a user can input
-- Show information of all national parks of the state input, e.g. 'list mi'
-- Show information of all nearby places(up to 20 reuslts) of the national park index input, e.g. 'nearby 1'
-- Quits on input of `exit`
-- Term explanation on input of `help`
-- Display on plot.ly web map on input of `map`

#### Please install the following libraries:
-- secrets
-- bs4
-- alternate_advanced_caching
-- requests
-- datetime
-- json
-- plotly
-- plotly.plotly
-- plotly.graph_objs

#### File overview:
-- proj2_nps.py: define NationalSite class and NearbyPlace class, define the functionality of obtaining a list of national sites in a state (get_sites_for_state) and get the nearby places of a site (get_sites_for_state), define the function to display interface and integrate all functionalities
-- proj2_nps_test.py: given test file, no modifications
-- secrets.py: store my Google API key
-- advanced_expiry_caching.py: copy from code provided on the class. Define a chache class to store the respond to a cache file.
-- part1.json: cache file
-- part1_address.json: cache file
-- part2_textsearch.json: cache file
-- part2_nearbysearch.json: cache file






