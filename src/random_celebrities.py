# on this webpage there are random celebrities' names and images
# in the div with class "Rand-stage" there are a number of <li> elements that contain the name and image of a celebrity
# the name is in a <span> element with class "rand_medium"
# from the <li> element we can get the image url by getting the src attribute of the <img> element
# we can get the name by getting the text of the <span> element
# we can get the url of the image by getting the src attribute of the <img> element

# let's put this into a function that takes a number of celebrities to get and returns a dataframe with the name and image url of each celebrity, to create a deck of cards


import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from ratelimit import limits, sleep_and_retry
import re

@sleep_and_retry
def parse_page():
    # Make a GET request to the website

    # Make a GET request to the website
    url = "https://www.randomlists.com/random-people"
    html = requests.get(url).text

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find all the elements that match the CSS selector
    name_elements = soup.select("body > div > div.layout-main > main > article > div.Rand-stage")  # span.rand_medium

    # Extract the names from the elements
    names = [element.text for element in name_elements]


    print(names)



# Test the function
parse_page()
