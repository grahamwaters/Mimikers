from html2image import Html2Image

def generate_card(title: str, description: str, points: str) -> None:
    # Create the HTML content for the card
    # The card is 550x850 pixels
    # read the template file from the current directory 'card_html.txt'
    with open('card_html.txt', 'r') as f:
        html = f.read()
    # replace the placeholders with the actual values
    html = html.replace('Card Title', title)
    html = html.replace('Card Description', description)
    html = html.replace('Point Value', points)
    space_to_fill = str(850 - len(description) - 100)
    html = html.replace('MIDDLE_HEIGHT',space_to_fill)
    # create blank lines to fill the space
    Middle_Content = ' '*int(space_to_fill)
    html = html.replace('Middle Content',Middle_Content)

    # Create an Html2Image object
    hti = Html2Image()

    # Generate a screenshot of the HTML content and save it to a file
    hti.screenshot(html_str=html, save_as='card.png')

# Example usage
# generate_card('Card Title', 'Card Description', '10 Points')

title = 'Tarzan yell'
description = 'Tarzan yell, The Tarzan yell or Tarzans jungle call is the distinctive, ululating yell of the character Tarzan as portrayed by actor Johnny Weissmuller in the films based on the character created by Edgar Rice Burroughs starting with Tarzan the Ape Man 1932. The yell was a creation of the movies based on what Burroughs described in his books as simply the victory cry of the bull ape.'
points = '10 Points'

generate_card(title, description, points)