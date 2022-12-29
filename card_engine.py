import json
import os
import warnings
import random
import re
from html2image import Html2Image
from tqdm import tqdm
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer
from icecream import ic
from PIL import Image
from profanity_check import predict, predict_prob
# using contextual spell checking
# verify that python -m spacy download en_core_web_sm has been run
#!python -m spacy download en_core_web_sm

#!pip install textblob
from textblob import TextBlob
#!pip install autocorrect
from autocorrect import Speller # for spell checking
import textstat
# constants
spell_check_flag = False
# ignore warnings
warnings.filterwarnings("ignore")

# functions

def summarize_text(text, num_sentences):
    #ic()
    """
    Summarize the given text using the LSA or LexRank summarization algorithms and return the summary as a string
    """

    parser = PlaintextParser.from_string(text, Tokenizer("english"))

    algorithm = LexRankSummarizer()

    summary = algorithm(parser.document, num_sentences)
    summary_text = "\n".join([str(sentence) for sentence in summary])
    return summary_text

def clear_card_box(card_box_directory):
    for file in os.listdir(card_box_directory):
        os.remove(os.path.join(card_box_directory, file))

# clear the card box directory
# clear_card_box('new_card_box') #note: to clear the card box, uncomment this line

def generate_card(
    title: str,
    description: str,
    points: str,
    html_template: str,
    name: str,
    links_on_wikipedia: str,
    category="Wild Card",
):
    filename = "{}.png".format(title.replace(" ", "_").lower())
    if os.path.exists("./new_card_box/{}".format(filename)) and "Test_Card" not in filename:
        print(f"Card {title} already exists, skipping...")
        return
    width_cm = 5.5
    height_cm = 8.5
    card_color = "green"
    # card_color = card['card_color']
    width_pixels = int(width_cm * 96)
    height_pixels = int(height_cm * 96)
    points = int(points)
    points = str(points)
    links_on_wikipedia = str(links_on_wikipedia)
    html = html_template
    if category == "Wild Card":
        if "(" in title and ")" in title:
            category = title[title.index("(") + 1 : title.index(")")]
            title = title.replace("({})".format(category), "")
            category = category.strip()

        elif "[" in title and "]" in title:
            category = title[title.index("[") + 1 : title.index("]")]
            title = title.replace("[{}]".format(category), "")
            category = category.strip()
        else:
            if category == "other":
                category = "Wild Card"


    if description[0] == "[" or description[0] == "(":
        # then this is a tuple still, and must be extracted from the description. Look for '.' (must include the ') and get the following text to the end of the string. This is the description.
        try:
            description = str(description).split("', '")[1] # get the second element of the tuple (the description)
            description = description.replace("')", "") # remove the trailing ')'
            description = description.replace("]", "") # remove the trailing ')'
            description = description.replace(")", "") # remove the trailing ')'
            description = description.replace("',", "") # remove the trailing ')'

            #note: I know this is unconventional and a hack, I am replacing '\n' occurrences here with a space.
            while '\\n' in description:
                description = description.replace('\\n', ' ')
            # description = description.replace("\n", " ")
            description = description.replace("\\r", " ")
            description = description.replace("\\t", " ")
            description = description.replace("\\v", " ")
            description = description.replace("\\f", " ")
            while "  " in description:
                description = description.replace("  ", " ")
        except Exception as e:
            description = str(description)
    # convert the description to a string
    description = str(description)
    description_words = description.split(" ")
    stripped_words = [re.sub(r"\n|\\n", "", word) for word in description_words]
    description = " ".join(stripped_words) # convert the list of words back to a string
    description = description.replace(" - ", " ")

    # skip the british television cards
    if 'british television' in description.lower():
        return
    if 'british television' in title.lower():
        return


    while "  " in description:
        description = description.replace("  ", " ")
    description = clean_string(description)
    #ic()
    #!assert (len(description) > 0, "There is no Description")
    if category == None:
        category = "Wild Card"
    if category == 'Wild Card':
        card_color = 'red'
    elif category in ['person', 'people', 'character', 'characters','actor']:
        card_color = 'blue'
    elif category == 'Place':
        card_color = 'yellow'
    #elif category == r'\d\d\d\d': # if the category is a year (e.g. 1999)
    elif category.isdigit() or (len(category) == 4 and category.isnumeric()): # if the category is a year (e.g. 1999)
        card_color = 'orange'
    elif category == 'book':
        card_color = 'purple'
    elif category == 'melon':
        card_color = 'pink'
    elif category == 'event':
        card_color = 'brown'
    elif category == 'movie':
        card_color = 'teal'
    elif category == 'animal':
        card_color = 'navy'
    elif category == 'die':
        card_color = 'grey'
    else:
        card_color = 'green'
    # if '\n' or '\r' or '\t' or '\v' or '\f' or any special character in description, then replace it with a space and print a warning
    if '\\n' in description:
        print('Warning: \\n in description')
        description = description.replace('\n', ' ')
    if '\\r' in description:
        print('Warning: \\r in description')
        description = description.replace('\r', ' ')
    if '\\t' in description:
        print('Warning: \\t in description')
        description = description.replace('\t', ' ')

    print(description) #note: debug

    html = html.replace("CARD_TITLE", title)
    html = html.replace("CARD_DESCRIPTION", description)
    html = html.replace("CARD_CATEGORY", category)
    html = html.replace("CARD_POINTS", str(points))
    html = html.replace("CARD_NAME", str(title))
    html = html.replace("CARD_COLOR", str(card_color))

    html = html.replace("WIDTH_PIXELS", str(width_pixels))
    html = html.replace("HEIGHT_PIXELS", str(height_pixels))
    html = html.replace("WIKILINKS", str(links_on_wikipedia))

    hti = Html2Image()

    output_path = "./card_box/"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:
        # Generate the image file
        filename = "{}.png".format(re.sub(r"[^\w\s]", "", title).replace(" ", "_"))
        filename = filename.lower()
        savepath = os.path.join(output_path, filename)
        hti.output_path = output_path
        hti.screenshot(html_str=html, save_as=filename)

        print(f"Generated card {title} at {savepath}!")
    except Exception as e:
        pass
        print(f"An error occurred while generating the image file: {e}")

    try:
        # Crop the image file
        savepath_out = "./new_card_box/{}.png".format(
            re.sub(r"[^\w\s]", "", title).replace(" ", "_")
        ).lower()
        crop_image(savepath, savepath_out, title)
    except Exception as e:
        print(f"An error occurred while cropping the image file: {e}")

    try:
        # Delete the original image file
        os.remove(savepath)
        print(f"Cropped card {title} at {savepath}!")
    except OSError as e:
        print(f"An error occurred while deleting the original image file: {e}")


def run_spell_check_on_cards(nlp):

    with open("ppn_deck.json", "r") as f:
        card_deck = json.load(f)

    for card in tqdm(card_deck):

        summary = card["summary_short"]
        if isinstance(summary, list):
            summary = summary[1]

        doc = nlp(summary)
        if doc._.performed_spellCheck:

            summary = doc._.outcome_spellCheck
            card["summary_short"] = summary
        else:
            print("Spell check was not performed")

tries = 0

def crop_image(input_file, output_file, title):
    # Generate the output file name based on the title argument
    output_file = './new_card_box/{}.png'.format(re.sub(r'[^\w\s]', '', title).replace(' ', '_')).lower()
    # Open the input image
    try:
        img = Image.open(input_file)

        # Crop the image to maintain a 14px buffer on the left, top, bottom, and right
        # of a rectangle that is 1182px wide and 1779px tall, starting from the upper left
        left = 14 # buffer
        cropped_img = img.crop((left, 14, 1182+left, 1779+left))

        # Save the cropped image to the specified output file
        cropped_img.save(output_file)

    except Exception as e:
        print(f"An error occurred while cropping image {input_file}: {e}")




def generate_physical_cards(options, html_template):
    print(f"Generating physical cards...")
    print(f"With the following options: {options}")
    print("--" * 20)
    print(
        f"Gandalf is automatically adding keywords for the 2018-2022 years to the deck."
    )


    profanity = options["profanity"]
    grade_level = options["grade_level"]
    keywords = options["keywords"]
    for year in range(2018, 2023):
        keywords.append(str(year))

    with open("ppn_deck.json", "r") as f:
        card_deck = json.load(f)
    cards_to_generate = len(card_deck)
    card_deck = random.sample(card_deck, cards_to_generate)

    for card in tqdm(card_deck):
        if gandalf_card_finder(card, keywords, grade_level, profanity=False):
            pass
        else:
            continue

        summary = card["summary"]
        summary = str(summary)

        if isinstance(summary, str):

            sentence_count = 5
            iterator = 1
            summary = summarize_text(summary, 3)
            if isinstance(summary, list):
                summary = " ".join(summary)
        else:
            raise ValueError("Summary is not a string!")
        card["final_summary"] = summary

        try:
            card["category"] = [keyword for keyword in keywords if keyword in summary][
                0
            ]
        except Exception as e:
            #card["category"] = "other"
            if "category" not in card.keys():
                card["category"] = "other"
            else:
                #todo predict the category with nltk on title
                category = str(card["category"]) if card['category'] != None else "Wild Card"
                pass


        category = card["category"]

        points = card["points_for_card"]

        generate_card(
            str(card["title"]),
            summary,
            points=points,
            html_template=html_template,
            name=str(card["title"]),
            links_on_wikipedia=card["related"],
            category=category,
        )


def gandalf_card_finder(card, keywords, grade_level, profanity):

    #!assert ("summary" in card.keys(), "Card does not have a summary!")
    full_summary = card["summary"]
    if isinstance(full_summary, list):
        full_summary = full_summary[1]

    found_keyword = False
    for keyword in keywords:
        if re.search(r"\b" + keyword + r"\b", full_summary, re.IGNORECASE):

            found_keyword = True
            break
        else:

            found_keyword = False

    profanity = False

    grade_level_check = True
    if 'grade_level' not in card.keys():
        #grade_level_check = False
        print(f"Card {card['title']} does not have a grade level!")
        # calculate the grade level of the summary
        card['grade_level'] = textstat.flesch_kincaid_grade(full_summary)
        print(f"Card {card['title']} has a grade level of {card['grade_level']}!")

    if float(card["grade_level"]) > float(grade_level):
        grade_level_check = False

    if (found_keyword and grade_level_check) or grade_level_check:
        return True
    else:
        return False


def clean_string(string):

    string = re.sub(r"(?<=[.!?])\s*[^a-zA-Z\d]", "", string)

    corrected_string = string

    corrected_string = str(corrected_string)
    description = corrected_string
    description = re.sub(r"\.(?=[^ ])", ". ", description)
    description = re.sub(r",(?=[^ ])", ", ", description)
    description = re.sub(r";(?=[^ ])", "; ", description)
    description = re.sub(r":(?=[^ ])", ": ", description)
    description = re.sub(r"\?(?=[^ ])", "? ", description)
    description = re.sub(r"!(?=[^ ])", "! ", description)
    description = re.sub(r"-(?=[^ ])", "- ", description)
    description = re.sub(r'"(?=[^ ])', '" ', description)
    description = re.sub(r"'(?=[^ ])", "' ", description)
    description = re.sub(r"\((?=[^ ])", "( ", description)
    description = re.sub(r"\)(?=[^ ])", ") ", description)
    corrected_string = description

    cleaned_string = re.sub(r"[^\x00-\x7F]+", "", corrected_string)

    cleaned_string = cleaned_string.replace("\n", " ")

    cleaned_string = cleaned_string.capitalize()

    cleaned_string = re.sub(r"[\.\?\!]\s(?=[a-z])", ". ", cleaned_string)

    #!assert (len(cleaned_string) > 0, "Cleaned string is empty!")
    return cleaned_string


def run_cleaner_on_cards():

    with open("ppn_deck.json", "r") as f:
        card_deck = json.load(f)

    for card in tqdm(card_deck):

        if "cleaned" in card.keys():
            continue
        summary = card["summary_short"]
        if isinstance(summary, list):
            summary = summary[1]
        if isinstance(summary, list):
            summary = " ".join(summary)

        summary = str(summary)

        summary = clean_string(summary)

        card["summary_short"] = summary

        card["cleaned"] = True

        if card_deck.index(card) % 10 == 0:

            with open("ppn_deck.json", "w") as f:
                json.dump(card_deck, f)

    with open("ppn_deck.json", "w") as f:
        json.dump(card_deck, f)


def main():
    # templates
    with open("card_html.txt", mode="r",encoding="UTF-8") as f:
        html_template = f.read()
    global spell_check_flag

    print("Initialized, ready to spell check!")

    if spell_check_flag:
        run_cleaner_on_cards()
    print("Spell check complete, ready to generate cards!")
    generate_card(
        "Test Card",
        "from Armentires is an English song that was particularly popular during World War I. It is also known by its ersatz French hook line, Inky Pinky Parlez Vous, or the American variant Hinky Dinky Parlez-vous variant: Parlay voo. Inky Pinky was a Scottish childrens name for parsnip and potato cakes, but it has been suggested that an onomatopoeic reference to the sound of bed springs is a more likely soldiers ribald derivation.",
        10,
        html_template,
        "Mademoiselle from Armentières",
        0,
        "People",
    )
    keywords = [
        "amish",
        "dance",
        "actor",
        "ghost",
        "character",
        "book",
        "movie",
        "funny",
        "famous",
        "viral",
        "dog poop",
        "poop",
        "therapy",
        "vegetables",
        "melon",
        "embarrassing",
    ]
    options = {
        "grade_level": 10,
        "profanity": False, # set to true to allow profanity
        "cards_to_generate": 5000,
        "keywords": keywords,
        "categories": [],
    }
    generate_physical_cards(options, html_template)
    print("Done")

# main function
if __name__ == "__main__":
    main()