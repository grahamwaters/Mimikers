# Define a function that takes a list of cards and a player, and sends them the batch of cards
def send_cards(cards, player):
    # Send the batch of cards to the player
    # Replace this with your code for sending the cards
    print(f"Sending {cards} to {player}")

# Define a list of players
players = ['player1', 'player2', 'player3']

# Define a list of cards
cards = ['card1', 'card2', 'card3', 'card4', 'card5', 'card6', 'card7', 'card8', 'card9', 'card10', 'card11', 'card12', 'card13', 'card14', 'card15']

# Iterate through the list of players, and send them a batch of 10 cards
for player in players:
    # Get the next batch of 10 cards
    batch = cards[:10]

    # Send the batch of cards to the player
    send_cards(batch, player)

    # Remove the sent cards from the list
    cards = cards[10:]


# Define a function that takes a player, and asks them to select their five cards
def select_cards(player):
    # Ask the player to select their five cards
    # Replace this with your code for asking the player to select their cards
    selected_cards = ['card1', 'card2', 'card3', 'card4', 'card5']

    # Return the selected cards
    return selected_cards

# Define a list of players
players = ['player1', 'player2', 'player3']

# Create an empty list to store the selected cards
selected_cards = []

# Iterate through the list of players, and ask them to select their five cards
for player in players:
    # Ask the player to select their five cards
    player_selected_cards = select_cards(player)

# Add the player's selected cards to the list of selected cards
selected_cards += player_selected_cards

# Print the list of selected cards
print(selected_cards)




import requests

# Replace :bot_id with your bot's ID
bot_id = "c9d6f93a4e96eeadbeaf21feef"

# Set the base URL for the GroupMe API
base_url = "https://api.groupme.com/v3"

# Set the payload for the request to the GroupMe API
# This payload will send a message to the group with the list of cards
payload = {
    "bot_id": bot_id,
    "text": "Here are your cards: [Card 1, Card 2, Card 3, Card 4, Card 5, Card 6, Card 7, Card 8, Card 9, Card 10]"
}

# Make the POST request to the GroupMe API to send the message
response = requests.post(f"{base_url}/bots/post", json=payload)

# Check the status code of the response
if response.status_code != 202:
    print(f"Failed to send message: {response.status_code} {response.text}")
else:
    print("Message sent successfully.")
