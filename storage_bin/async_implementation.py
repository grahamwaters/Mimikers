import wikipediaapi
import re
import aiohttp
import asyncio

async def get_random_page_url(categories, category_sample_size):
    base_url = "https://randomincategory.toolforge.org/Random_page_in_category?"
    for i, cat in enumerate(categories):
        base_url += f"&category{i}={urllib.parse.quote(str(cat).lower())}"
    base_url += "&server=en.wikipedia.org&cmnamespace=0&cmtype=page&returntype="
    return base_url

async def get_page_title_and_summary(html):
    title_regex = r"<title>(.+?)</title>"
    title_match = re.search(title_regex, html)
    title = title_match.group(1)
    title = title.replace(" - Wikipedia", "").replace("Wiki", "")
    summary_regex = r"<p>(.+?)</p>"
    summary_match = re.search(summary_regex, html)
    summary = summary_match.group(1)
    return title, summary

async def get_random_wiki_entry_dict(original_categories, category_sample_size):
    async with aiohttp.ClientSession() as session:
        while True:
            categories = random.sample(original_categories, category_sample_size)
            random_page_url = await get_random_page_url(categories, category_sample_size)
            async with session.get(random_page_url) as response:
                redirected_url = response.url
                html = await response.text()
                title, summary = await get_page_title_and_summary(html)
                if redirected_url == "https://randomincategory.toolforge.org/":
                    continue
                else:
                    break
        return {"title": title, "summary": summary}

async def get_random_wiki_entries_dict(original_categories, category_sample_size, num_entries):
    entries = []
    for _ in range(num_entries):
        entry = await get_random_wiki_entry_dict(original_categories, category_sample_size)
        entries.append(entry)
    return entries

async def main():
    original_categories = ["Technology", "Arts", "Geography"]
    category_sample_size = 2
    num_entries = 5
    entries = await get_random_wiki_entries_dict(original_categories, category_sample_size, num_entries)
    print(entries)

if __name__ == "__main__":
    asyncio.run(main())
