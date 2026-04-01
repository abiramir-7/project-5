import streamlit as st
import pandas as pd
from recommendation import get_recommendations

# Page Configuration
st.set_page_config(page_title="IMDb 2024 Recommender", page_icon="🎥", layout="wide")

# Custom CSS for UI Enhancement
st.markdown("""
    <style>
    /* Background */
    .stApp {
        background: linear-gradient(135deg, #020300 0%, #ffffff 100%);
    }

    /* Target specific headers and labels to be white */
    /* This fixes the Title, Subtitle, and Top 5 header */
    .stApp h1, .stApp h2, .stApp h3, .stApp p {
        color: white !important;
    }

    /* Target the Text Area label: 'Paste a storyline or describe a plot:' */
    .stWidgetLabel p {
        color: white !important;
    }

    .stTextArea textarea {
        background-color: #1e1e1e;
        color: white;
        border: 3px solid #f5c518;
    }
    
    .movie-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #f5c518;
        margin-bottom: 20px;
    }
    
    .movie-title {
        color: #f5c518;
        font-size: 22px;
        font-weight: bold;
    }
    
    .imdb-logo {
        color: #000000;
        background-color: #f5c518;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
    }
            
    /* Style the button container */
    .stButton > button {
        background-color: #020300 !important; 
        color: #020300
        font-weight: bold !important;
        border-radius: 5px !important;
        border: none !important;
        width: 100% !important;            
        transition: 0.3s;
    }

    /* Style the button hover effect */
    .stButton > button:hover {
        background-color: #e2b616 !important; /* Slightly darker yellow on hover */
        color: #000000 !important;
        border: none !important;
    }
    
    /* Style the button click/active state */
    .stButton > button:active {
        background-color: #f5c518 !important;
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 1 & 2. Header Section: '2024 Movie Recommender' and the description
st.markdown("# <span class='imdb-logo'>IMDb</span> 2024 Movie Recommender", unsafe_allow_html=True)
st.write("Find movies from 2024 that match your favorite plot style using NLP and Cosine Similarity.")
st.divider()

# 3. User Input Section: 'Paste a storyline or describe a plot:'
user_storyline = st.text_area("Paste a storyline or describe a plot:", 
                              height=150,
                              placeholder="e.g., A group of explorers travel through a wormhole in space...")

if st.button("✨ Discover Similar Movies"):
    if user_storyline:
        try:
            df = pd.read_csv("movies_2024.csv")
            recommendations = get_recommendations(user_storyline, df)
            
            # 4. Results Header: 'Top 5 Matches Found:'
            st.subheader("Top 5 Matches Found:")
            
            # Display results in stylized cards
            for index, row in recommendations.iterrows():
                st.markdown(f"""
                    <div class="movie-card">
                        <div class="movie-title">🎬 {row['Movie Name']}</div>
                        <p style="color: #cccccc; margin-top: 10px;">{row['Storyline']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
        except FileNotFoundError:
            st.error("Dataset not found. Please run the scraping script first.")
    else:
        st.warning("Please enter a storyline to get started.")