
# coding: utf-8

# # Airbnb Neighborhood Info Scraping

# First, run the code below to import the `requests` and `BeautifulSoup` libraries, as well as some other libraries we will be using.

# In[1]:

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
import sys


# In[84]:

def get_cities(url):
    src = requests.get(url).text
    soup = BeautifulSoup(src)
    cities = soup.select('a')
    listofcities = []
    for item in cities:
        stritem = str(item)
        shortitem = stritem[9:-4]
        if shortitem.startswith("/locations/"):
            listofcities.append(shortitem)
    return listofcities
get_cities("https://www.airbnb.com/locations")


# In[87]:

citylist = get_cities("https://www.airbnb.com/locations")
citylist = list(set(citylist))
citydic = {}
for item in citylist:
    newlist = item.split(">")
    name = newlist[1]
    URL = "https://www.airbnb.com" + newlist[0][:-1]
    citydic[name] = URL
print citydic


# In[88]:

def get_neighborhoods(url):
    src = requests.get(url).text
    soup = BeautifulSoup(src)
    neighborhoods = soup.select('div.span3')
    listofneighborhoods = []
    for column in neighborhoods:
        hoodlist = column.select('li')
        for hood in hoodlist:
            hood = str(hood)
            hood = hood[13:-9]
            listofneighborhoods.append(hood)
    return listofneighborhoods

neighborhoodlist = get_neighborhoods('https://www.airbnb.com/locations/san-francisco/neighborhoods')
print neighborhoodlist


# In[94]:

for item in neighborhoodlist:
    if not item.startswith("/locations/"):
        neighborhoodlist.remove(item)
        print "I removed something"
print neighborhoodlist


# In[95]:

neighborhooddic = {}
for item in neighborhoodlist:
    newlist = item.split(">")
    name = newlist[1]
    URL = "https://www.airbnb.com" + newlist[0][:-1]
    neighborhooddic[name] = URL
print neighborhooddic


# Ok now we have a list of neighborhoods; how do we extract the information we want and write it to a CSV?

# In[286]:

def get_descriptions(url):
    src = requests.get(url).text
    
    descriptions = {}
    soup = BeautifulSoup(src)
        
    descriptions["Name"] = str(soup.select('h1.circularbold'))[26:-6]
    
    print descriptions["Name"]
    
    intro = str(soup.select("div.description"))[48:-20]
    newintro = intro.replace("\xe2\x80\x99","'")
    descriptions["Intro"] = newintro
    
    lede = soup.select("p.lede")[0]
    strlede = str(lede)[16:-4]
    cleanlede = strlede.replace("\xe2\x80\x99","'")
    cleanerlede = cleanlede.replace("\xe2\x80\x94"," - ")
    descriptions["Lede"] = cleanerlede
    
    official_tags = soup.select("span.name")
    official_tag_list = []
    for tag in official_tags:
        justtag = (str(tag)[19:-7])
        cleantag = justtag.replace("&amp;","&")
        official_tag_list.append(cleantag)
    descriptions["Official_Tags"] = official_tag_list
    
    community_tags = soup.select("div.neighborhood-tag")
    community_tag_list = []
    for tag in community_tags:
        justtag = (str(tag)[30:]).split("\n")[0]
        community_tag_list.append(justtag)
    descriptions["Community_Tags"] = community_tag_list
    
    photo_captions = soup.select("div.primary")[1:]
    photo_caption_list = []
    for caption in photo_captions:
        justcaption = str(caption)[25:-11]
        cleancaption = justcaption.replace("\xc2\xa0"," ")
        cleanercaption = cleancaption.replace("\xe2\x80\x93"," - ")
        cleanestcaption = cleanercaption.replace("\\", "")
        photo_caption_list.append(cleanestcaption)
    descriptions["Photo_Captions"] = photo_caption_list
    
    photo_headers = soup.select("h2")[1:-8]
    photo_header_list = []
    for header in photo_headers:
        justheader = str(header)[4:-5]
        photo_header_list.append(justheader)
    descriptions["Photo_Headers"] = photo_header_list
    
    block_quotes = soup.select("blockquote")
    block_quote_list = []
    for quote in block_quotes:
        justquote = str(quote)[12:-14]
        cleanquote = justquote.replace("\xe2\x80\x99","'")
        cleanestquote = cleanquote.replace("&amp;","&")
        block_quote_list.append(cleanestquote)
    descriptions["Block_Quotes"] = block_quote_list

    import csv
    filename = url[33:] + '_' + 'descriptions.csv'
    cleanfilename = filename.replace("/","_")
    writer = csv.writer(open(cleanfilename, 'wb'))
    print "I'm creating a CSV file..."
    for key, value in descriptions.items():
        writer.writerow([key, value])

    print "CSV file created!"

    #return descriptions

get_descriptions('https://www.airbnb.com/locations/san-francisco/mission-district')

#missiondescriptions = get_descriptions('https://www.airbnb.com/locations/san-francisco/mission-district')
#print missiondescriptions


# In[291]:

for item in neighborhooddic:
    try:
        get_descriptions(neighborhooddic[item])
    except IndexError: # catch the error
        pass
    print "I made a CSV for " + item + "!"


# In[ ]:



