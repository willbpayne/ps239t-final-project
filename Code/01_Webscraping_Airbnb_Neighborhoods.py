
# coding: utf-8

# # Scraping Text from Airbnb Neighborhood Pages

# here's where we get all the libraries we need
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
import sys

# here's where we define a function to make a dictionary of city names and URLs

def get_cities(url):
    src = requests.get(url).text
    soup = BeautifulSoup(src) # use BeautifulSoup to get all the HTML
    cities = soup.select('a') # we only want links
    listofcities = [] # empty list
    for item in cities:
        stritem = str(item) # convert to string
        shortitem = stritem[9:-4] # this cuts off the "<a href="" and "</a>" from the ends
        shortitem = shortitem.split("/") # this splits by "/" and makes "shortitem" a list
        if len(shortitem) == 3: # only get the ones that had two "/"s: cities, not neighborhoods
            listitem = shortitem[1] + "/" + shortitem[2] #
            if listitem.startswith("locations/"): # this is where we only get city links
                listofcities.append(listitem) # and add them to our list of cities
    citylist = list(set(listofcities)) # uniquify the list
    citydic = {} # create empty dictionary
    for item in citylist:
        newlist = item.split(">") # split between the URL fragment and name
        name = newlist[1] # second item in this new list is the name
        URL = "https://www.airbnb.com/" + newlist[0][:-1] + "/neighborhoods" # build full URL
        citydic[name] = URL # assign URL as value for the city name key
    return citydic

# here's where we use the function to get the city list
airbnbcitydic = get_cities("https://www.airbnb.com/locations")
print airbnbcitydic

# here's where we define the get_neighborhoods function to scrape all the neighborhood names:

def get_neighborhoods(url):
    src = requests.get(url).text
    soup = BeautifulSoup(src)
    neighborhoods = soup.select('div.span3') # this pulls all the neighborhood list columns by CSS selector
    listofneighborhoods = [] # creates empty list
    for column in neighborhoods: # loops through columns
        hoodlist = column.select('li') # selects neighborhood names/links
        for hood in hoodlist: # loops through neighborhoods
            hood = str(hood) # stringify
            hood = hood[13:-9] # get rid of leading and trailing characters
            if hood.startswith("/locations/"): # only get actual neighborhood links
                listofneighborhoods.append(hood)
        neighborhooddic = {} # create empty dictionary
        for item in listofneighborhoods: # loop through scraped list of neighborhoods
            newlist = item.split(">") # split between URL fragment and name
            name = newlist[1]
            URL = "https://www.airbnb.com" + newlist[0][:-1] # convert to full URL
            neighborhooddic[name] = URL
    return neighborhooddic

get_neighborhoods('https://www.airbnb.com/locations/san-francisco/neighborhoods')

# need this function to clean up strings from Unicode issues below
# there are still outstanding issues, especially for foreign countries,
# but this works for all of the American cities I'm conducting analysis on
# GitHub people: if there's a non-bootleg way to solve this problem, I'm all ears!

def clean_strings(string): 
    a = string.replace("\xe2\x80\x99","'")
    b = a.replace("\xe2\x80\x94"," - ")
    c = b.replace("&amp;","&")
    d = c.replace("\xc2\xa0"," ")
    e = d.replace("\xe2\x80\x93"," - ")
    f = e.replace("\xc3\xb1","n")
    g = f.replace("\xe2\x80\x9c","'")
    h = g.replace("\xe2\x80\x9d","'")
    i = h.replace("\xc3\xa9","e")
    j = i.replace("\xe2\x80\x82","'")
    k = j.replace("\n"," ")
    return k

# Ok now we have a list of neighborhoods; how do we extract the information we want and write it to a CSV?

def get_descriptions(url):
    src = requests.get(url).text
    
    descriptions = {} # create empty dictionary, this will end up being the output CSV
    soup = BeautifulSoup(src)
        
    descriptions["Name"] = soup.select('h1.circularbold')[0].text.encode("ascii", "ignore")
    # Get the neighborhood name from the CSS selector and assign it as value for "Name" key
    
    intro = str(soup.select("div.description"))[48:-20] # find the text of the introductory paragraph
    newintro = clean_strings(intro) # run clean-up function on the text
    descriptions["Intro"] = newintro # assign to the dictionary as value for "Intro" key
    
    lede = soup.select("p.lede")[0].text.encode("ascii", "ignore") # get text from the lede sentence
    strlede = str(lede) # make sure it's a string
    cleanerlede = clean_strings(strlede) # clean it up
    descriptions["Lede"] = cleanerlede # assign to the dictionary
    
    official_tags = soup.select("span.name") # get list of official tags
    official_tag_list = [] # create empty list
    for tag in official_tags: # loop through scraped list
        justtag = (str(tag)[19:-7]) # shorten and stringify the tag
        cleantag = clean_strings(justtag) # clean it up
        official_tag_list.append(cleantag) # add it to the list
    descriptions["Official_Tags"] = official_tag_list # assign to the dictionary
    
    community_tags = soup.select("div.neighborhood-tag") # get list of community tags
    community_tag_list = [] # create empty list
    for tag in community_tags: # loop through scraped list
        justtag = (str(tag)[30:]).split("\n")[0] # shorten and stringify the tag
        cleantag = clean_strings(justtag) # clean it up
        community_tag_list.append(cleantag) # add it to the list
    descriptions["Community_Tags"] = community_tag_list # assign to the dictionary
    
    photo_captions = soup.select("div.primary")[1:] # get list of photo captions
    photo_caption_list = [] # create empty list
    for caption in photo_captions: # loop through scraped list
        justcaption = str(caption)[25:-11] # shorten and stringify the caption
        cleancaption = clean_strings(justcaption) # clean it up
        photo_caption_list.append(cleancaption) # add it to the list
    descriptions["Photo_Captions"] = photo_caption_list # assign to the dictionary
    
    photo_headers = soup.select("h2")[1:-8] # get list of photo headers
    photo_header_list = [] # create empty list
    for header in photo_headers: # loop through scraped list
        justheader = str(header)[4:-5] # shorten and stringify the header
        photo_header_list.append(justheader) # add it to the list
    descriptions["Photo_Headers"] = photo_header_list # assign to the dictionary
    
    block_quotes = soup.select("blockquote") # get list of block quotes
    block_quote_list = [] # create empty list
    for quote in block_quotes: # loop through scraped list
        justquote = str(quote)[12:-14] # shorten and stringify the quotes
        if "photograph" not in justquote: # gets rid of the repetitive block quotes describing photographers
            cleanquote = clean_strings(justquote) # clean it up
            block_quote_list.append(cleanquote) # add it to the list
    for quote in block_quote_list: # loop through the new list
        if "client" in quote: # hack for one photographer description that said "client" instead of above.
            block_quote_list.remove(quote) # get rid of those descriptions
    descriptions["Block_Quotes"] = block_quote_list # assign to the dictionary

    import csv
    filename = url[33:] + '_' + 'descriptions.csv' # pull the url of the neighborhood page to use in the name
    cleanfilename = filename.replace("/","_") # replace "/" with "_" to be more filename-friendly
    writer = csv.writer(open(cleanfilename, 'wb')) # write the csv!
    print "I'm creating a CSV file..." # print statement to let you see progress in real time
    for key, value in descriptions.items():
        writer.writerow([key, value])
    print "CSV file created!"

    return descriptions

get_descriptions('https://www.airbnb.com/locations/berlin/prenzlauer-berg')

#missiondescriptions = get_descriptions('https://www.airbnb.com/locations/san-francisco/mission-district')
#print missiondescriptions


# this code gets data for all american cities, except Lake Tahoe, the only non-urban area to get a neighborhood guide.
americancities = ["https://www.airbnb.com/locations/miami/neighborhoods", 
                  "https://www.airbnb.com/locations/boston/neighborhoods", 
                  "https://www.airbnb.com/locations/new-york/neighborhoods", 
                  "https://www.airbnb.com/locations/los-angeles/neighborhoods", 
                  "https://www.airbnb.com/locations/washington-dc/neighborhoods", 
                  "https://www.airbnb.com/locations/san-francisco/neighborhoods", 
                  "https://www.airbnb.com/locations/austin/neighborhoods"]
for city in americancities:
    cityneighborhooddic = get_neighborhoods(city) 
    for hood in cityneighborhooddic:
        try:
            get_descriptions(cityneighborhooddic[hood])
        except IndexError: # catch any index errors and keep going
            pass
        print "I made a CSV for " + hood + "!"

#this code gets them all! NOTE: this takes a while to run, feel free to interrupt the kernel if necessary.
for item in airbnbcitydic:
    cityneighborhooddic = get_neighborhoods(airbnbcitydic[item]) 
    for item in cityneighborhooddic:
        try:
            get_descriptions(cityneighborhooddic[item])
        except IndexError: # catch any index errors and keep going
            pass
        print "I made a CSV for " + item + "!"

