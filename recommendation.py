import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import re

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    # Remove punctuation and lowercase [cite: 25]
    text = re.sub(r'[^\w\s]', '', text).lower()
    # Remove stop words [cite: 25]
    words = text.split()
    cleaned = [w for w in words if w not in stop_words]
    return " ".join(cleaned)

def get_recommendations(user_input, df):
    # Preprocess the dataset storylines [cite: 77]
    df['cleaned_storyline'] = df['Storyline'].apply(clean_text)
    
    # Vectorize using TF-IDF [cite: 28, 78]
    tfidf = TfidfVectorizer()
    combined_text = pd.concat([df['cleaned_storyline'], pd.Series([clean_text(user_input)])])
    tfidf_matrix = tfidf.fit_transform(combined_text)
    
    # Calculate Cosine Similarity [cite: 31, 79]
    # Compare the last item (user input) against all movies
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    
    # Rank and get top 5 [cite: 32, 34]
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sim_scores[:5]]
    
    return df.iloc[top_indices][['Movie Name', 'Storyline']]