import json
import textwrap
import random
from tqdm import tqdm
from icecream import ic
# PlaintextParser
from sumy.parsers.plaintext import PlaintextParser

# LexRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# LsaSummarizer

# define Tokenizer
from sumy.nlp.tokenizers import Tokenizer

# define Stemmer



import os
from PIL import Image, ImageDraw, ImageFont
import time
# with open("ppn_deck_cleaned.json", "w") as write_file:
#     json.dump(card_deck, write_file, indent=4)

# read card_deck from ppn_deck.json file
# with open("ppn_deck.json", "r") as read_file:
# card_deck = json.load(read_file)
with open("ppn_deck.json", "r") as read_file:
    card_deck = json.load(read_file)

# # clear the card_images folder
# print("Clearing card_images folder...")
# for filename in os.listdir("card_box"):
#     os.remove(os.path.join("card_box", filename))
import textstat

def determine_grade_level(summary):
    """
    determine_grade_level - generates a grade level for the given summary using the Flesch-Kincaid Grade Level formula

    The Flesch-Kincaid Grade Level formula is a readability test designed to indicate how difficult a passage in English is to understand. The score is based on the average number of syllables per 100 words and the average number of words per sentence. The higher the score, the more difficult the text is to understand.

    :param summary: _description_
    :type summary: _type_
    :return: _description_
    :rtype: float
    """
    grade_level = textstat.flesch_kincaid_grade(summary)
    return grade_level

# Example usage
card_summary = "The quick brown fox jumps over the lazy dog."
grade_level = determine_grade_level(card_summary)
print(grade_level) # prints "4.9"


def summarize_text(text, num_sentences):
    """
    Summarize the given text using the LSA or LexRank summarization algorithms and return the summary as a string
    """
    try:
        # create a PlaintextParser object to parse the text
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        # choose a summarization algorithm
        # algorithm = LsaSummarizer()
        algorithm = LexRankSummarizer()

        # summarize the text and return the summary as a string
        summary = algorithm(parser.document, num_sentences)
        summary_text = "\n".join([str(sentence) for sentence in summary])
    except:
        #ic()
        summary_text = "No summary available"
    return summary_text


def generate_card(title, definition, points, name=None):
    ic(title)
    #ic()
    # create a blank image
    # ^print(f'creating: {title}')
    # ignore Theo Carver

    # add checks to make sure title and defition are both not empty and not longer than 40 characters * 25 lines (1000 characters). If they are, raise an error, also if either are None raise an error
    #print(f'title length: {len(title)}, definition length: {len(definition)}')
    #* It isn't related to the length of title, or description
    if 'diltondoiley' in title:
        #ic()
        # skip Dilton Doiley
        return
    if title == None or definition == None:
        raise ValueError("Title and definition cannot be None")
    if len(title) > 1000 or len(definition) > 1000:
        raise ValueError("Title and definition cannot be longer than 1000 characters")
    try:
        # create a blank image
        image = Image.new("RGB", (550, 850), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        # set font sizes and create font objects
        title_font_size = 20
        description_font_size = 20
        points_font_size = 18
        title_font = ImageFont.truetype("./fonts/SFNSMono.ttf", title_font_size)
        description_font = ImageFont.truetype("./fonts/SFNSMono.ttf", description_font_size)
        points_font = ImageFont.truetype("./fonts/SFNSMono.ttf", points_font_size)

        # wrap the title and definition to 40 characters
        title_wrapped = textwrap.wrap(title, width=40)
        definition_wrapped = textwrap.wrap(definition, width=40)

        # calculate the heights of the title and definition text areas
        title_height = len(title_wrapped) * title_font_size
        description_height = len(definition_wrapped) * description_font_size

        # draw the title and definition text areas
        draw.rectangle([(10, 10), (540, 10 + title_height)], fill="lightblue")
        draw.rectangle([(10, 30 + title_height), (540, 30 + title_height + description_height)], fill="white")

        # write the title and definition text
        y_text = 20
        for line in title_wrapped:
            draw.text((270, y_text), line, fill=(0, 0, 0), font=title_font, anchor="mm")
        y_text += title_font_size
        y_text = 30 + title_height
        for line in definition_wrapped:
            draw.text((10, y_text), line, fill=(0, 0, 0), font=description_font, anchor="lm")
            y_text += 20

        # draw the points text area at the bottom left corner of the card
        draw.rectangle([(10, 830), (100, 850)], fill="lightgreen")

        # write the points text
        draw.text((55, 840), str(points), fill=(0, 0, 0), font=points_font, anchor="mm")

        # if a name is provided, write it in the bottom right corner
        if name:
            draw.text((540, 830), name, fill=(0, 0, 0), font=points_font, anchor="mm")

        # save the image
        title = title.replace(" ", "_").lower()
        # remove any non-alphanumeric characters
        title = "".join([char for char in title if char.isalnum() or char == " "]).rstrip()
        # save the image
        try:
            image.save(f"card_box/{title}.png")
            #ic()
        except Exception as e:
            #ic()
            print(e)
            #ic()
            print("Error saving card:", title)
            #ic()
    except:
        ic('error generating card')
        #ic()
        print("Error generating card for:", title)


def generate_physical_cards():
    #ic()
    # choose a random card from the card deck
    card = random.choice(card_deck)
    print(card)

    # get the summary for the card
    summary = (
        card["summary"][1] if isinstance(card["summary"], list) else card["summary"]
    )

    # summarize the summary if it is a string, or convert it to a string if it is a list
    if isinstance(summary, str):
        summary = summarize_text(summary, 2)
    if isinstance(summary, list):
        summary = " ".join(summary)

    # calculate the points for the card
    points = card["point_value"] if "point_value" in card else 1

    # generate the card image
    generate_card(str(card["title"]), summary, points=points)

    # shuffle the card deck
    random.shuffle(card_deck)
    print("checking for nan values")
    start_time = time.time() # start the timer
    for card in tqdm(card_deck):
        if card["summary_clean"] == "nan" or card["summary_clean"] == None or type(card["summary_clean"]) == float:
            card["summary_clean"] = ""
        # if the summary_short is longer than 1000 characters, truncate it to 1000 characters
        if len(card["summary_clean"]) > 1000:
            card["summary_clean"] = card["summary_clean"][:1000]
            #!ic(card['title'])
            print(f'card summary too long: {len(card["summary_clean"])}')
    # iterate through the card deck and generate card images for each card

    while True:
        # choose a random 100 cards from the card deck
        #ic()
        subdeck = random.sample(card_deck, 100)
        for card in tqdm(subdeck):
            #!ic(card)
            # if the card does not already exist in the card box, generate it
            try:
                if not os.path.exists(
                    f"card_box/{card['title'].replace(' ', '_').lower()}.png"
                ):
                    # get the title and summary for the card
                    title = card["title"]
                    summary = (
                        card["summary"][1]
                        if isinstance(card["summary"], list)
                        else card["summary"]
                    )
                    sentence_count = 5
                    # summarize the summary if it is a string, or convert it to a string if it is a list
                    if isinstance(summary, str):
                        # if the summarized text fills more than 3/4 the height of the card, summarize it again with one fewer sentence. This is to prevent the text from overflowing the card.
                        # max at font size 20
                        while len(summary) > 25 * 40:  # and sentence_count > 1:
                            summary = summarize_text(summary, 1)
                            sentence_count -= 1
                    if isinstance(summary, list):
                        summary = " ".join(summary)

                    # calculate the points for the card
                    points = card["point_value"]

                    # if not os.path.exists(f"card_box/{card['title'].replace(' ', '_').lower()}.png"):
                    generate_card(title, summary, points=points)
                else:
                    print(f"Card for {card['title']} already exists")
            except Exception as e:
                print(f"Error generating card for {card['title']}: {e}")
        # if the total seconds in the inner loop is more than 1 minute (60 seconds), break the loop and start over
        if (
            time.time() - start_time > 3600 or len(os.listdir("card_box")) == len(card_deck)
        ):
            break

    print("Done generating physical cards")

print("Initialized process, and ready to generate physical cards...")


generate_physical_cards()
print("Done")
