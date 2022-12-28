lemmatizing = False
stemming = True
minimum_word_length = 4

# collect cards and store in a list
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm
# Gather all the cards that you want to include in the deck
# read in the ppn_deck.json file
# read in the ppn_deck.json file
import json
import pandas as pd

with open('ppn_deck.json') as f:
    cards = json.load(f)

# cards = [
#     {"title": "Card 1", "text": "This is the text for card 1"},
#     {"title": "Card 2", "text": "This is the text for card 2"},
#     {"title": "Card 3", "text": "This is the text for card 3"},
# ]

# Preprocess the data by removing irrelevant information
processed_cards = []

# Initialize the stemmer and stopwords
stemmer = PorterStemmer()
stopwords = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

for card in tqdm(cards):
    # Tokenize the text
    tokens = nltk.word_tokenize(str(card["summary"]))
    # lemmatize the tokens
    if lemmatizing:
        filtered_tokens = [lemmatizer.lemmatize(t) for t in filtered_tokens]
    # Remove any non-alphabetic characters
    filtered_tokens = [re.sub(r'[^a-zA-Z]', '', t) for t in filtered_tokens]
    # Remove words less than 4 characters long
    filtered_tokens = [t for t in filtered_tokens if len(t) > minimum_word_length]
    # Remove stopwords and stem the remaining words
    if stemming:
        filtered_tokens = [stemmer.stem(t) for t in tokens if t not in stopwords]

    # Store the preprocessed data in a new list
    processed_cards.append({"title": str(card["title"]), "summary": filtered_tokens})

# The processed_cards list now contains the preprocessed data
print(processed_cards[0])


# using the tfidf vectorizer to create a vector for each card from sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
# Create a list of documents
documents = []
for card in processed_cards:
    documents.append(" ".join(card["summary"]))

# print the documents list
print(documents[0])


# Initialize the TfidfVectorizer
vectorizer = TfidfVectorizer()

# Use the fit_transform method to calculate the TF-IDF values for each word
try:
    X = vectorizer.fit_transform(documents)
except ValueError as e:
    print("Error! The vectorizer was unable to process the data")
    print(e)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Cluster the documents using K-Means
km = KMeans(n_clusters=10, random_state=0)
km.fit(X)

# Assign each card to a cluster
clusters = km.labels_.tolist()
for i, cluster in enumerate(clusters):
    cards[i]["cluster"] = cluster

# The cards list now contains the cluster assignment for each card
print(cards[0]) # Print the first 10 cards

df = pd.DataFrame(cards)

# # Get the cluster labels for each card
# cluster_labels = km.labels_

# # Initialize a list to store the top 10 words for each cluster
# top_words = []

# # Iterate over each cluster
# for i in range(10):
#     # Get the indices of the cards in this cluster
#     cluster_indices = [j for j, label in enumerate(cluster_labels) if label == i]

#     # Get the tf-idf values for each word in this cluster
#     cluster_tfidf = X[cluster_indices]

#     # Get the sum of the tf-idf values for each word
#     word_tfidf_sums = cluster_tfidf.sum(axis=0)

#     # Convert the sums to a dense array
#     word_tfidf_sums = cluster_tfidf.sum(axis=0).tolist()[0]

#     # Get the indices of the words with the highest tf-idf values
#     sorted_tfidf_indices = sorted(range(len(word_tfidf_sums)), key=lambda i: word_tfidf_sums[i], reverse=True)

#     # Get the top 10 words
#     top_10_words = [vectorizer.get_feature_names()[i] for i in sorted_tfidf_indices[:10]]

#     # Add the top 10 words to the list
#     top_words.append(top_10_words)


# # Print the top 10 words for each cluster
# for i, top_words in enumerate(top_words):
#     print("Cluster {}: {}".format(i, ", ".join(top_words)))

# Randomly sample the cards from each cluster to add to a new deck of cards that has at most the same number of cards as the smallest cluster
import random
def balance_the_deck_by_cluster(deck_df, num_clusters):
    # Find the smallest cluster
    min_cluster_size = min(df["cluster"].value_counts())
    # Create a new list to store the new deck of cards
    new_deck = []
    # Randomly sample the cards from each cluster
    for cluster in range(num_clusters):
        new_deck.extend(random.sample(list(df[df["cluster"] == cluster].to_dict("records")), min_cluster_size))
    return new_deck # Return the new deck of cards


# Create a new deck of cards that has the same number of cards in each cluster
balanced_deck = balance_the_deck_by_cluster(df,10)
# save the balanced deck to a json file
with open('balanced_deck.json', 'w') as f:
    json.dump(balanced_deck, f)
