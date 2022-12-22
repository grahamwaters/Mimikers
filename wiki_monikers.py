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

categories = [
    "Fictional characters",
    "People",
    "Slogans",
    "celebrities",
    "Cities",
    "Famous quotes",
    "psychological disorders",
    "Diseases",
    "Medical conditions",
    "famous court cases",
    "Famous crimes",
    "art movements",
    "art techniques",
    "art styles",
    "laws of physics",
    "well-known laws",
    "well-known theorems",
    "well-known equations",
    "well-known formulas",
    "well-known proofs",
    "well-known conjectures",
    "well-known people",
    "Famous Criminals",
    "paradoxes",
    "Famous speeches",
    "mythical creatures",
    "Famous last words",
    "epigrams",
    "adages",
    "Historical events",
    "Mythological figures",
    "Landmarks",
    "Inventions",
    "Scientists",
    "Artists",
    "Writers",
    "Musicians",
    "Athletes",
    "memes",
    "Political figures",
    "TV shows",
    "Movies",
    "Video games",
    "Animals",
    "Chemical compounds",
    "Astronomical objects",
    "Geographical features",
    "Countries",
    "Languages",
    "Cultures",
    "Holidays",
    "Words and phrases",
    "Proverbs",
    "Idioms",
    "Slang terms",
    "Jokes",
    "Riddles",
    "Events",
    "Pop culture",
    "Literature",
    "Art",
    "80s pop culture",
    "90s pop culture",
    "2000s pop culture",
    "2010s pop culture",
    "2020s pop culture",
    "70s pop culture",
    "60s pop culture",
    "50s pop culture",
    "popular music",
    "popular movies",
    "popular television",
    "popular books",
    "popular video games",
    "tiktok trends",
    "tiktok memes",
    "tiktok dances",
    "tiktok challenges",
    "tiktok songs",
    "vine trends",
    "vine memes",
    "vine dances",
    "vine challenges",
    "teen slang",
    "teen memes",
    "teen dances",
    "millennial slang",
    "millennial memes",
    "millennial dances",
    "millennial challenges",
    "millennial songs",
    "gen z slang",
    "gen z memes",
    "gen z dances",
    "gen z challenges",
    "gen z songs",
    "gen z trends",
    "Science and technology",
    "Nature and the environment",
    "Food and drink",
    "Sports and recreation"
]

import random
# shuffle categories to get a random selection
random.shuffle(categories)
for cat in enumerate(categories):
    URL += f"&category{cat[0]}={urllib.parse.quote(str(cat[1]).lower())}"

URL += "&server=en.wikipedia.org&cmnamespace=0&cmtype=page&returntype="

replacements = {
    r"\bsex\b": "affection",
    r"\bporn\w*\b": "adult entertainment",
    r"fuck": "have intimate relations with",
    r"fucking": "romancing, physically",
    r"\bfuck\w*\b": " (bleep) ",
    r"\bass\b": "dump truck",
    r"\bshit\w*\b": "poop",
    r"damn\w*\b": "darn",
    r"god-damn\w*\b|goddamn\w*\b": "super darn",
    r"\bass\b|\wasse*": "rear end",
    r"cock": "rooster",
    r"small dick energy": "little man syndrome",
    r"\bdick\w*\b": " johnson ",
    r"ppl": "people",
    "\bwat\b": "what",
    r"a black": "an african-american",
    r"black person": "dark skinned person",
    r"\bpee\b": "urinate",
    r"\bpiss\b": "urinate",
    r"\b(peeing|pissing)": "urinating",
    r"white person": "caucasian",
    r"\bwhore\w*\b": "prostitute",
    r"nigg*": "racial slur",
    "\r\n": " ",
    r"\bslut\b": " loose person ",
    r"\bblowjob\b": "random gift",
    r"racist": "ignorant",
    "racism": "fear of people that look different",
    r"faggot": "gay person",
    r"\bfag\w*\b": "gay person",
    r"boob|boob*|breast": "lady pillows",
    r"\bbitch*\b": "mean woman",
    r"bastard*": "illegitimate child",
    r"hoes?": "chicks",
    r"breast*|jugs": "chest",
    r"\bcunt*\b": "comtemptible person",
    r"\bpuss\w*\b": "vagina",
    r"\wdick*": "penis",
    r"naked": "disrobed",
    r"\bnud\w*\b": "unclothed",
    r"\nmasterbate\w*\b": "self-gratified",
    r"\bmasturbating\w*\b": "gratifying themselves",
    r"\b\w{4}ilf\b": "person id like to get to know",
    r"mastu\w*\b": "self-gratification",
    "god": "deity",
    "jesus": "religious figure",
    "christ": "religious figure",
    "bible": "religious text",
    "church": "place of worship",
    "religion": "set of beliefs",
    r"\bpray\w*\b": "communicate with a deity",
    "prayer": "a conversation with a deity",
    "faith": "belief",
    " lord ": "captain",
    " allah ": "a diety",
    "gay": "homosexual",
    r" rapist ": " intense toucher ",
    r" rape ": " unwelcomed tickling ",  # eek I know...
    r"pedo\w*\b": "seventies mustached van driver",
    "yahwey": "a deity",
    "yeshua": "a religious figure",
    " sexual": " reproductive",
    "douche": "chad",
    " sex ": " private adult time ",
    "milf": "mother I would like to take on a date",
    " butt ": "dumptruck/tailgate",
}


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

    phrase, definition = replacer_censor(definition, phrase, replacements)

    return phrase, definition


@sleep_and_retry
def get_random_wiki_entry():
    # Use a while loop to retry the request until a valid page is found.
    while True:
        try:
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
            print("Found a page for ", title)
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
            #print("DisambiguationError occurred:", e)
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
        # get the categories of the entry
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


def create_ppn_deck(num_cards=10, card_deck=[]):
    # create a deck of person/place/thing cards

    while len(card_deck) < num_cards:
        temp = create_ppn_card()
        if temp != {}:
            # check if the card is unique
            if temp["title"] not in [card["title"] for card in card_deck]:
                card_deck.append(temp)
            else:
                print("duplicate card")
                print(f'we have {len(card_deck)} cards so far')
                with open('ppn_deck.json', 'w') as outfile:
                    json.dump(card_deck, outfile, indent=4)
    return card_deck


english_words = words.words()
# open the card deck file
with open("ppn_deck.json", "r") as read_file:
    card_deck = json.load(read_file)

while len(card_deck) < 500:
    card_deck = create_ppn_deck(500, card_deck)
    sentence_count = 2
    card_deck = [
        {
            **card,
            **{
                "summary_short": "".join(
                    str(sentence)
                    for sentence in summarize_text(
                        card["summary"][1], int(sentence_count)
                    )
                )
            },
        }
        for card in card_deck
    ]
    card_deck = [
        card
        for card in card_deck
        if not any(
            word in card["title"]
            for word in ["List", "Timeline of", "History of", "Wikipedia", "Category"]
        )
    ]
    card_deck = [
        {
            **card,
            **{
                "summary_clean": str(
                    re.sub(r"[^a-zA-Z0-9]+", " ", card["summary_short"]).replace("\n", " ")
                )
            },
        }
        for card in card_deck
    ]
    print('shortened')
    # card_deck = [
    #     card
    #     for card in card_deck
    #     if len(
    #         word_tokenize(
    #             [word for word in card["summary_clean"] if str(word) in english_words]
    #         )
    #     )
    #     >= len(card["summary_short"]) / 4
    # ]
    card_deck = [
        {
            **card,
            **{
                "summary_clean": unpack_definitions(
                    card["title"], card["summary_clean"]
                )
            },
        }
        for card in card_deck
    ]
    print('cleaned')
    card_deck = [
        {
            **card,
            **{
                "summary_short": str(card["summary_short"])[:1200][
                    : str(card["summary_short"])[:1200].rfind(".") + 1
                ]
            },
        }
        for card in card_deck
        if len(card["summary_short"]) > 1200
    ]
    card_deck = [card for card in card_deck if len(card["summary_short"]) >= 100]

    with open('ppn_deck.json', 'w') as outfile:
        json.dump(card_deck, outfile, indent=4)
print(f"I have created a deck of {len(card_deck)} cards")
