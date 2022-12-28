import wikipedia
import re
import random
import requests
import urllib

def get_random_page_url(categories, category_sample_size):
    base_url = "https://randomincategory.toolforge.org/Random_page_in_category?"
    for i, cat in enumerate(categories):
        base_url += f"&category{i}={urllib.parse.quote(str(cat).lower())}"
    base_url += "&server=en.wikipedia.org&cmnamespace=0&cmtype=page&returntype="
    return base_url

from bs4 import BeautifulSoup

def get_page_title_and_summary(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string.replace(" - Wikipedia", "").replace("Wiki", "")
    summary = soup.find('p').text
    return title, summary


def get_random_wiki_entry_dict(original_categories, category_sample_size):
    while True:
        categories = random.sample(original_categories, category_sample_size)
        random_page_url = get_random_page_url(categories, category_sample_size)
        response = requests.get(random_page_url)
        redirected_url = response.url
        html = response.text
        title, summary = get_page_title_and_summary(html)
        if redirected_url == "https://randomincategory.toolforge.org/":
            continue
        else:
            break
    return {"title": title, "summary": summary}
def get_random_wiki_entries_dict(original_categories, category_sample_size, num_entries):
    entries = []
    for _ in range(num_entries):
        entry = get_random_wiki_entry_dict(original_categories, category_sample_size)
        entries.append(entry)

def main():
    original_categories = ["Technology", "Arts", "Geography"]
    category_sample_size = 2
    num_entries = 5
    entries = get_random_wiki_entries_dict(original_categories, category_sample_size, num_entries)
    print(entries)



if __name__ == "__main__":
    main()
