import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=23571579463eccee6c20518f860d7510&language=en-US"
    response = requests.get(url)
    
    if response.status_code == 200:  # Ensure successful request
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:  # If poster path exists
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
    return None  # Return None if there's no poster

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster = fetch_poster(movie_id)
        if poster:  # Only append if the poster was successfully fetched
            recommended_movie_posters.append(poster)
            recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')

# Load movie list and similarity matrix
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Show recommendations
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Displaying recommendations in columns
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        if idx < len(recommended_movie_names):  # Check if there are enough recommendations
            with col:
                st.text(recommended_movie_names[idx])
                st.image(recommended_movie_posters[idx])
