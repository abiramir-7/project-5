from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Initialize Chrome Driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL for IMDb 2024 Feature Films
url = "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31"
driver.get(url)
time.sleep(5) # Allow page to load

movies = []

# Locate movie containers (Note: IMDb selectors may change, update if needed)
items = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item")

for item in items:
    try:
        name = item.find_element(By.CLASS_NAME, "ipc-title__text").text
        # Clicking or finding the plot summary/storyline
        storyline = item.find_element(By.CLASS_NAME, "ipc-html-content-inner-div").text
        movies.append({"Movie Name": name, "Storyline": storyline})
    except:
        continue

# Save to CSV as required [cite: 18, 21]
df = pd.DataFrame(movies)
df.to_csv("movies_2024.csv", index=False)
driver.quit()
print("Scraping Complete. Data saved to movies_2024.csv")