import streamlit as st
import pandas as pd
import random

# Function to apply CSS style
def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load CSV file
@st.cache_data
def load_data():
    df = pd.read_csv('releases2025_updated.csv')
    return df

# Function to filter data
def filter_data(df, search_term):
    return df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

# Function to create album cards
def create_album_card(row):
    spotify_link = f'<a href="{row["Spotify"]}" target="_blank">Spotify</a>' if 'Error.' not in row['Spotify'] else ''
    bandcamp_link = f'<a href="{row["Bandcamp"]}" target="_blank">Bandcamp</a>' if 'Error.' not in row['Bandcamp'] else ''
    links = ' | '.join(filter(None, [spotify_link, bandcamp_link]))

    card = f"""
    <div class="album-card">
        <h3>{row['Album']}</h3>
        <div class="album-details">
            <p style="display: inline-block; margin-right: 10px;"><strong>Date:</strong> {row['Date']}</p>
            <p style="display: inline-block; margin-right: 10px;"><strong>Type:</strong> {row['Type']}</p>
            <p style="display: inline-block;"><strong>Genre:</strong> {row['Genre']}</p>
        </div>
        <p>{links}</p>
    </div>
    """
    return card

# Function to get a random record
def get_random_record(df):
    return df.sample(n=1).iloc[0]

# Page configuration
st.set_page_config(page_title="Metal Releases 2025", layout="wide")

# Apply custom CSS
local_css("style.css")

# App title
st.title("Metal Releases 2025")

# Load data
df = load_data()

# Button to get a random album
if st.button("Show Random Album"):
    random_row = get_random_record(df)
    st.markdown(create_album_card(random_row), unsafe_allow_html=True)

# Search bar
search_term = st.text_input("Search for albums (by artist, genre, type, record name, etc.)")

# Filter data dynamically
filtered_df = filter_data(df, search_term)

# Display albums
for _, row in filtered_df.iterrows():
    st.markdown(create_album_card(row), unsafe_allow_html=True)

# Add results counter
st.write(f"Showing {len(filtered_df)} of {len(df)} records")
