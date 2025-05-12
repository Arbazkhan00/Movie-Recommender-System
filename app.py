import streamlit as st
import pickle
import pandas as pd
import requests

# Load movie data and similarity matrix
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# TMDb API Key
API_KEY = '27c7db380b786af195adc3564c0cfc56'

# Function to fetch poster from TMDb
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url)
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500" + data['poster_path']
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"
    except:
        return "https://via.placeholder.com/300x450?text=Error"

# Recommend function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:21]

    recommended_titles = []
    recommended_posters = []
    for i in movie_indices:
        movie_id = movies.iloc[i[0]]['id']  # make sure 'id' exists in movies.pkl
        title = movies.iloc[i[0]]['title']
        recommended_titles.append(title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_titles, recommended_posters

# Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title('🎬 Movie Recommender System')

selected_movie = st.selectbox('Select a movie you like:', movies['title'].values)

if st.button('Show Recommendations'):
    titles, posters = recommend(selected_movie)

    # Display 20 movies in 4 rows of 5 columns
    for row in range(4):
        cols = st.columns(5)
        for col in range(5):
            i = row * 5 + col
            with cols[col]:
                st.image(posters[i])
                st.caption(titles[i])
