import re
import json
import nltk
from tqdm import tqdm

# read in the cards and their descriptions
# with open("ppn_deck_cleaned.json", "w") as write_file:
#     json.dump(card_deck, write_file, indent=4)

# read card_deck from ppn_deck.json file
with open("ppn_deck.json", "r") as read_file:
    card_deck = json.load(read_file)

for card in tqdm(card_deck):
    # in the card['summary'] which is found in card['summary'][1] there should be a string that looks like this: "example summary text for a card that has a clue in it".
    # the card['title'] is the title of the card, and it may be something like "Eragon" or "The Hobbit".
    # These words (Eragon, The, Hobbit) are the clues that we want to hide in the summary because they give away the answer to the card. Usually the cards mention the words at least once, towards the beginning of the summary.
    # We want to hide the clues in the summary so that the user can quickly read the summary like catchphrase and try to get others to guess the card title without using any of the (nonstopwords) words in the title of the card.

    # first, we need to get the title of the card and split it into a list of words
    card_title = card['title']

    # Now, remove any exact matches of the card title phrase from the summary phrase before we split the summary phrase into a list of words.
    # This is because the card title phrase may be a substring of the summary phrase, and we don't want to remove the substring from the summary phrase.

    # how? we can use the re.sub() function to replace the card title phrase with an empty string in the summary phrase.
    # the re.sub() function takes 3 arguments: the regex pattern to match, the string to replace the match with, and the string to search for the match in.
    regex_pattern = card_title.lower() # the regex pattern to match is the card title phrase
    string_to_replace_with = "" # the string to replace the match with is an empty string
    string_to_search = card['summary'][1].lower() # the string to search for the match in is the summary phrase
    card['summary'][1] = re.sub(regex_pattern, string_to_replace_with, string_to_search) # replace the card title phrase with an empty string in the summary phrase.

    # now split the title of the card into a list of words, and remove any stopwords from the list of words using nltk stopwords
    stopwords = nltk.corpus.stopwords.words('english')
    card_title_words = card_title.split()
    card_title_words = [word for word in card_title_words if word not in stopwords]
    # now we have a list of words that are in the title of the card, but not stopwords. (i.e. Hobbit, Eragon, etc.)
    # if these words appear in the card summary, we want to hide them in the summary by replacing them with the phrase "clue_hider" (or something similar)
    # we can use the re.sub() function to replace the words in the card title with the phrase "clue_hider" in the summary phrase.

    for word in card_title_words: # for every word in the card title
        string_to_replace_with = " ---- "
        regex_pattern = r'\b' + word + r'\b' # the regex pattern to match is the word
        string_to_search = card['summary'][1].lower()
        card['summary'][1] = re.sub(regex_pattern, string_to_replace_with, string_to_search) # replace the word with the phrase "clue_hider" in the summary phrase.

# save the card_deck to a new file
with open("ppn_deck_cleaned_clues_hidden.json", "w") as write_file:
    json.dump(card_deck, write_file, indent=4)
