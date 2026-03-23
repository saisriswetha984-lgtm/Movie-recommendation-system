
import pickle
import streamlit as st
import requests

# 🔥 Fetch poster using movie name
def fetch_poster(movie_name):
    try:
        movie_name = movie_name.split("(")[0]

        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": "e83c81f3f7b32d2a67e9d6a1fc412825",
            "query": movie_name
        }

        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        results = data.get('results', [])

        # 🔥 Find first movie WITH poster
        for movie in results:
            poster_path = movie.get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path

        # fallback
        return "https://via.placeholder.com/300x450.png?text=No+Poster"

    except Exception as e:
        print("ERROR:", e)
        return "https://via.placeholder.com/300x450.png?text=Error"


# 🔥 Recommendation logic
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_name = movies.iloc[i[0]].title

        recommended_movie_names.append(movie_name)
        recommended_movie_posters.append(fetch_poster(movie_name))

    return recommended_movie_names, recommended_movie_posters


# 🎬 UI
st.title('🎬 Movie Recommendation System')
st.write("Get top 5 similar movie recommendations instantly!")

# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values

# Dropdown
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Button
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    st.subheader("Top 5 Recommendations")

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])

            poster = recommended_movie_posters[i]

            # Extra safety check
            if poster is None or not str(poster).startswith("http"):
                poster = "https://via.placeholder.com/300x450.png?text=No+Poster"

            st.image(poster, width='stretch')