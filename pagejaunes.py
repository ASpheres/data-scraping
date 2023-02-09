import csv
from selenium import webdriver
from bs4 import BeautifulSoup

# Initialize the web driver
driver = webdriver.Chrome()

# Define the base URL
base_url = "https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui=technicien+informatique&ou=Autour+de+moi&univers=pagesjaunes&idOu=&accuracy=13.787&latitude=48.8213468&longitude=2.3908476&page="

# Initialize an empty list to store the company information
companies = []

# Scrape data from 25 pages
for page in range(1, 26):
    # Navigate to the website
    url = base_url + str(page)
    driver.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find the elements that contain the company information
    company_elements = soup.find_all("li", class_="bi bi-generic")

    # Extract the information for each company
    for company_element in company_elements:
        company_info = company_element.find("span", class_='bi-activity small').text
        company_name = company_element.find("h3").text
        company_address = company_element.find("a", class_='pj-lb pj-link').text
        type = company_element.find("div", class_='number-contact')
        company_tel = type.find('span').text if type else None
        companies.append({
            "company_name": company_name,
            "services": company_info,
            "telephone": company_tel,
            "address": company_address
        })

# Save the information to a CSV file
with open("companies.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["company_name", "services", "telephone", "address"])
    writer.writeheader()
    for company in companies:
        writer.writerow(company)

# Close the web driver
driver.quit()
