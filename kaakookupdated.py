import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Initialize the web driver
driver = webdriver.Chrome()

# Define the base URL
base_url = "https://www.kaakook.fr/films"

base_url1 = "https://www.kaakook.fr"
# Define the list of alphabets
alphabets = ["", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

# Initialize an empty list to store the movie information
data = []

# Loop through each alphabet and scrape data from each page
for alphabet in alphabets:
    # Navigate to the page for the current alphabet
    url = base_url
    if alphabet:
        url += '-'+alphabet
    driver.get(url)

    # Wait for the page to load
    time.sleep(1)

    # Parse the HTML content of the page
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find the elements that contain the movie information
    movie_elements = soup.find_all("ul", class_='liste')
    #print(movie_elements)
    print(len(movie_elements))
    # Loop through each movie and scrape the data
    for movie_element in movie_elements:
        # Get the URL for the current movie
        #type = movie_element.find("li")
        urlms = soup.select('a')
        movie_url=[urlm['href'] for urlm in urlms]

        #movie_url = type.select('a') if type else None
        #movie_url = movie_element.find("a href")
        print('here',movie_url)
        print(len(movie_url))
        # Navigate to the movie page
         
        for movie_urls in movie_url[34:-12]:
            urlm1 = f"{base_url1}/{movie_urls}"
            driver.get(urlm1)

            # Wait for the page to load
            time.sleep(2)

            # Parse the HTML content of the page
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Find the element that contains the movie information
            quotes = []

            movie_info_element = soup.find("main")
            #print('movie_info',movie_info_element)
            

            # Extract the quotes
            quote_elements = movie_info_element.find_all("blockquote")

            title = movie_info_element.find("h1").text

            for quote_element in quote_elements:
                # Extract the movie title
                
                #type1 = quote_element.find("blockquote")
                quote = quote_element.find('a').text #if type1 else None
                #quote = quote_element.find("a").text
                #quotes.append(quote)

                # Append the movie information to the data list
                data.append({
                    "title": title,
                    "quote": quote,
                })

# Save the information to a CSV file
with open("qmovies.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, delimiter = '*', fieldnames=["title", "quote"])
    writer.writeheader()
    for data_element in data:
        writer.writerow(data_element)

# Close the web driver
driver.quit()
