import urbandictionary as ud
import re
import pytrends
from pytrends.request import TrendReq
import wikipedia
import requests
from bs4 import BeautifulSoup
import random
import PyDictionary
from PyDictionary import PyDictionary
#import spacy
import pandas as pd
import re
# adding import alias recommended
bad_patterns = [r'sex*', r'porn*',r'fuck*',r'-ass*','ass','shit',r'damn*',r'ass|asse*',r'cock*',r'whor*',r'nigg*',r'slut*','blowjob',r'fagg*',r'boob|boob*', r'bitch*', r'bastard*',' ho |hoe',r'breast*|jugs', r'cunt*', r'puss*', r'dick*', 'naked', r'nud*', r'masterb*',r'mastu',r'nipple*',r'penis|penal|peni*','god','jesus','christ','bible','church','religion','pray','prayer','faith','lord','allah','muslim','islam','allah','ejaculate','jew*','islamic','atheist',r'rapist*|rape*',r'pedo*','atheism','atheists','atheist','atheists','christian','christianity','christians','christian','christians','gay',r'tit*|titt*','god','jesus','christ','bible','church','religion','pray','prayer','faith','lord','allah','muslim','islam','allah','islamic','atheist','atheism','atheists','atheist','atheists','christian','christianity','christians','christian','christians','yahwey','yeshua',r'israel*',r'sex*', r'porn*',r'fuck*',r'-ass*','ass','shit',r'damn*',r'ass|asse*',r'cock*',r'whor*',r'nigg*',r'slut*','blowjob',r'fagg*',r'boob|boob*', r'breast*|jugs', r'cunt*', r'puss*', r'dick*', 'naked', r'nud*', r'nipple*',r'penis|penal|peni*','god','jesus','christ','bible','church','religion','pray','prayer','faith','lord','allah','muslim','islam','allah','islamic','atheist','atheism','atheists','atheist','atheists','christian','christianity','christians','christian','christians','gay',r'tit*|titt*', 'fellatio', 'fuck', 'nigger','lynch',r'erotic*']

# to make the game more fun we can replace words with less inflamatory ones.


def check_for_badwords(definition, bad_patterns):
    definition = definition.lower()
    # if any of the buzzwords are found return true else false
    if any(re.search(r'\b' + word + r'\b', definition) for word in bad_patterns):
        return True
    else:
        return False

def check_for_good_patterns(definition, title):
    # check both title and definition for good patterns
    good_patterns = [r'\b\w+phobia\.?\b', r'\bslang\b', r'\bacronymn\b', r'\bmeme\b']


    if any(re.match(r'\b' + word + r'\b', definition) for word in good_patterns):
        print(f'Found a good pattern in the definition: {definition}')
        return True
    elif any(re.match(r'\b' + word + r'\b', title) for word in good_patterns):
        print(f'Found a good pattern in the title: {title}')
        return True
    else:
        return False

def remove_undesireable_sentences(definition, title, bad_patterns):
    # convert the definition and title to lowercase
    definition = definition.lower()
    title = title.lower()

    # split the definition into sentences
    sentences = definition.split('.')

    # split the title into words
    title_words = title.split()

    # initialize a list to store the acceptable sentences
    acceptable_sentences = []

    # iterate over the sentences in the definition
    for sentence in sentences:
        # split the sentence into words
        sentence_words = sentence.split()

        # check if any of the words in the sentence are also in the title
        if not any(word in title_words for word in sentence_words):
            # if not, add the sentence to the list of acceptable sentences
            acceptable_sentences.append(sentence)

    # remove sentences that are not in English
    definition = re.sub(r'[^\x00-\x7f]',r'', '.'.join(acceptable_sentences))
    # remove sentences that contain a regex match to any word in the buzzwords list
    definition = re.sub(r'|'.join(map(re.escape, bad_patterns)), '', definition)
    return definition


def unpack_definitions(definition):
    # remove the brackets and clean up the definitions
    # with regex
    definition = definition.replace("[","")
    definition = definition.replace("]","")
    definition = definition.replace("'","")
    definition = definition.replace('"',"")
    definition = definition.replace("(","")
    definition = definition.replace(")","")

    # remove double spaces
    definition = definition.replace('  ',' ')

    return definition

import wikipedia

def get_page_length(phrase):
  # search for pages on Wikipedia that match the given phrase
    try:
        pages = wikipedia.search(phrase)

        # retrieve the first page from the search results
        page = wikipedia.page(pages[0])
        print(f'Found the page for {page.title}', end='')
        if phrase.lower() != page.title.lower():
            print(' ... nevermind... not the right page.')
            return 0
        # return the length of the page
        return len(page.content)
    except Exception as e:
            return 0


def main():

    # example: usage example,
    # upvotes: number of upvotes on Urban Dictionary,
    # downvotes: number of downvotes on Urban Dictionary
    import time
    wikitest = False # set to true to test the wikipedia page length
    # include a phrase if it has a combined total of at least 100 upvotes and downvotes on Urban Dictionary
    rand_dict = {}
    total_votes_thresh = 200 # min number of upvotes + downvotes
    upvotes_thresh = 100 # min number of upvotes
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
            # add the usage example to the definition
            definition += "\nUsage Example: " + usage_example
            upvotes = element.upvotes
            downvotes = element.downvotes
            # define a list of boolean values
            values = [upvotes + downvotes >= total_votes_thresh,
                    upvotes >= upvotes_thresh and downvotes <= downvotes_thresh,
                    check_for_good_patterns(definition, phrase)]


            # check if any element in the list is True
            if any(values) and not check_for_badwords(definition, bad_patterns) \
            and not check_for_badwords(phrase, bad_patterns): # check if the phrase or definition contains any buzzwords
                # include the element in the dictionary if it has a combined total of at least 100 upvotes and downvotes on Urban Dictionary
                definition = remove_undesireable_sentences(
                    definition, phrase, bad_patterns) # remove sentences that contain buzzwords, are not in English, etc.
                definition = unpack_definitions(definition) # remove brackets and clean up the definitions with regex
                if wikitest:
                    print('Testing phrase:', phrase, ' for popularity on Wikipedia...')
                    page_length = get_page_length(phrase) # get the length of the Wikipedia page for the phrase
                    print('Page length:', page_length)
                    if page_length < 1000: # if the page is too short, skip it
                        continue

            print(f'Added {phrase}: {definition[0:10]}...')
            rand_dict[phrase] = definition

    # save the cards to a csv file
    df = pd.DataFrame.from_dict(rand_dict, orient='index')
    df.to_csv('cards.csv', header=False)

    # save the cards to a json file
    import json
    with open('cards.json', 'w') as f:
        json.dump(rand_dict, f)

    # Hippopotomonstrosesquippedaliophobia - fear of long words