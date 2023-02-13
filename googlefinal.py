import csv
from selenium import webdriver
from bs4 import BeautifulSoup

# Initialize the web driver
driver = webdriver.Chrome()

# Define the base URL
base_url = "https://www.google.com/search?q=site:linkedin.com/in+%2B+CEO+%2B+%22%40gmail.com%22+%2B+%27%27%2B33%27%27+%2B+%22France%22&rlz=1C1CHBD_enIN1017IN1017&sxsrf=AJOqlzV65NLT15lAihbW70yWwG0zxFpHgg:1675852502527&ei=1nrjY9LmH8iIkdUP0eOioAY&start=0&sa=N&ved=2ahUKEwjSqe-I3YX9AhVIRKQEHdGxCGQ4FBDy0wN6BAgEEAQ&biw=1366&bih=625&dpr=1"

# Initialize an empty list to store the company information
contact_info = []

# Scrape data from 25 pages
for page in range(1, 2):
    # Navigate to the website
    url = base_url + str(page)
    driver.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find the elements that contain the company information
    contact_info_elements = soup.find_all("div", class_="v7W49e")

    # Extract the information for each company
    for contact_info_element in contact_info_elements:
        title = contact_info_element.find("h3").text
        email = contact_info_element.find("div", class_ = 'VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf').text
        type = contact_info_element.find("div", class_='VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf')
        tel = type.find('span').text if type else None
        contact_info.append({
            "company_name": title,
            "email": email,
            #"telephone": tel,
        })

# Save the information to a CSV file
with open("resultsg.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["company_name", "email", "telephone"])
    writer.writeheader()
    for info in contact_info:
        writer.writerow(info)

# Close the web driver
driver.quit()
