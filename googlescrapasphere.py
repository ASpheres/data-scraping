import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Initialize the web driver
driver = webdriver.Chrome()

# Define the base URL
base_url = "https://www.google.com/search?q=site:linkedin.com/in+%2B+CEO+%2B+%22%40gmail.com%22+%2B+%22phone+number%22+%2B+%22France%22&rlz=1C1CHBD_enIN1017IN1017&sxsrf=AJOqlzV0v-xdHVpmgOcayozsKspn4eqpQw:1676035816656&ei=6EbmY5ncJ8STkdUPjIeoIA&start={}&sa=N&ved=2ahUKEwiZ8O37h4v9AhXESaQEHYwDCgQ4FBDy0wN6BAgCEAQ&cshid=1676035833639607&biw=1366&bih=625&dpr=1"

# Initialize an empty list to store the company information
data = []

# Scrape data from 10 pages
for page in range(0, 8):
    # Calculate the start parameter for the current page
    start = page * 10

    # Navigate to the website
    url = base_url.format(start)
    driver.get(url)

    # Wait for 10 seconds for the page to load
    time.sleep(20)

    # Parse the HTML content of the page
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find the elements that contain the company information
    data_elements = soup.find_all("div", class_="g")

    # Extract the information for each company
    for data_element in data_elements:
        title = data_element.find("h3", class_='LC20lb').text
        type1 = data_element.find("div", class_='IsZvec')
        contact_email = type1.find('span').text if type1 else None
        type2 = data_element.find("div", class_='lyLwlc')
        contact_tel = type2.find('span').text if type2 else None
        data.append({
            "title": title,
            "contact_email": contact_email,
            "contact_tel": contact_tel,
        })

# Save the information to a CSV file
with open("data4.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "contact_email", "contact_tel"])
    writer.writeheader()
    for data_element in data:
        writer.writerow(data_element)

# Close the web driver
driver.quit()
