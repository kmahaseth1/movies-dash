import requests
import re
import sqlite3
import time

# Config
DB = "movies_2020s.db"
TABLE_NAME = "movie_data_raw"
COLUMN_NAME = "production_country2"
BATCH_SIZE = 100
URL = "https://en.wikipedia.org/w/api.php"
HEADERS = {
    "User-Agent": "MovieDataScript/1.0"
}

# Connect to the database
con = sqlite3.connect(DB)
cursor = con.cursor()

# Add column if first time running the script
cursor.execute(f"PRAGMA table_info({TABLE_NAME})")
columns = [row[1] for row in cursor.fetchall()]
if COLUMN_NAME not in columns:
    cursor.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN {COLUMN_NAME} TEXT")
    print(f"Added column '{COLUMN_NAME}' to '{TABLE_NAME}'.")
else:
    print(f"Column '{COLUMN_NAME}' already exists.")

# Helper Functions
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

# Batch process the data
total_processed = 0
while True:
    cursor.execute(
        f"""SELECT name, release_year FROM {TABLE_NAME} 
            WHERE {COLUMN_NAME} IS NULL 
            LIMIT ?""", 
        (BATCH_SIZE,)
    )
    batch = cursor.fetchall()
    if not batch:
        print("All rows processed.")
        break

    for name, release_year in batch:
        try:
            query_string = f"{name} {release_year} film"
            print(f"Processing: {query_string}")

            best_page = get_best_wiki_page(query_string)
            if best_page:
                wikitext = get_raw_wiki(best_page)
                if wikitext:
                    country = get_prod_country(wikitext)
                    if country:
                        cursor.execute(
                            f"""UPDATE {TABLE_NAME} 
                                SET {COLUMN_NAME} = ? 
                                WHERE name = ? AND release_year = ?""",
                            (country, name, release_year)
                        )
                        con.commit()
                        print(f"Updated '{name} ({release_year})' with: {country}")
                    else:
                        cursor.execute(
                            f"""UPDATE {TABLE_NAME} 
                                SET {COLUMN_NAME} = ? 
                                WHERE name = ? AND release_year = ?""",
                            ("Not Found", name, release_year)
                        )
                        con.commit()
                        print(f"No country info found for '{name} ({release_year})'")
                else:
                    cursor.execute(
                            f"""UPDATE {TABLE_NAME} 
                                SET {COLUMN_NAME} = ? 
                                WHERE name = ? AND release_year = ?""",
                            ("No Raw Data", name, release_year)
                        )
                    print(f"No wikitext found for '{name} ({release_year})'")
            else:
                cursor.execute(
                            f"""UPDATE {TABLE_NAME} 
                                SET {COLUMN_NAME} = ? 
                                WHERE name = ? AND release_year = ?""",
                            ("No Page", name, release_year)
                        )
                print(f"No Wikipedia page found for '{name} ({release_year})'")
        except Exception as e:
            print(f"Error processing '{name} ({release_year})': {e}")
        time.sleep(1)  # Respect API rate limits

    total_processed += len(batch)
    print(f"Batch complete. Total processed: {total_processed}\n")

con.close()
print("Done.")