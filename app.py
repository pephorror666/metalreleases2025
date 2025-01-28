import streamlit as st
import pandas as pd
import base64

# Función para aplicar estilo CSS
def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Cargar el archivo CSV
@st.cache_data
def load_data():
    df = pd.read_csv('releases2025_updated.csv')
    return df

# Función para filtrar datos
def filter_data(df, search_term):
    return df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

# Función para crear tarjetas de álbumes
def create_album_card(row):
    card = f"""
    <div class="album-card">
        <h3>{row['Album']}</h3>
        <p><strong>Date:</strong> {row['Date']}</p>
        <p><strong>Type:</strong> {row['Type']}</p>
        <p><strong>Genre:</strong> {row['Genre']}</p>
        <p><a href="{row['Spotify']}" target="_blank">Spotify</a> | <a href="{row['Bandcamp']}" target="_blank">Bandcamp</a></p>
    </div>
    """
    return card

# Configuración de la página
st.set_page_config(page_title="Metal Releases 2025", layout="wide")

# Aplicar CSS personalizado
local_css("style.css")

# Título de la aplicación
st.title("Metal Releases 2025")

# Cargar datos
df = load_data()

# Barra de búsqueda
search_term = st.text_input("Buscar álbumes (por artista, género, tipo, etc.)")

# Filtrar datos
if search_term:
    filtered_df = filter_data(df, search_term)
else:
    filtered_df = df

# Mostrar álbumes
for _, row in filtered_df.iterrows():
    st.markdown(create_album_card(row), unsafe_allow_html=True)

# Agregar contador de resultados
st.write(f"Mostrando {len(filtered_df)} de {len(df)} álbumes")
