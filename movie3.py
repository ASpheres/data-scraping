import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Initialize the web driver
driver = webdriver.Chrome()

# Define the base URL
base_url = "https://www.kaakook.fr/films-{}"

# Initialize an empty list to store the movie information
data = []

# Loop through each alphabet page (A to Z)
for letter in range(0, 26):
    # Convert the index to the corresponding alphabet letter
    alphabet = chr(ord('a') + letter)

    # Navigate to the page for the current alphabet letter
    url = base_url.format(alphabet)
    driver.get(url)

    # Wait for 5 seconds for the page to load
    time.sleep(5)

    # Parse the HTML content of the page
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find the elements that contain the movie information
    liste_elements = soup.find_all("ul", class_="liste")
    if len(liste_elements) < 2:
        continue
    movie_elements = liste_elements[1].find_all("a")

    # Extract the information for each movie
    for movie_element in movie_elements:
        # Navigate to the movie page
        url = movie_element["href"]
        driver.get(url)

        # Wait for 5 seconds for the page to load
        time.sleep(5)

        # Parse the HTML content of the page
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find the elements that contain the movie information
        info_elements = soup.find_all("dl", class_="infos")

        # Extract the information for the movie
        movie_data = {}
        for info_element in info_elements:
            for dt, dd in zip(info_element.find_all("dt"), info_element.find_all("dd")):
                movie_data[dt.text.strip()] = dd.text.strip()
        quote_elements = soup.find_all("header", class_="extrait")[0].find_all("a")
        if len(quote_elements) > 0:
            quotes = "\n".join([quote_element.text.strip() for quote_element in quote_elements])
            movie_data["Répliques du film"] = quotes

        # Add the movie information to the list
        data.append(movie_data)

# Save the information to a CSV file
with open("kaakook_films.csv", "w", newline="", encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Titre", "Réalisé par", "Année de sortie", "Nombre de citations", "Note moyenne des citations", "Publication", "Dernière mise à jour", "Répliques du film"])
    writer.writeheader()
    for movie in data:
        writer.writerow(movie)

# Close the web driver
driver.quit()
