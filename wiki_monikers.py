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

import pandas as pd

with open("categories.json", "r") as f:
    categories = json.load(f)

categories = [category.strip() for category in categories]

base_categories = categories.copy()

meme_categories = [
    "Internet_memes_introduced_in_{}".format(str(year)) for year in range(2000, 2023)
]

with open("meme_categories.json", "w") as f:
    json.dump(meme_categories, f)


year_categories = [
    "{}s_in_Internet_culture".format(str(year)) for year in range(1980, 2020, 10)
]



charactersTV = ['Television_characters_introduced_in_{}'.format(str(year)) for year in range(1950,2023)]


with open("charactersTV.json", "w") as f:
    json.dump(charactersTV, f)


VideoGames_Categories = ['{}_video_games'.format(str(year)) for year in range(2012,2010,2)]


with open("VideoGames_Categories.json", "w") as f:
    json.dump(VideoGames_Categories, f)




categories = base_categories

categories.extend(meme_categories)


categories.extend(year_categories)

categories.extend(charactersTV)



extras = ['English-language_idioms','British_English_idioms']
categories.extend(extras)

most_linkedto_categories = ['Living_people']
categories.extend(most_linkedto_categories)


with open("categories.json", "w") as f:
    json.dump(categories, f)


original_categories = categories.copy()

original_categories = list(set(categories))
categories = original_categories.copy()

original_categories.sort()

import random


random.shuffle(categories)

categories = categories[:20]
for cat in enumerate(categories):
    URL += f"&category{cat[0]}={urllib.parse.quote(str(cat[1]).lower())}"

URL += "&server=en.wikipedia.org&cmnamespace=0&cmtype=page&returntype="



import wikipedia





def check_for_new_messages():
    with open("./secrets.json") as json_file:
        secrets = json.load(json_file)
        bot_id = secrets["

    global groupme_api

    latest_messages = groupme_api.get_latest_messages()


    new_messages = [message for message in latest_messages if message['sender_id'] != bot_id]

    return new_messages


def add_category(message):

    try:
        wikipedia.WikipediaPage(message).category
        is_valid_category = True
    except wikipedia.exceptions.PageError:
        is_valid_category = False


    if is_valid_category:
        with open("categories.txt", "a") as categories_file:
            categories_file.write(f"{message}\n")

    else:
        pass

def replacer_censor(definition, phrase, replacements_dict):

    for pattern in replacements_dict:

        phrase = re.sub(pattern, replacements_dict[pattern], phrase)
        definition = re.sub(pattern, replacements_dict[pattern], definition)
    return phrase, definition



def summarize_text(text, num_sentences):
    """
    Summarize the given text using the LSA or LexRank summarization algorithms and return the summary as a list of sentences
    """

    parser = PlaintextParser.from_string(text, Tokenizer("english"))


    algorithm = LexRankSummarizer()


    summary = algorithm(parser.document, num_sentences)

    return summary



def unpack_definitions(phrase, definition):


    definition = definition.replace("[", "")
    definition = definition.replace("]", "")
    definition = definition.replace("'", "")
    definition = definition.replace('"', "")
    definition = definition.replace("(", "")
    definition = definition.replace(")", "")


    definition = definition.replace("  ", " ")

    definition = definition.replace("..", ".")

    definition = re.sub(r"[^\x00-\x7f]", r"", definition)








    return phrase, definition












import pandas as pd
import random


urls_master = pd.read_csv("./peoplelinks.csv", error_bad_lines=False)

urls_master = [urls_master.values[i][0] for i in range(len(urls_master))]

urls_master = [url for url in urls_master if "wikipedia" in url]


@sleep_and_retry
def get_random_wiki_entry(category_sample_size=3):

    while True:
        try:
            URL = "https://randomincategory.toolforge.org/Random_page_in_category?"
            categories = random.sample(original_categories, category_sample_size)
            for cat in enumerate(categories):
                URL += f"&category{cat[0]}={urllib.parse.quote(str(cat[1]).lower())}"
            URL += "&server=en.wikipedia.org&cmnamespace=0&cmtype=page&returntype="


            activate_loop = True
            if random.randint(0, 1) == 0 or not activate_loop:
                try:
                    URL = random.choice(urls_master)

                    page_title = random.choice(card_deck)["title"]
                    URL = generate_related_deck(page_title, 10)[
                        0
                    ]

                    print("using related page")
                except Exception as e:
                    pass
            else:
                pass


            if random.randint(0, 60) == 0:
                print("using random article from wikipedia")
                if random.randint(0, 1) == 0:
                    URL = "https://en.wikipedia.org/wiki/Special:Random"
                else:
                    URL = 'https://en.wikiquote.org/wiki/Special:Random'

            req_url = requests.get(URL).url
            req_html = requests.get(req_url).text

            page_title_regex = r"<title>(.+?)</title>"
            page_title_match = re.search(page_title_regex, req_html)

            title = page_title_match.group(1)

            title = title.replace(" - Wikipedia", "")

            title = title.replace("Wiki", "")

            if re.search(r"\/\b(Wikipedia|Wiki)\b$", req_url, re.IGNORECASE):


                print("Skipping wikipedia page")
                continue


            page = wikipedia.page(title)
            title = page.title
            short_summary = wikipedia.summary(title, sentences=3)



            summary = page.summary

            related = page.links


            random_wiki_entry_dict = {
                "title": title,
                "summary": unpack_definitions(title, summary),
                "related": related,
            }

            return random_wiki_entry_dict
        except wikipedia.DisambiguationError as e:


            return random_wiki_entry_dict










def create_ppn_card():


    try:
        random_wiki_entry_dict = get_random_wiki_entry()

        random_wiki_entry_summary = random_wiki_entry_dict["summary"]

        random_wiki_entry_title = random_wiki_entry_dict["title"]

        random_wiki_entry_related = random_wiki_entry_dict["related"]


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






import re


def replace_definition_start(definition, title):

    if isinstance(definition, list):
        definition = definition[1]
    else:
        definition = str(definition)

    pattern = r"^{}\s+(is|was|are|were)\s+a\s+".format(re.escape(title))


    match = re.search(
        pattern, definition, re.IGNORECASE
    )
    if match:

        start, end = match.span()

        new_definition = "{}This is a {}".format(definition[:start], definition[end:])
        return new_definition
    return definition


def create_ppn_deck(num_cards=10, card_deck=[]):


    new_card_exists_flag = False
    while len(card_deck) < num_cards:
        temp = create_ppn_card()
        if temp != {}:

            if temp["title"] not in [card["title"] for card in card_deck]:


                if "List of" in temp["title"]:
                    continue

                card_summary = (
                    temp["summary"][1]
                    if isinstance(temp["summary"], list)
                    else str(temp["summary"])
                )
                temp["summary"] = unpack_definitions(
                    temp["title"], card_summary
                )

                card_deck.append(temp)

                print(
                    f'card {len(card_deck)}: {temp["title"]}: \n\t{temp["summary"][1][0:60]}...'
                )
                new_card_exists_flag = True
            else:


                if new_card_exists_flag:
                    with open("ppn_deck.json", "w") as outfile:
                        json.dump(card_deck, outfile, indent=4)
                    new_card_exists_flag = False
        else:
            print("error creating card")
        if len(card_deck) % 20 == 0:


            random_card = random.sample(card_deck, 1)[0]


    return card_deck





def groupme_bot(
    message_text="Welcome to the ever expanding world of Generative Monikers! I am your host, Hubert.",
):


    with open("./secrets.json") as json_file:
        secrets = json.load(json_file)
        bot_id = secrets["


    if type(message_text) != str:
        message_text = str(message_text)


    payload = {"bot_id": bot_id, "text": message_text[0:1000]}


    response = requests.post("https://api.groupme.com/v3/bots/post", json=payload)


    if response.status_code != 202:
        print(f"Failed to send message: {response.status_code} {response.text}")
    else:

        pass





def generate_related_deck(primary_card, number_of_cards_to_generate):


    primary_card_title = primary_card["title"]

    primary_card_related = primary_card["related"]

    related_pages = [page for page in primary_card_related]

    random.shuffle(related_pages)

    related_pages = [
        page
        for page in related_pages
        if page not in [card["title"] for card in card_deck]
    ]



    while len(card_deck) < number_of_cards_to_generate:

        random_page = random.choice(related_pages)


        page = wikipedia.page(random_page)
        random_wiki_entry_summary = page.summary
        random_wiki_entry_title = page.title
        random_wiki_entry_related = page.links


        random_wiki_entry_dict = {
            "title": random_wiki_entry_title,
            "summary": random_wiki_entry_summary,
            "related": len(random_wiki_entry_related),
        }
        print(f'{primary_card_title} >> {random_wiki_entry_dict["title"]}')

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



import random
import wikipedia
import json


@sleep_and_retry
def get_page_from_wiki(title):
    return wikipedia.page(title)


def page_is_person(page):

    if "birth" in page.content.lower() and "family" in page.content.lower():
        return True
    else:
        return False


def page_is_location(page):

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

    if (
        "organization" in page.content.lower()
        or "company" in page.content.lower()
        and "business" in page.content.lower()
    ):

        if not page_is_person(page) and not page_is_location(page):
            return True
        else:
            return False
    else:
        return False


def page_is_event(page):

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


                if len(random_wiki_entry_dict["summary"]) < min_len:
                    continue

                if random_wiki_entry_dict["related"] < min_links:
                    continue







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


                print(f'{primary_card_title} >> {random_wiki_entry_dict["title"]}')
            with open("./new_ppn_deck.json", "w") as outfile:
                json.dump(new_card_deck, outfile, indent=4)


            if len(new_card_deck) >= number_of_cards_to_generate:

                break
        except Exception as e:
            continue
    return card_deck



def refine_cards(card_deck):
    sentence_count = 1
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

























    talk = "I have refined the deck, so far I have " + str(len(card_deck)) + " cards"

    return card_deck














































































english_words = words.words()

with open("ppn_deck.json", "r") as read_file:
    card_deck = json.load(read_file)

while len(card_deck) < 16000:
    print(len(card_deck))


    card_deck = create_ppn_deck(16000, card_deck)

    with open("ppn_deck_copy.json", "w") as outfile:
        json.dump(card_deck, outfile, indent=4)





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
    ]
    random_card = random.choice(card_deck)

    if len(card_deck) % 100 == 0:
        stringval = (
            "For example, here is a card: "
            + str(random_card["title"])
            + " "
            + str(random_card["summary_short"])
        )

    with open("ppn_deck.json", "w") as outfile:
        json.dump(card_deck, outfile, indent=4)

    message = (
        "I have created a deck of "
        + str(len(card_deck))
        + " cards, and am now saving them as images"
    )


print(f"I have created a deck of {len(card_deck)} cards")


from nltk.metrics.distance import edit_distance
import json
import nltk
from nltk.corpus import wordnet
import random
import nltk
from nltk.corpus import wordnet
from tqdm import tqdm
from main import base_categories


def find_synonyms(word):
    synonyms = []
    lemmatizer = nltk.WordNetLemmatizer()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name()
            if synonym != word and synonym not in synonyms:
                synonyms.append(synonym)
    return set(synonyms)



with open("ppn_deck.json", "r") as read_file:
    card_deck = json.load(read_file)

stop_words = nltk.corpus.stopwords.words("english")


def find_similar_words(title, definition, threshold=3):

    if type(definition) == list:
        definition = " ".join(definition)
    words = definition.split()

    words = [word for word in words if word not in stop_words]
    words = [word for word in words if len(word) > 3]


    title = title.split()
    similar_words_list = []
    for title_word in title:
        similar_words = [
            word for word in words if edit_distance(title_word, word) <= threshold
        ]

        similar_words_list.extend(similar_words)

    similar_words = set(similar_words_list)

    return similar_words


def replace_similar_words(title, definition, threshold=3):
    similar_words = find_similar_words(title, definition, threshold)


    for word in similar_words:
        synonyms = find_synonyms(word)

        synonyms = list(synonyms)

        try:
            synonym = random.choice(synonyms)
        except IndexError:
            synonym = word


        if type(definition) == list:
            definition = " ".join(definition)
        definition = definition.replace(word, synonym)

    return definition



for card in tqdm(card_deck):
    title = card["title"]
    definition = card["summary"]
    definition = replace_similar_words(title, definition)


    card["summary_short"] = definition


with open("ppn_deck_cleaned.json", "w") as write_file:
    json.dump(card_deck, write_file, indent=4)
