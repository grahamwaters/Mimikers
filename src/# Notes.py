# Notes

While the loop runs do the following:

1. First, it creates an empty list called "related_pages" to store the related pages.
2. Then, it loops through the card deck and for each card...
3. It calls the get_related_pages function and passes the card's title as an argument.
4. The get_related_pages function returns a list of dictionaries, so we can loop through the list and for each dictionary...
5. We extract the title key and append it to the "related_pages" list.
6. Then, we call the generate_related_deck function and pass the "related_pages" list as an argument.
7. The generate_related_deck function returns a list of dictionaries, so we can loop through the list and for each dictionary...
8. We extract the title key and append it to the "card_deck" list.
9. Finally, we return the "card_deck" list.