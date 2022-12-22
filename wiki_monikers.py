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
URL += f"category={urllib.parse.quote('famous fictional characters')}"
URL += f"&category2={urllib.parse.quote('historical figures')}"
URL += f"&category3={urllib.parse.quote('slogans')}"
URL += f"&category4={urllib.parse.quote('catchphrases')}"
URL += f"&category5={urllib.parse.quote('authors')}"
URL += f"&category6={urllib.parse.quote('actors')}"
URL += f"&category7={urllib.parse.quote('british authors')}"
URL += f"&category8={urllib.parse.quote('american authors')}"
URL += f"&category9={urllib.parse.quote('musicians')}"
URL += f"&category10={urllib.parse.quote('songs')}"
URL += f"&category11={urllib.parse.quote('books')}"
URL += f"&category12={urllib.parse.quote('movies')}"
URL += "&category{}={{urllib.parse.quote('{}')}}".format(13, "celebrities")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(14, "politicians")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(15, "sportspeople")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(16, "famous paintings")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(17, "historical events")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(18, "famous quotes")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(19, "famous poems")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(20, "memes")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(21, "hashtags")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(22, "United States Presidents")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(23, "United States Vice Presidents")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(24, "United States Senators")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(25, "World Leaders")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(26, "World War II Leaders")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(27, "World War I Leaders")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(28, "Viral Videos")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(29, "Viral Songs")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(30, "Viral Memes")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(31, "Viral Hashtags")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(32, "Terrible People")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(33, "Terrible Events")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(34, "Acronyms")
URL += "&category{}={{urllib.parse.quote('{}')}}".format(35, "United States Cities")
URL += "&server=en.wikipedia.org&cmnamespace=&cmtype=page&returntype="


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
    return random_wiki_entry_dict


def create_ppn_deck(num_cards=500, card_deck=[]):
    # create a deck of person/place/thing cards

    while len(card_deck) < num_cards:
        card_deck.append(create_ppn_card())
    return card_deck


english_words = words.words()
card_deck = []

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
