# goal of this script: build a game based on Monikers. This game generates cards from wikipedia entries, and Urban Dictionary definitions.
import spacy # for NLP
import wikipedia # for wikipedia entries
import random # for randomization
import pytrends # for google trends


"""
    Example Card:
        Title: Bro Bono
        Description:
            The act of providing free services to friends. Originated from the legal term "pro bono" meaning "for the public good" or "free".
            Friend #1: "Hey man, I need a logo designed for my new company but I dont have a lot of money"
            Friend #2: "no problem man, your my best friend, I'll do it Bro Bono"
        Point Value: 2
"""




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


def check_for_religious_words(definition):
    definition = definition.lower()
    if any(re.search(r'\b' + word + r'\b', definition) for word in ['god','jesus','christ','bible','church','religion','pray','prayer','faith','lord','allah','muslim','islam','allah','islamic','atheist','atheism','atheists','atheist','atheists','christian','christianity','christians','christian','christians']):
        return True
    else:
        return False

import re


def check_for_badwords(definition):
    definition = definition.lower()
    bad_patterns = [r'sex*', r'porn*',r'fuck*',r'-ass*','ass','shit',r'damn*',r'ass|asse*',r'cock*',r'whor*',r'nigg*',r'slut*','blowjob',r'fagg*',r'boob|boob*', r'breast*|jugs', r'cunt*', r'puss*', r'dick*', 'naked', r'nud*', r'nipple*',r'penis|penal|peni*','god','jesus','christ','bible','church','religion','pray','prayer','faith','lord','allah','muslim','islam','allah','islamic','atheist','atheism','atheists','atheist','atheists','christian','christianity','christians','christian','christians','gay',r'tit*|titt*']
    # if any of the buzzwords are found return true else false
    if any(re.search(r'\b' + word + r'\b', definition) for word in bad_patterns):
        return True
    else:
        return False



def remove_undesireable_sentences(definition):
    definition = definition.lower()
    # removes any sentence that contains a regex match to any word in the buzzwords list leaving the other sentences intact.
    # remove sentences that are not in English
    definition = re.sub(r'[^\x00-\x7f]',r'', definition)
    # example: "A woman with huge breasts" would be removed because of the mention of "breast"
    buzzwords = [r'sex*', r'porn*',r'fuck*',r'-ass*','ass','shit',r'damn*',r'ass|asse*',r'cock*',r'whor*',r'nigg*',r'slut*','blowjob',r'fagg*',r'boob|boob*', r'breast*|jugs', r'cunt*', r'puss*', r'dick*', 'naked', r'nud*', r'nipple*',r'penis|penal|peni*','god','jesus','christ','bible','church','religion','pray','prayer','faith','lord','allah','muslim','islam','allah','islamic','atheist','atheism','atheists','atheist','atheists','christian','christianity','christians','christian','christians','gay',r'tit*|titt*']
    # remove sentences that contain a regex match to any word in the buzzwords list
    definition = re.sub(r'|'.join(map(re.escape, buzzwords)), '', definition)
    return definition #