# IMDB Movie Recommendation System Using Storylines (2024)

## Project Overview
This project scrapes movie data for 2024 from IMDb and uses Natural Language Processing (NLP) to recommend movies based on storyline similarity.

## Skills Applied
- **Web Scraping:** Selenium
- **Data Analysis:** Pandas
- **Machine Learning:** TF-IDF Vectorization & Cosine Similarity
- **Web App Development:** Streamlit

## Workflow & Execution
1. **Data Collection:** Run `scraping.py` to extract 2024 movie names and storylines into `movies_2024.csv`.
2. **Text Processing:** The system cleans storylines by removing stop words and punctuation.
3. **Vectorization:** TF-IDF converts text into numerical vectors.
4. **Recommendation:** Cosine Similarity calculates the distance between the user input and the dataset to find the top 5 matches.
5. **Launch App:** Run `streamlit run app.py` to start the interactive interface.

## How to Run
```bash
pip install -r requirements.txt
python scraping.py
streamlit run app.py
