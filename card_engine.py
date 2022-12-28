import json
import os
import random
import re
from html2image import Html2Image
from tqdm import tqdm
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer
from icecream import ic

def summarize_text(text, num_sentences):
    ic()
    """
    Summarize the given text using the LSA or LexRank summarization algorithms and return the summary as a string
    """

    parser = PlaintextParser.from_string(text, Tokenizer("english"))

    algorithm = LexRankSummarizer()

    summary = algorithm(parser.document, num_sentences)
    summary_text = "\n".join([str(sentence) for sentence in summary])
    return summary_text


def generate_card(
    title: str,
    description: str,
    points: str,
    html_template: str,
    name: str,
    links_on_wikipedia: str,
    category="Wild Card",
):
    filename = "{}.png".format(title.replace(" ", "_"))
    if os.path.exists("./card_box/{}".format(filename)) and "Test_Card" not in filename:
        print(f"Card {title} already exists, skipping...")
        return
    width_cm = 5.5
    height_cm = 8.5
    card_color = "green"
    width_pixels = int(width_cm * 96)
    height_pixels = int(height_cm * 96)
    points = int(points)
    points = str(points)
    links_on_wikipedia = str(links_on_wikipedia)
    html = html_template
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
    description = description.replace(" - ", " ")

    while "  " in description:
        description = description.replace("  ", " ")
    description = clean_string(description)
    ic()
    assert (len(description) > 0, "There is no Description")
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
    savepath = os.path.join(output_path, filename)
    hti.output_path = output_path

    filename = "{}.png".format(re.sub(r"[^\w\s]", "", title).replace(" ", "_"))
    filename = filename.lower()
    hti.screenshot(html_str=html, save_as=filename)

    print(f"Generated card {title} at {savepath}!")
    savepath_out = "./new_card_box/{}.png".format(
        re.sub(r"[^\w\s]", "", title).replace(" ", "_")
    ).lower()
    crop_image(savepath, savepath_out, title)

    os.remove(savepath)
    print(f"Cropped card {title} at {savepath}!")


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


def generate_physical_cards(options):
    print(f"Generating physical cards...")
    print(f"With the following options: {options}")
    print("--" * 20)

    cards_to_generate = options["cards_to_generate"]
    profanity = options["profanity"]
    grade_level = options["grade_level"]
    keywords = options["keywords"]

    with open("ppn_deck.json", "r") as f:
        card_deck = json.load(f)

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
        except IndexError:
            card["category"] = "other"
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

    print(
        f"Gandalf is automatically adding keywords for the 2018-2022 years to the deck."
    )
    for year in range(2018, 2023):
        keywords.append(str(year))
    assert ("summary" in card.keys(), "Card does not have a summary!")
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

    assert (len(cleaned_string) > 0, "Cleaned string is empty!")
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
    "nasa",
    "famous",
    "viral",
    "dog poop",
    "poop",
    "therapy",
    "vegetables",
    "melon",
    "die",
    "embarrassing",
]
options = {
    "grade_level": 16,
    "profanity": True,
    "cards_to_generate": 100,
    "keywords": keywords,
    "categories": [],
}
generate_physical_cards(options)
print("Done")
