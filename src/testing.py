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
