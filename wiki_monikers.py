import re
from nltk.corpus import words
from nltk.tokenize import word_tokenize
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer

import wikipedia
import requests
import urllib.parse
from bs4 import BeautifulSoup
from ratelimit import limits, sleep_and_retry
from tqdm import tqdm
import json

URL = "https://randomincategory.toolforge.org/Random_page_in_category?"

hard_mode_categories = [
    "Philosophers_of_ethics_and_morality",
    "United_States_Supreme_Court_cases",
    "Political_party_founders",
    "Classics_educators",
]
obscure_mode_categories = ["Fictional_inventors"]

profanity_pages = [
    "English_profanity"
]  # note: use this to filter out profanity in the definitions (it is evolving so it is not perfect)

events_and_culture = [
    "Whistleblowing",
    "News_leaks",
    "WikiLeaks",
    "Popular_music",
    "Fiction_about_personifications_of_death",
    "Bogeymen",
]

movies = ["Universal_Pictures_films", "Paramount_Pictures_films"]

linguistic_categories = ["English_phrases"]
biblical_categories = ["Biblical_phrases"]
# Literary_characters
# categories = ["paradoxes","Slogans","English-language_books"]
base_categories = [
    "Literary_concepts",
    "Historical_eras",
    "Viral_videos",
    "Internet_memes",
    "Theorems",
    "21st-century_male_actors",
    "21st-century_female_actors",
    "Fables",
    "American_Internet_celebrities",
    "Legends",
    "Mythology",
    "Rules_of_thumb",
    "Adages",
    "Fallacies",
    "Mountains",
    "Lakes",
    "Oceans",
    "Sea_Monsters",
    "fairy_tales",
    "1800s",
    "Tall_tales",
    "Urban_legends",
    "Superstitions",
    "Western_culture",
    "English-language_idioms",
    "Catchphrases",
    "Quotations_from_film",
    "Quotations_from_music",
    "Quotations_from_literature",
    "Quotations_from_television",
    "Quotations_from_video_games",
]

# append this ['Internet_memes_introduced_in_{}'.format(str(year)) for year in range(2000,2023)] to categories
meme_categories = [
    "Internet_memes_introduced_in_{}".format(str(year)) for year in range(2000, 2023)
]
year_categories = [
    "{}s_in_Internet_culture".format(str(year)) for year in range(1970, 2020, 10)
]
# subcats_foryears = ['_in_television']

# Television_characters_introduced_in_1980 through 2023
# //charactersTV = ['Television_characters_introduced_in_{}'.format(str(year)) for year in range(1950,2023)]
# Video Games for years 1950 through 2023
#!VideoGames_Categories = ['{}_video_games'.format(str(year)) for year in range(1970,2010)]

# create these categories: Extraterrestrial_life_in_popular_culture, Fairies and sprites in popular cuture
pop_culture_creatures = [
    "Dinosaurs_in_popular_culture",
    "Extraterrestrial_life_in_popular_culture",
]

categories = base_categories
# * appending to categories
categories.extend(meme_categories)  # add meme categories to categories
# add in events and culture
categories.extend(events_and_culture)  # adds some events and culture to categories
# add pop_culture_creatures
categories.extend(
    pop_culture_creatures
)  # adds some pop culture creatures to categories
# add year categories
categories.extend(year_categories)  # adds some year categories to categories
# add charactersTV
# //categories.extend(charactersTV) # adds some charactersTV to categories
categories.extend(biblical_categories)  # adds some biblical_categories to categories
# add VideoGames_Categories
#!categories.extend(VideoGames_Categories) # adds some VideoGames_Categories to categories
# add linguistic_categories
categories.extend(
    linguistic_categories
)  # adds some linguistic_categories to categories
# add events_and_culture
categories.extend(events_and_culture)  # adds some events_and_culture to categories
categories.extend(movies)  # adds some movies to categories


# * let's get all memes only
# * categories = meme_categories

# * let's get all memes and years only
# //categories = meme_categories
# //categories.extend(year_categories)


# these pages have links to extract
pages = [
    "https://en.wikipedia.org/wiki/List_of_Internet_phenomena",
    "https://en.wikipedia.org/wiki/List_of_largest_cities",
    "https://en.wikipedia.org/wiki/List_of_-gate_scandals_and_controversies",
]

# these are links for current events
pages = [
    "https://en.wikipedia.org/wiki/Portal:Current_events/December_2022",
    "https://en.wikipedia.org/wiki/Wikipedia:Top_25_Report",
    "https://en.wikipedia.org/wiki/List_of_eponymous_laws",
]


original_categories = categories.copy()

import random

# shuffle categories to get a random selection
random.shuffle(categories)
# select 20 random categories
categories = categories[:20]
for cat in enumerate(categories):
    URL += f"&category{cat[0]}={urllib.parse.quote(str(cat[1]).lower())}"

URL += "&server=en.wikipedia.org&cmnamespace=0&cmtype=page&returntype="

#^ Dynamic updates through GroupMe

import wikipedia
# create a GroupMeAPI object
groupme_api = GroupMeAPI(secrets["groupme_token"])


# function to check the groupme thread for new messages (that are not from the bot)
def check_for_new_messages():
    with open("./secrets.json") as json_file:
        secrets = json.load(json_file)
        bot_id = secrets["groupme_botid"]

    global groupme_api
    # access the GroupMe API and get the latest messages in the thread
    latest_messages = groupme_api.get_latest_messages()

    # filter the messages to get only those that are not from the bot
    new_messages = [message for message in latest_messages if message['sender_id'] != bot_id]

    return new_messages


def add_category(message):
    # check if the message is a valid Wikipedia category
    try:
        wikipedia.WikipediaPage(message).category
        is_valid_category = True
    except wikipedia.exceptions.PageError:
        is_valid_category = False

    # if the message is a valid Wikipedia category, add it to the categories text file
    if is_valid_category:
        with open("categories.txt", "a") as categories_file:
            categories_file.write(f"{message}\n")
    # if the message is not a valid Wikipedia category, ignore it
    else:
        pass




def replacer_censor(definition, phrase, replacements_dict):
    # Iterate over the keys in the replacements dictionary
    for pattern in replacements_dict:
        # Use re.sub to replace the occurrences of the pattern with its corresponding value in the phrase and definition strings
        phrase = re.sub(pattern, replacements_dict[pattern], phrase)
        definition = re.sub(pattern, replacements_dict[pattern], definition)
    return phrase, definition


# todo
def summarize_text(text, num_sentences):
    """
    Summarize the given text using the LSA or LexRank summarization algorithms and return the summary as a list of sentences
    """
    # create a PlaintextParser object to parse the text
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    # choose a summarization algorithm
    # algorithm = LsaSummarizer()
    algorithm = LexRankSummarizer()

    # summarize the text and return the summary as a list of sentences
    summary = algorithm(parser.document, num_sentences)

    return summary


# todo
def unpack_definitions(phrase, definition):
    # remove the brackets and clean up the definitions
    # with regex
    definition = definition.replace("[", "")
    definition = definition.replace("]", "")
    definition = definition.replace("'", "")
    definition = definition.replace('"', "")
    definition = definition.replace("(", "")
    definition = definition.replace(")", "")

    # remove double spaces
    definition = definition.replace("  ", " ")
    # also remove any .. by replacing them with a single .
    definition = definition.replace("..", ".")
    # remove all non-ascii characters
    definition = re.sub(r"[^\x00-\x7f]", r"", definition)
    # remove any words that are not in the english dictionary
    # english_words = set(w.lower() for w in nltk.corpus.words.words())
    # definition = re.sub(r'\b\w+\b', lambda m: m.group(0) if m.group(0) in english_words else '', definition)
    # remove extra spaces
    # definition = re.sub(' +', ' ', definition)

    #!phrase, definition = replacer_censor(definition, phrase, replacements)

    return phrase, definition


# get the links from the page Forbes_Celebrity_100 list on wikipedia and return them as a list
# def get_links_from_page(page):
#     # get the html of the page
#     html = requests.get(page).text
#     # create a BeautifulSoup object to parse the html
#     soup = BeautifulSoup(html, "html.parser")
#     # get the links from the page
#     links = soup.find_all("a", href=True)
#     # return the links that go to a wikipedia page
#     return [link["href"] for link in links if link["href"].startswith("/wiki/")]
import pandas as pd
import random

# peoplelinks = get_links_from_page("https://en.wikipedia.org/wiki/Forbes_Celebrity_100_list")
urls_master = pd.read_csv("./peoplelinks.csv", error_bad_lines=False)
# convert to list of urls urls_master.values[0][0]
urls_master = [urls_master.values[i][0] for i in range(len(urls_master))]
# only include urls with wikipedia in them
urls_master = [url for url in urls_master if "wikipedia" in url]


@sleep_and_retry
def get_random_wiki_entry():
    # Use a while loop to retry the request until a valid page is found.
    while True:
        try:
            URL = "https://randomincategory.toolforge.org/Random_page_in_category?"
            # shuffle categories to get a random selection
            random.shuffle(original_categories)
            # select 10 random categories
            # categories = original_categories[:20]
            # randomly sample 20 categories
            categories = random.sample(original_categories, 5)
            for cat in enumerate(categories):
                URL += f"&category{cat[0]}={urllib.parse.quote(str(cat[1]).lower())}"
            URL += "&server=en.wikipedia.org&cmnamespace=0&cmtype=page&returntype="

            # either randomly use URL or one of the urls from the urls_master list above
            activate_loop = True  # flag
            if random.randint(0, 1) == 0 or not activate_loop:
                try:
                    #!print("using random url from urls_master list")
                    # *URL = random.choice(urls_master)
                    # pick a random card title from the list of cards and get the related pages with the get_related_pages function
                    page_title = random.choice(card_deck)["title"]
                    URL = generate_related_deck(page_title, 10)[
                        0
                    ]  # get the first related page
                    # get the first related page
                    # tag1
                    print("using related page")
                except Exception as e:
                    pass
            else:
                pass

            # once every 30 times use Random article from Wikipedia
            if random.randint(0, 30) == 0:
                URL = "https://en.wikipedia.org/wiki/Special:Random"

            # Use requests to get the page, then pass the redirected page url to wikipedia library.
            req_url = requests.get(URL).url  # This is a random page from the category.
            req_html = requests.get(req_url).text
            # get the title with regex
            page_title_regex = r"<title>(.+?)</title>"
            page_title_match = re.search(page_title_regex, req_html)
            # get the title
            title = page_title_match.group(1)
            # remove the wikipedia part
            title = title.replace(" - Wikipedia", "")
            # remove the word wiki
            title = title.replace("Wiki", "")

            if re.search(r"\/\b(Wikipedia|Wiki)\b$", req_url, re.IGNORECASE):

                # Skip wikipedia pages.
                print("Skipping wikipedia page")
                continue

            # Using wikipedia library.
            page = wikipedia.page(title)  # This is a random page from the category.
            title = page.title
            # groupme_bot(str("Found a page for " + title))
            #!print("Found a page for ", title)
            # print(f'Page URL: {req_url}')
            summary = page.summary
            # categories = page.categories
            related = page.links

            # Create a dictionary of the entry.
            random_wiki_entry_dict = {
                "title": title,
                "summary": unpack_definitions(title, summary),
                "related": related,
            }

            return random_wiki_entry_dict
        except wikipedia.DisambiguationError as e:
            # If the page is not found, retry the request with a different URL.
            # print("DisambiguationError occurred:", e)
            return random_wiki_entry_dict


# make a card from the random wiki entry
def create_ppn_card():
    # create a person/place/thing card
    # get a random wikipedia entry

    try:
        random_wiki_entry_dict = get_random_wiki_entry()
        # get the summary of the entry
        random_wiki_entry_summary = random_wiki_entry_dict["summary"]
        # get the title of the entry
        random_wiki_entry_title = random_wiki_entry_dict["title"]
        # get the related pages of the entry
        random_wiki_entry_related = random_wiki_entry_dict["related"]

        # create a dictionary of the entry
        random_wiki_entry_dict = {
            "title": random_wiki_entry_title,
            "summary": random_wiki_entry_summary,
            "related": len(random_wiki_entry_related),
        }
    except:
        random_wiki_entry_dict = {
            "title": "error",
            "summary": "error",
            "related": "error",
        }
    # only return if the entry is unique and not a duplicate (check the title)
    return random_wiki_entry_dict
    # if random_wiki_entry_dict['title'] not in [card['title'] for card in card_deck]:
    #     return random_wiki_entry_dict
    # else:
    #     return {}


import re


def replace_definition_start(definition, title):
    # Create the pattern to search for
    if isinstance(definition, list):
        definition = definition[1]
    else:
        definition = str(definition)

    pattern = r"^{}\s+(is|was|are|were)\s+a\s+".format(re.escape(title))

    # Use the `search` function to find the first occurrence of the pattern
    match = re.search(
        pattern, definition, re.IGNORECASE
    )  # re.IGNORECASE makes the search case-insensitive
    if match:
        # Get the start and end indices of the match
        start, end = match.span()
        # Replace the match with "This is a"
        new_definition = "{}This is a {}".format(definition[:start], definition[end:])
        return new_definition
    return definition


def create_ppn_deck(num_cards=10, card_deck=[]):
    # create a deck of person/place/thing cards

    new_card_exists_flag = False
    while len(card_deck) < num_cards:
        temp = create_ppn_card()
        if temp != {}:
            # check if the card is unique
            if temp["title"] not in [card["title"] for card in card_deck]:

                # if the title has "List of" in it, skip it
                if "List of" in temp["title"]:
                    continue
                # clean up the summary:
                card_summary = (
                    temp["summary"][1]
                    if isinstance(temp["summary"], list)
                    else str(temp["summary"])
                )
                temp["summary"] = unpack_definitions(
                    temp["title"], card_summary
                )  # unpack the definitions

                card_deck.append(temp)
                # in the printline show the card number as the first element, which is the length of card_deck
                print(
                    f'card {len(card_deck)}: {temp["title"]}: \n\t{temp["summary"][1][0:60]}...'
                )
                new_card_exists_flag = True
            else:
                # print("duplicate card")
                # print(f'we have {len(card_deck)} cards so far')
                if new_card_exists_flag:
                    with open("ppn_deck.json", "w") as outfile:
                        json.dump(card_deck, outfile, indent=4)
                    new_card_exists_flag = False
        else:
            print("error creating card")
        if len(card_deck) % 20 == 0:
            groupme_bot(f"I have {len(card_deck)} cards so far")
            # show a random card by sampling the deck
            random_card = random.sample(card_deck, 1)[0]
            # print the card
            groupme_bot(f'{random_card["title"]}: {random_card["summary"]}')
    return card_deck


# ^ bot functions for groupme


def groupme_bot(
    message_text="Welcome to the ever expanding world of Generative Monikers! I am your host, Hubert.",
):
    # Replace :bot_id with your bot's ID
    # read bot_id from secrets.json
    with open("./secrets.json") as json_file:
        secrets = json.load(json_file)
        bot_id = secrets["groupme_botid"]

    # if the message is not a single string, convert it to a string
    if type(message_text) != str:
        message_text = str(message_text)

    # Set the payload for the request
    payload = {"bot_id": bot_id, "text": message_text[0:1000]}

    # Make the POST request to the GroupMe API
    response = requests.post("https://api.groupme.com/v3/bots/post", json=payload)

    # Check the status code of the response
    if response.status_code != 202:
        print(f"Failed to send message: {response.status_code} {response.text}")
    else:
        # print("Message sent successfully.")
        pass


# ^ card generating functions

# function one - a modified version of the create_ppn_deck function that generates a deck of cards that are related to a specific card instead of from the requests of the random page url generator.
def generate_related_deck(primary_card, number_of_cards_to_generate):
    # generate a deck of cards that are related to the primary card
    # get the title of the primary card
    primary_card_title = primary_card["title"]
    # get the related pages of the primary card
    primary_card_related = primary_card["related"]
    # create a list of the related pages
    related_pages = [page for page in primary_card_related]
    # shuffle the list of related pages
    random.shuffle(related_pages)
    # create a list of the related pages that are not already in the deck
    related_pages = [
        page
        for page in related_pages
        if page not in [card["title"] for card in card_deck]
    ]

    # now we have a list of related pages that are not already in the deck, we can create a
    # deck of cards from them
    while len(card_deck) < number_of_cards_to_generate:
        # get a random page from the list of related pages
        random_page = random.choice(related_pages)

        # using the wikipedia library we can get the summary of the page, the title of the page and the related pages of the page
        page = wikipedia.page(random_page)
        random_wiki_entry_summary = page.summary
        random_wiki_entry_title = page.title
        random_wiki_entry_related = page.links

        # create a dictionary of the entry
        random_wiki_entry_dict = {
            "title": random_wiki_entry_title,
            "summary": random_wiki_entry_summary,
            "related": len(random_wiki_entry_related),
        }
        print(f'{primary_card_title} >> {random_wiki_entry_dict["title"]}')
        # add the card to the deck if it it has not already been added (check the title)
        if random_wiki_entry_dict["title"] not in [card["title"] for card in card_deck]:
            card_deck.append(random_wiki_entry_dict)
            print(f"we have {len(card_deck)} cards so far")
            with open("sub_ppn_deck.json", "w") as outfile:
                json.dump(card_deck, outfile, indent=4)
        else:
            print("duplicate card")
            print(f"we have {len(card_deck)} cards so far")
            with open("sub_ppn_deck.json", "w") as outfile:
                json.dump(card_deck, outfile, indent=4)
    return card_deck


# ~ creating related decks
import random
import wikipedia
import json


@sleep_and_retry
def get_page_from_wiki(title):
    return wikipedia.page(title)


def page_is_person(page):
    # people pages have the words "birth" "family" and potentially "death" in the article text (birth and death are not always present). We can use this to filter out people pages.
    if "birth" in page.content.lower() and "family" in page.content.lower():
        return True
    else:
        return False


def page_is_location(page):
    # location pages have the words "location" "country" and "city" in the article text. We can use this to filter out location pages.
    if (
        "location" in page.content.lower()
        and "country" in page.content.lower()
        and "city" in page.content.lower()
    ):
        return True
    elif page.coordinates is not None:
        return True
    else:
        return False


def page_is_organization(page):
    # organization pages have the words "organization" "company" and "business" in the article text. We can use this to filter out organization pages.
    if (
        "organization" in page.content.lower()
        or "company" in page.content.lower()
        and "business" in page.content.lower()
    ):
        # also cannot be a person or location
        if not page_is_person(page) and not page_is_location(page):
            return True
        else:
            return False
    else:
        return False


def page_is_event(page):
    # event pages have the words "event" "incident" and "disaster" in the article text. We can use this to filter out event pages.
    if (
        "event" in page.content.lower()
        and "date" in page.content.lower()
        and "history" in page.content.lower()
    ):
        if (
            not page_is_person(page)
            and not page_is_location(page)
            and not page_is_organization(page)
        ):
            return True
        else:
            return False
    else:
        return False


def generate_related_deck(
    primary_card,
    number_of_cards_to_generate,
    min_len=100,
    min_links=5,
    people=True,
    locations=True,
    organizations=True,
    events=True,
    other=False,
):
    new_card_deck = []
    primary_card_title = primary_card["title"]
    primary_card_related = wikipedia.page(primary_card_title).links
    related_pages = [page for page in primary_card_related]
    random.shuffle(related_pages)
    related_pages = [
        page
        for page in related_pages
        if page not in [card["title"] for card in new_card_deck]
    ]

    # Loop through each related page
    for random_page in related_pages:
        try:
            page = get_page_from_wiki(random_page)
            random_wiki_entry_summary = page.summary
            random_wiki_entry_title = page.title
            random_wiki_entry_related = page.links
            random_wiki_entry_dict = {
                "title": random_wiki_entry_title,
                "summary": random_wiki_entry_summary,
                "related": len(random_wiki_entry_related),
            }
            if random_wiki_entry_dict["title"] not in [
                card["title"] for card in new_card_deck
            ]:

                # check for min length
                if len(random_wiki_entry_dict["summary"]) < min_len:
                    continue
                # check for min links
                if random_wiki_entry_dict["related"] < min_links:
                    continue

                # check for people, locations, organizations, events, and other categories in the related pages. Follow the logic outlined by T/F in the function arguments. If people is true for example, then we will add the page if it is a person. Else we ignore people pages.
                # people pages have the words "birth" "family" and potentially "death" in the article text (birth and death are not always present). We can use this to filter out people pages.
                # locations have a page.coordinates attribute that is not None
                # organizations - ?
                # events - have a date in the article text (not always present)?

                is_person = page_is_person(page)
                is_location = page_is_location(page)
                is_organization = page_is_organization(page)
                is_event = page_is_event(page)
                print(page.title)
                print(f"-" * 8)
                print(f"is_person: {is_person}")
                print(f"is_location: {is_location}")
                print(f"is_organization: {is_organization}")
                print(f"is_event: {is_event}")

                if people and is_person:
                    new_card_deck.append(random_wiki_entry_dict)
                    print(f'Added {random_wiki_entry_dict["title"]} to the deck')
                elif locations and is_location:
                    new_card_deck.append(random_wiki_entry_dict)
                    print(f'Added {random_wiki_entry_dict["title"]} to the deck')
                elif organizations and is_organization:
                    new_card_deck.append(random_wiki_entry_dict)
                    print(f'Added {random_wiki_entry_dict["title"]} to the deck')
                elif events and is_event:
                    new_card_deck.append(random_wiki_entry_dict)
                    print(f'Added {random_wiki_entry_dict["title"]} to the deck')
                elif (
                    other
                    and not is_person
                    and not is_location
                    and not is_organization
                    and not is_event
                ):
                    new_card_deck.append(random_wiki_entry_dict)
                    print(f'Added {random_wiki_entry_dict["title"]} to the deck')
                else:
                    print(f'Not adding {random_wiki_entry_dict["title"]} to the deck')
                # new_card_deck.append(random_wiki_entry_dict)
                # print(f'Added {random_wiki_entry_dict["title"]} to the deck')
                print(f'{primary_card_title} >> {random_wiki_entry_dict["title"]}')
            with open("./new_ppn_deck.json", "w") as outfile:
                json.dump(new_card_deck, outfile, indent=4)
            # Break the loop if the number of cards in the deck reaches the desired number
            # print(f'Number of cards in deck: {len(new_card_deck)}/{number_of_cards_to_generate}')
            if len(new_card_deck) >= number_of_cards_to_generate:
                # print("We have enough cards. Exiting loop.")
                break
        except Exception as e:
            continue
    return card_deck


# ^ refining functions
def refine_cards(card_deck):
    sentence_count = 1
    card_deck = [
        {
            **card,  # merge the card with the new summary
            **{  # create a new key called summary_short
                "summary_short": "".join(  # join the sentences together
                    str(sentence)  # convert the sentence to a string
                    for sentence in summarize_text(
                        card["summary"][1], int(sentence_count)
                    )
                )
            },
        }
        for card in card_deck
    ]
    # card_deck = [
    #     card
    #     for card in card_deck
    #     if not any(
    #         word in card["title"]
    #         for word in ["List", "Timeline of", "History of", "Wikipedia", "Category"]
    #     )
    # ]
    card_deck = [
        {
            **card,
            **{
                "summary_clean": str(
                    re.sub(r"[^a-zA-Z0-9]+", " ", card["summary_short"]).replace(
                        "\n", " "
                    )
                )
            },
        }
        for card in card_deck
    ]

    # card_deck = [
    #     {
    #         **card,
    #         **{
    #             "summary_clean": unpack_definitions(
    #                 card["title"], card["summary_clean"]
    #             )
    #         },
    #     }
    #     for card in card_deck
    # ]
    # print('cleaned')
    # card_deck = [
    #     {
    #         **card,
    #         **{
    #             "summary_short": str(card["summary_short"])[:1200][
    #                 : str(card["summary_short"])[:1200].rfind(".") + 1
    #             ]
    #         },
    #     }
    #     for card in card_deck
    #     if len(card["summary_short"]) > 1200
    # ]
    talk = "I have refined the deck, so far I have " + str(len(card_deck)) + " cards"
    # groupme_bot(talk)
    return card_deck


# ^ Creating a printable deck of cards with Pillow

# import random
# import textwrap
# import os
# from PIL import Image, ImageDraw, ImageFont
# import pytrends
# # build a pytrends object with the Google Trends API
# pytrend = pytrends.TrendReq(hl='en-US', tz=360)
# # with open("ppn_deck_cleaned.json", "w") as write_file:
# #     json.dump(card_deck, write_file, indent=4)

# def get_google_trends_score(title):
#     try:
#         pytrend.build_payload([title])
#         trend_data = pytrend.interest_over_time()
#         point_value = trend_data[title].mean()
#     except:
#         point_value = 10

#     return int(point_value)

# def generate_card(title, definition, points):
#     # determine the font size based on the length of the definition
#     # font_size = int(len(definition) / 20)
#     font_size = max(30, int(len(definition) / 20))
#     # create the image and draw objects
#     # set the canvas size to 8.5 cm by 5.5 cm
#     image = Image.new('RGB', (550, 850), (255, 255, 255))
#     draw = ImageDraw.Draw(image)

#     # select a font and draw the title in a rectangle
#     font = ImageFont.truetype('./fonts/Menlo.ttc', 15)
#     draw.rectangle([(10, 10), (540, 50)], fill='lightgrey')
#     draw.text((20, 20), title, fill=(0, 0, 0), font=font)

#     # draw the definition in a rectangle, and soft wrap the text. Don't exceed 40 characters per line.
#     # wrapped_definition = textwrap.wrap(definition, width=40)
#     definition = str(definition) if isinstance(definition, str) else definition[0]
#     wrapped_definition = textwrap.fill(definition, width=80)
#     wrapped_definition_str = "\n".join(wrapped_definition)
#     font = ImageFont.truetype('./fonts/Menlo.ttc', font_size)
#     draw.text((20, 70), wrapped_definition_str, fill=(0, 0, 0))

#     # draw a circle around the point value
#     draw.ellipse([(520, 820), (540, 840)], fill='lightblue')
#     # draw the point value

#     font = ImageFont.truetype('./fonts/Menlo.ttc', font_size)
#     draw.text((525, 825), str(points), fill=(0, 0, 0))

#     # save the image
#     image.save('./card_images/{}.png'.format(len(os.listdir('./card_images/'))))

# def generate_physical_cards():
#     #^ Example usage
#     card = random.choice(card_deck)
#     print(card)
#     summary = card['summary'][1] if isinstance(card['summary'], list) else card['summary']
#     # summarize the definition with the summarize function
#     summary = summarize_text(summary, 2) if isinstance(summary, str) else summary # if the summary is a list, then it's already been summarized
#     generate_card(str(card['title']), summary, points=get_google_trends_score(card['title']))
#     # generate_card('test title', 'test definition', 10)

#     # iterate through each card and generate a card image, starting with the index of the last card image
#     for card in tqdm(card_deck[len(os.listdir('./card_images/'))]):
#         title = card['title']
#         summary = card['summary'][1] if isinstance(card['summary'], list) else card['summary']
#         # summarize the definition with the summarize function
#         summary = summarize_text(summary, 2) if isinstance(summary, str) else summary # if the summary is a list, then it's already been summarized
#         generate_card(str(card['title']), summary, points=get_google_trends_score(card['title']))


# ^ google forms functions


english_words = words.words()
# open the card deck file
with open("ppn_deck.json", "r") as read_file:
    card_deck = json.load(read_file)

while len(card_deck) < 10000:
    print(len(card_deck))
    # stringval = 'Building the deck...' + str(len(card_deck)), 'cards'
    # groupme_bot(stringval)
    card_deck = create_ppn_deck(10000, card_deck)
    # create a copy of the card deck file for safety
    with open("ppn_deck_copy.json", "w") as outfile:
        json.dump(card_deck, outfile, indent=4)
    # groupme_bot('I have created a copy of the deck for safety, so far I have ' + str(len(card_deck)) + ' cards')
    # show an example card (random sample)
    # * card_deck = refine_cards(card_deck)
    # card_deck = [card for card in card_deck if len(card["summary_short"]) >= 100]
    # summarize the cards summaries to 2 sentences in one line
    card_deck = [
        {
            **card,
            **{
                "summary_short": "".join(
                    str(sentence) for sentence in summarize_text(card["summary"], 2)
                )
            },
        }
        for card in card_deck
    ]  # summarize the cards summaries to 2 sentences in one line
    random_card = random.choice(card_deck)
    # every 100 cards, show an example card
    if len(card_deck) % 100 == 0:
        stringval = (
            "For example, here is a card: "
            + str(random_card["title"])
            + " "
            + str(random_card["summary_short"])
        )
        groupme_bot(stringval)
    with open("ppn_deck.json", "w") as outfile:
        json.dump(card_deck, outfile, indent=4)
    # groupme message that the deck has been created and is being saved as pngs
    message = (
        "I have created a deck of "
        + str(len(card_deck))
        + " cards, and am now saving them as images"
    )
    groupme_bot(message)
    #!generate_physical_cards()
print(f"I have created a deck of {len(card_deck)} cards")


from nltk.metrics.distance import edit_distance
import json
import nltk
from nltk.corpus import wordnet
import random
import nltk
from nltk.corpus import wordnet
from tqdm import tqdm


def find_synonyms(word):
    synonyms = []
    lemmatizer = nltk.WordNetLemmatizer()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name()
            if synonym != word and synonym not in synonyms:
                synonyms.append(synonym)
    return set(synonyms)


# open the card deck file
with open("ppn_deck.json", "r") as read_file:
    card_deck = json.load(read_file)

stop_words = nltk.corpus.stopwords.words("english")


def find_similar_words(title, definition, threshold=3):
    # split the definition into a list of words
    if type(definition) == list:
        definition = " ".join(definition)
    words = definition.split()
    # remove words less than 3 characters and any english stop words
    words = [word for word in words if word not in stop_words]
    words = [word for word in words if len(word) > 3]
    # use a list comprehension to create a list of words with a Levenshtein distance less than the threshold
    # split the title into a list of words
    title = title.split()
    similar_words_list = []
    for title_word in title:
        similar_words = [
            word for word in words if edit_distance(title_word, word) <= threshold
        ]
        # append the similar words to the list of similar words
        similar_words_list.extend(similar_words)
    # remove duplicate words
    similar_words = set(similar_words_list)

    return similar_words


def replace_similar_words(title, definition, threshold=3):
    similar_words = find_similar_words(title, definition, threshold)

    # replace each similar word with a synonym
    for word in similar_words:
        synonyms = find_synonyms(word)  # find a synonym for the word -> set
        # extract the synonym from the set
        synonyms = list(synonyms)
        # choose a random synonym from the set
        try:
            synonym = random.choice(synonyms)
        except IndexError:
            synonym = word

        # print(f"Replacing {word} with {synonym}")
        if type(definition) == list:
            definition = " ".join(definition)
        definition = definition.replace(word, synonym)

    return definition


# iterate through each card and replace the similar words in the summary_short with synonyms
for card in tqdm(card_deck):
    title = card["title"]
    definition = card["summary"]
    definition = replace_similar_words(title, definition)

    # update the definition in the card dictionary
    card["summary_short"] = definition

# save the card deck to a new file
with open("ppn_deck_cleaned.json", "w") as write_file:
    json.dump(card_deck, write_file, indent=4)
