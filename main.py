import requests
import csv
import time

# === CONFIG ===
OMDB_API_KEY = "86651dbf"
OMDB_URL = "http://www.omdbapi.com/"
INPUT_CSV = "movies_en_90-25.csv"
OUTPUT_CSV = "english_movies_1990_2025.csv"

# === READ MOVIE TITLES FROM CSV ===
movie_titles = []
with open(INPUT_CSV, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        title = row.get("title")  # <-- lowercase 'title' here
        if title:
            movie_titles.append(title.strip())

print(f"Loaded {len(movie_titles)} movie titles from {INPUT_CSV}")

# === FUNCTION TO FETCH MOVIE DATA ===
def get_movie_info(title):
    params = {
        "apikey": OMDB_API_KEY,
        "t": title,
        "type": "movie"
    }
    try:
        response = requests.get(OMDB_URL, params=params)
        data = response.json()
        if data.get("Response") == "True":
            language = data.get("Language", "")
            year = data.get("Year", "")
            release_date = data.get("Released", "")
            budget = data.get("BoxOffice", "N/A")

            if "English" in language and year.isdigit() and 1990 <= int(year) <= 2025:
                return {
                    "Title": data.get("Title", ""),
                    "Year": year,
                    "Released": release_date,
                    "Budget": budget,
                    "Language": language
                }
        return None
    except Exception as e:
        print(f"Error fetching {title}: {e}")
        return None

# === MAIN SCRIPT ===
movies_data = []
for i, title in enumerate(movie_titles, start=1):
    info = get_movie_info(title)
    if info:
        movies_data.append(info)
        print(f"[{i}/{len(movie_titles)}] Fetched: {info['Title']} ({info['Year']})")
    else:
        print(f"[{i}/{len(movie_titles)}] Skipped: {title}")
    time.sleep(1)  # pause to avoid rate limiting

# === SAVE TO CSV ===
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Title", "Year", "Released", "Budget", "Language"])
    writer.writeheader()
    writer.writerows(movies_data)

print(f"\n✅ Saved {len(movies_data)} movies to {OUTPUT_CSV}")
