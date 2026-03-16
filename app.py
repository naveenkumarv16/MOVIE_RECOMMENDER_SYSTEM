import streamlit as st
import pickle
import pandas as pd
import requests

# TMDB API KEY
API_KEY = "53a6b0757f7196e8ced9a1d5f8764f67"

# Load data
new_data = pickle.load(open('artifacts/movie_list.pkl','rb'))
similarity = pickle.load(open('artifacts/similarity2.pkl','rb'))
similarity = pd.DataFrame(similarity)

st.title("🎬 Movie Recommender System")

movie_list = new_data["title"].values

selected_movie = st.selectbox(
    "Select Movie",
    movie_list
)


# Fetch poster from TMDB
@st.cache_data
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster"

    except:
        return "https://via.placeholder.com/300x450?text=Poster+Unavailable"


# Recommendation function
def recommend(movie):

    movie = movie.lower()
    new_data['title'] = new_data['title'].str.lower()

    if movie not in new_data['title'].values:
        return [], []

    index = new_data[new_data['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity.iloc[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movies = []
    recommended_posters = []

    for i in distances[1:6]:

        movie_id = new_data.iloc[i[0]].id
        recommended_movies.append(new_data.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# Show recommendations
if st.button("Show Recommendations"):

    movie_names, movie_posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(len(movie_names)):
        with cols[i]:
            st.image(movie_posters[i])
            st.caption(movie_names[i])