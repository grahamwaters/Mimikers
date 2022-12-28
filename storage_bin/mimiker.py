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
def check_for_good_patterns(definition, title, good_patterns):
    # check both title and definition for good patterns
    good_patterns = [r'phobia','slang','acronymn','meme']
    if any(re.match(r'\b' + word + r'\b', definition) for word in good_patterns):
        return True
    elif any(re.match(r'\b' + word + r'\b', title) for word in good_patterns):
        return True
    else:
        return False


def unpack_definitions(definition):
    # remove the brackets and clean up the definitions
    # with regex
    definition = definition.replace("[","")
    definition = definition.replace("]","")
    definition = definition.replace("'","")
    definition = definition.replace('"',"")
    definition = definition.replace("(","")
    definition = definition.replace(")","")
    print(definition)
    return definition



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
    bad_patterns = [r'sex*', r'porn*',r'fuck*',r'-ass*','ass','shit',r'damn*',r'ass|asse*',r'cock*',r'whor*',r'nigg*',r'slut*','blowjob',r'fagg*',r'boob|boob*', r'breast*|jugs', r'cunt*', r'puss*', r'dick*', 'naked', r'nud*', r'nipple*',r'penis|penal|peni*','god','jesus','christ','bible','church','religion','pray','prayer','faith','lord','allah','muslim','islam','allah','islamic','atheist','atheism','atheists','atheist','atheists','christian','christianity','christians','christian','christians','gay',r'tit*|titt*', 'fellatio', 'fuck', 'nigger','lynch']
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
    buzzwords = [r'sex*', r'porn*',r'fuck*',r'-ass*','ass','shit',r'damn*',r'ass|asse*',r'cock*',r'whor*',r'nigg*',r'slut*','blowjob',r'fagg*',r'boob|boob*', r'breast*|jugs', r'cunt*', r'puss*', r'dick*', 'naked', r'nud*', r'nipple*',r'penis|penal|peni*','god','jesus','christ','bible','church','religion','pray','prayer','faith','lord','allah','muslim','islam','allah','islamic','atheist','atheism','atheists','atheist','atheists','christian','christianity','christians','christian','christians','gay',r'tit*|titt*', 'fellatio', 'fuck', 'nigger','lynch']
    # remove sentences that contain a regex match to any word in the buzzwords list
    definition = re.sub(r'|'.join(map(re.escape, buzzwords)), '', definition)
    return definition #

good_patterns = [r'phobia','slang','acronymn','meme']






def main():

    # example: usage example,
    # upvotes: number of upvotes on Urban Dictionary,
    # downvotes: number of downvotes on Urban Dictionary
    import time
    wikitest = False # set to true to test the wikipedia page length
    # include a phrase if it has a combined total of at least 100 upvotes and downvotes on Urban Dictionary
    rand_dict = {}
    total_votes_thresh = 20
    upvotes_thresh = 50 # min number of upvotes
    downvotes_thresh = 10 # max number of downvotes
    desired_number_of_cards = 15
    rands = [] # the randoms

    while len(rand_dict) < desired_number_of_cards:
    time.sleep(1)
    rand = ud.random() # returns a list of 5 random phrases and definitions from Urban Dictionary
    # append these to a master list
    rands.extend(rand) # rands is a list of all the random phrases and definitions from Urban Dictionary

    # iterate over the elements in the rand object
    for element in rand:
        # extract the relevant data from the element
        phrase = element.word
        definition = element.definition
        usage_example = element.example
        upvotes = element.upvotes
        downvotes = element.downvotes
        # define a list of boolean values
        values = [upvotes + downvotes >= total_votes_thresh,
                upvotes >= upvotes_thresh and downvotes <= downvotes_thresh]

        # check if any element in the list is True
        if any(values) and not check_for_badwords(definition, bad_patterns) \
        and not check_for_badwords(phrase, bad_patterns): # check if the phrase or definition contains any buzzwords
        # include the element in the dictionary if it has a combined total of at least 100 upvotes and downvotes on Urban Dictionary
        definition = remove_undesireable_sentences(definition, bad_patterns) # remove sentences that contain buzzwords, are not in English, etc.
        definition = unpack_definitions(definition) # remove brackets and clean up the definitions with regex
        if wikitest:
            print('Testing phrase:', phrase, ' for popularity on Wikipedia...')
            page_length = get_page_length(phrase) # get the length of the Wikipedia page for the phrase
            print('Page length:', page_length)
            if page_length < 1000: # if the page is too short, skip it
            continue

        print(f'Added {phrase}: {definition[0:100]}...')
        rand_dict[phrase] = definition

    # show the dictionary of random phrases and definitions as a pandas dataframe
    pd.DataFrame(rand_dict, index=[0]).T
