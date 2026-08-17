from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time


# ==========================================
# 1. Initialize Chrome Driver
# ==========================================

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

wait = WebDriverWait(driver, 15)


# ==========================================
# 2. IMDb Search URL
# ==========================================

url = (
    "https://www.imdb.com/search/title/"
    "?title_type=feature"
    "&release_date=2024-01-01,2024-12-31"
)

driver.get(url)

movies = []
scraped_names = set()

target_movies = 1000


# ==========================================
# 3. Main Scraping Loop
# ==========================================

while len(movies) < target_movies:

    # --------------------------------------
    # Wait for IMDb movie results
    # --------------------------------------

    try:
        wait.until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "ipc-metadata-list-summary-item")
            )
        )

    except TimeoutException:

        print("\nIMDb is showing a human verification page.")
        print("Please complete the verification manually in Chrome.")

        input(
            "After completing the verification, "
            "press ENTER here to continue..."
        )

        wait.until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "ipc-metadata-list-summary-item")
            )
        )


    # ======================================
    # 4. Get Currently Loaded Movie Cards
    # ======================================

    items = driver.find_elements(
        By.CLASS_NAME,
        "ipc-metadata-list-summary-item"
    )

    print(f"\nMovie cards currently loaded: {len(items)}")


    # ======================================
    # 5. Extract Movie Information
    # ======================================

    for item in items:

        if len(movies) >= target_movies:
            break

        try:

            # Scroll the movie card into view.
            # This helps IMDb render dynamically loaded content.
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                item
            )

            time.sleep(0.05)


            # ----------------------------------
            # Get Movie Name
            # ----------------------------------

            name_element = item.find_element(
                By.CLASS_NAME,
                "ipc-title__text"
            )

            name = name_element.text.strip()

            if ". " in name:
                  name = name.split(". ", 1)[1]


            # Skip if this movie was already processed
            if not name or name in scraped_names:
                continue


            # ----------------------------------
            # Get Storyline
            # ----------------------------------

            storyline_elements = item.find_elements(
                By.CLASS_NAME,
                "ipc-html-content-inner-div"
            )


            # If storyline is not available,
            # skip this movie.
            if not storyline_elements:
                continue


            storyline = storyline_elements[0].text.strip()


            if not storyline:
                continue


            # ----------------------------------
            # Save Movie
            # ----------------------------------

            movies.append({
                "Movie Name": name,
                "Storyline": storyline
            })

            scraped_names.add(name)


            print(
                f"Collected: {len(movies)}/"
                f"{target_movies} - {name}"
            )


        except Exception:
            continue


    # ======================================
    # 6. Check Target
    # ======================================

    if len(movies) >= target_movies:
        break


    # ======================================
    # 7. Find "50 more" Button
    # ======================================

    try:

        load_more = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(., '50 more')]"
                )
            )
        )


        # Scroll to the button
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            load_more
        )

        time.sleep(1)


        # Click the button
        driver.execute_script(
            "arguments[0].click();",
            load_more
        )

        print("Loading 50 more movies...")


        # Give IMDb time to add the new cards
        time.sleep(3)


    except Exception:

        print(
            "\n'50 more' button was not found."
        )

        print(
            "IMDb may have reached the end "
            "of the available results."
        )

        break


# ==========================================
# 8. Keep Exactly Maximum 1000 Movies
# ==========================================

movies = movies[:target_movies]


# ==========================================
# 9. Create DataFrame
# ==========================================

df = pd.DataFrame(movies)


# ==========================================
# 10. Remove Duplicate Movie Names
# ==========================================

df = df.drop_duplicates(
    subset=["Movie Name"]
)


# ==========================================
# 11. Save CSV
# ==========================================

df.to_csv(
    "movies_2024.csv",
    index=False
)


# ==========================================
# 12. Close Browser
# ==========================================

driver.quit()


# ==========================================
# 13. Final Report
# ==========================================

print("\n================================")
print("Scraping Complete!")
print(f"Total movies collected: {len(df)}")
print("Data saved to movies_2024.csv")
print("================================")