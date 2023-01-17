import nltk
from nltk.corpus import stopwords
from sklearn.preprocessing import MinMaxScaler

import json

import pandas as pd
from nltk.corpus import stopwords
from sklearn.preprocessing import MinMaxScaler

english_stopwords = stopwords.words('english')
stopwords = set(english_stopwords)
import json

import pandas as pd
from nltk.corpus import stopwords
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm

# read card_deck from ppn_deck.json file
with open("ppn_deck.json", "r") as read_file:
    card_deck = json.load(read_file)

# Now assign points based on the related column but scale it with MinMaxScaler
# card_deck = revise_point_values(card_deck, max_points=50)
scaler = MinMaxScaler(feature_range=(0, 20))
# read card_deck from ppn_deck.json file
with open("ppn_deck.json", "r") as read_file:
    card_deck = json.load(read_file)
# Now assign points based on the related column but scale it with MinMaxScaler
card_deck = revise_point_values(card_deck, max_points=50)



with open("ppn_deck.json", "r") as read_file:
    card_deck = json.load(read_file)

def revise_point_values(card_deck, max_points=20):
    stop_words = stopwords.words("english")
    card_id = 0
    related_words = []
    for card in card_deck:
        summary_text = card['summary'][1]
        words = summary_text.split()
        nonstop_words = [word for word in words if word not in stop_words]
        word_count = len(nonstop_words)
        try:
            related_words.append(int(card['related']))
        except:
            related_words.append(0)
        card_id += 1
    scaled_word_counts = scaler.fit_transform(pd.DataFrame(related_words))
    card_id = 0
    for card in card_deck:
        try:
            scaled_word_count = scaled_word_counts[card_id]
            related_words = int(card['related'])
            rounded_value = int(scaled_word_count[0])
        except:
            related_words = 0
            rounded_value = 0
        try:
            card['point_value'] = max(rounded_value, related_words)
        except Exception:
            pass
        card_id += 1
    return card_deck

card_deck = revise_point_values(card_deck, max_points=50)


# the summary_short needs to always be the second element in the tuple if it is an instance of a tuple, else it is itself (str)
for card in card_deck:
    summary = card['summary']
    if isinstance(summary, tuple) or isinstance(summary, list):
        summary_short = summary[1]
    else:
        summary_short = summary
    card['summary_short'] = summary_short
    card['summary'] = summary_short

df = pd.DataFrame(card_deck)


# revise point values
card_deck = revise_point_values(card_deck,20)


# the point_value must always be a value from 1 to 10 never 0. Replace all 0's with 1's
df['point_value'] = df['point_value'].replace(0,1)


# now save the df as a json file
card_deck = df.to_dict('records')
with open("ppn_deck.json", "w") as write_file:
    json.dump(card_deck, write_file)
