# ps239t-final-project: Branding Urban Neighborhoods on Airbnb

## Short Description

This is my final project for PS239T, in which I use web scraping and text analysis tools on Airbnb neighborhood descriptions. I’m an urban geographer studying the way that location-based services (LBS) affect how people interact with cities. For this project, I wanted to study the difference in the way LBS developers and users describe different urban neighborhoods, through discriminating word analysis and visualizing wordclouds for different cities.

## Dependencies

1. R, version 3.2.2 (2015-08-14)
2. Python 2.7.10, Anaconda distribution (2.3.0)

## Files

#### Data

1. Discriminating_words_cities: Set of CSV files resulting from webscraping of Airbnb neighborhood description pages in New York and San Francisco, with the following variable names (all strings or lists of strings):
    - *Name*: Neighborhood name
    - *Lede*: One-sentence summary of the neighborhood page.
    - *Official_Tags*: Tags applied by Airbnb staff to the neighborhood (from a set of 18 total, with every city including tags for "Peace & Quiet," "Nightlife," "Shopping," "Dining," some variant on "Loved by Locals," and "Touristy")
    - *Intro*: Full paragraph description of the neighborhood.
    - *Community_Tags*: User-generated tags for the neighborhood (e.g. "Murals," "Hipsters," "Bicyclists," "Trendy," "Burritos," "Artists," "Nightlife," "Music," "Dive Bars," "Coffee" "Latino" "Community" "Tamale Lady").
    - *Photo_Headers*: Headers for sections of photos (e.g. "The Mission District: It's Complicated").
    - *Photo_Captions*: Captions for individual photos (e.g. the totally ridiculous sentence "The Mission District's streets are more than names and numbers. They often serve as geographic indicators when answering the question, "Will I find amusement or will I feel apprehensive?")
    - *Block_Quotes*: Full text of any block quotes on the page, except the descriptions of the individual contributing photographers (since those are often shared between neighborhood, throwing off text analysis).
2. Wordcloud_cities: Same as above but containing folders representing all eight cities examined in the wordcloud analysis: Austin, Berlin, Boston, DC, LA, Miami, NYC, and SF. Using the Airbnb_Wordcloud.Rmd file below, changing the working directory results in a wordcloud for the given city.
  

#### Code

1. Webscraping_Airbnb_Neighborhoods.py: Collects data from neighborhood description pages on Airbnb using Beautiful Soup and adds them to individual CSV files for each neighborhood. 
2. Airbnb_Discriminating_Words.Rmd: .
2. Airbnb_Wordcloud.Rmd: Creates wordclouds of description text for a given Airbnb city.

#### Results

1. Presentation.key: Keynote presentation summarizing project, methods, and results.
2. Presentation.pdf: PDF version of results presentation.
3. Wordclouds: Folder of eight PNG files showing final wordclouds for neighborhood descriptions in each of the following cities: Austin, Berlin, Boston, DC, LA, Miami, NYC, and SF.

## More Information

Contact info:

Will Payne
PhD student, [Geography, UC Berkeley](http://geography.berkeley.edu/people/graduate-students/willbpayne/)
<willbpayne@berkeley.edu>
[Twitter](https://twitter.com/willbpayne) | [Academia.edu](https://berkeley.academia.edu/WillBPayne)
