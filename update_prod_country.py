import requests
import re

URL = "https://en.wikipedia.org/w/api.php"
HEADERS = {
    "User-Agent": "MovieDataScript/1.0"
}

def get_best_wiki_page(name):
    """
    Search Wikipedia and return the best page
    """
    params = {
        "action": "query",
        "list": "search",
        "srsearch": name+ " film", 
        "format": "json"
    }

    r = requests.get(URL, params=params, headers=HEADERS)
    info = r.json()

    if info["query"]["search"]:
        return info["query"]["search"][0]["title"]
    return None


def get_raw_wiki(name):
    """
    Get the raw wikitext of the film's Wikipedia page.
    """
    params = {
        "action": "query",
        "prop": "revisions",
        "titles": name,
        "rvslots": "main",
        "rvprop": "content",
        "format": "json",
        "formatversion": 2
    }

    r = requests.get(URL, params=params, headers=HEADERS)
    raw = r.json()

    pages = raw.get("query", {}).get("pages", [])
    if not pages or "revisions" not in pages[0]:
        return None
    return pages[0]["revisions"][0]["slots"]["main"]["content"]
    
def clean_infobox(text):
    """
    Clean and extract the first useful entry from malformed infobox content
    """
    # Remove <ref>...</ref>
    text = re.sub("<ref.*?</ref>", "", text, flags=re.DOTALL)

    # Try to extract bullet list items (e.g., * English)
    bullet_items = re.findall("\*\s*(.+)", text)
    if bullet_items:
        # Clean brackets like [[...]] and strip
        return re.sub("\[\[|\]\]", "", bullet_items[0]).strip()

    # Fallback: clean brackets and templates
    text = re.sub("\{\{.*?\}\}", "", text, flags=re.DOTALL)
    text = re.sub("\[\[|\]\]", "", text)
    text = re.sub("\[.*?\]", "", text)
    return text.strip()

def get_prod_country(wikitext):
    """
    Extract production country and language from Wikipedia API
    """
    country = None
    country_match = re.search("\|\s*country\s*=\s*([\s\S]+?)(?:\n\||\n\})", 
                              wikitext, re.IGNORECASE)
    if country_match:
        country = clean_infobox(country_match.group(1))

    return country

# Test
title = "Oppenheimer"
wiki_pg = get_best_wiki_page(title)
wiki_text = get_raw_wiki(wiki_pg)
country = get_prod_country(wiki_text)
print(country)

