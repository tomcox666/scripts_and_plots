import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_albums_for_current_month():
    url = "https://en.wikipedia.org/wiki/List_of_2024_albums"
    response = requests.get(url)
    albums = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        current_month = datetime.now().strftime("%B")  # Get the current month's name
        tables = soup.find_all('table', class_='wikitable')

    for table in tables:
        if current_month in table.find('caption').text:
            rows = table.find_all('tr')
            for row in rows[2:]:
                columns = row.find_all('td')
                artist = columns[0].text.strip()
                album = columns[1].text.strip()
                albums.append((artist, album))

    return albums

# Example usage:
albums_this_month = get_albums_for_current_month()
for artist, album in albums_this_month:
    print(f"Artist: {artist}, Album: {album}")