import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urljoin  # Import for proper URL joining

def get_random_lyrics():
    base_url = "https://lyrics.github.io/"

    # Fetch the main page
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Select a random letter
    letter_links = soup.select("nav a")
    if not letter_links:
        print("No letter links found.")
        return

    random_letter_link = random.choice(letter_links)
    letter_url = urljoin(base_url, random_letter_link["href"])  # Use urljoin for correct URL

    # Fetch the letter page
    response = requests.get(letter_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Select a random band (and so on for album and song)
    links = soup.select("ul li a")
    if not links:
        print("No links found on this page.")
        return

    random_link = random.choice(links)
    next_url = urljoin(letter_url, random_link["href"])

    # Repeat for album and song
    for _ in range(2):  # Two more levels to navigate
        response = requests.get(next_url)
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.select("ul li a")
        if not links:
            print("No links found on this page.")
            return
        random_link = random.choice(links)
        next_url = urljoin(next_url, random_link["href"])

    # Fetch the song page
    response = requests.get(next_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract and print the first five lines of lyrics
    lyrics_element = soup.select_one("#lyrics")
    if lyrics_element:
        lyrics = lyrics_element.get_text().splitlines()[:5]
        for line in lyrics:
            print(line)
    else:
        print("Lyrics not found on the page.")

# Call the function to run it
get_random_lyrics()