# goal of this script: build a game based on Monikers. This game generates cards from wikipedia entries, and Urban Dictionary definitions.
import spacy # for NLP
import wikipedia # for wikipedia entries
import random # for randomization
import pytrends # for google trends

# Function One: Card Creator for a random Person or Thing from Wikipedia
def create_ppn_card():
    # create a person/place/thing card
    # get a random wikipedia entry
    random_wiki_entry = wikipedia.random(pages=1)
    # get the summary of the entry
    random_wiki_entry_summary = wikipedia.summary(random_wiki_entry)
    # get the url of the entry
    random_wiki_entry_url = wikipedia.page(random_wiki_entry).url
    # get the title of the entry
    random_wiki_entry_title = wikipedia.page(random_wiki_entry).title
    # get the image of the entry
    random_wiki_entry_image = wikipedia.page(random_wiki_entry).images[0]
    # get the categories of the entry
    random_wiki_entry_categories = wikipedia.page(random_wiki_entry).categories
    # get the links of the entry
    random_wiki_entry_links = wikipedia.page(random_wiki_entry).links
    # get the references of the entry
    random_wiki_entry_references = wikipedia.page(random_wiki_entry).references
    # get the html of the entry
    random_wiki_entry_html = wikipedia.page(random_wiki_entry).html()

    # create a dictionary of the entry
    random_wiki_entry_dict = {
        "summary": random_wiki_entry_summary,
        "url": random_wiki_entry_url,
        "title": random_wiki_entry_title,
        "image": random_wiki_entry_image,
        "categories": random_wiki_entry_categories,
        "links": random_wiki_entry_links,
        "references": random_wiki_entry_references,
        "html": random_wiki_entry_html
    }

    # return the dictionary
    return random_wiki_entry_dict

# Helper Function A: Does this wikipedia page refer to a person?
def is_person(wiki_entry_dict):
    # check if the entry is a person. If it is, return True. If not, return False.
    # get the categories of the entry
    random_wiki_entry_categories = wiki_entry_dict["categories"]
    # check if the entry is a person
    if "Category:Living people" in random_wiki_entry_categories:
        return True
    else:
        return False



# Function Two: Card Creator for a random Phrase from Urban Dictionary
