import streamlit as st
import pickle
import requests
import time

st.title("Movie Recommendation System 🎬")
st.write("App started 🚀")

# -------------------- LOAD DATA SAFELY --------------------
try:
    movies_list = pickle.load(open('movies.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()


# -------------------- COMPUTE SIMILARITY (CACHED) --------------------
@st.cache_data
def compute_similarity(data):
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    cv = CountVectorizer(max_features=2000, stop_words='english')
    vectors = cv.fit_transform(data['tags']).toarray()
    return cosine_similarity(vectors)


similarity = compute_similarity(movies_list)


# -------------------- FETCH POSTER --------------------
def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=0a17f2c0c35553b988319b763e54f0da&language=en-US'
        response = requests.get(url, timeout=3)
        data = response.json()

        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except:
        return "https://via.placeholder.com/500x750?text=No+Image"


# -------------------- RECOMMEND FUNCTION --------------------
def recommend(movie):
    try:
        m = movies_list[movies_list["title"] == movie].index[0]
        distances = similarity[m]

        movies_list['similarity'] = distances
        movies_sorted = movies_list.sort_values(by='similarity', ascending=False)

        top_movies = movies_sorted.iloc[1:6]

        names = []
        posters = []

        for _, row in top_movies.iterrows():
            names.append(row['title'])
            posters.append(fetch_poster(row['id']))
            time.sleep(0.2)

        return names, posters

    except Exception as e:
        st.error(f"Recommendation error: {e}")
        return [], []


# -------------------- UI --------------------
movies_title = movies_list["title"].values
selected_movie_name = st.selectbox("Select a movie", movies_title)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    if names:
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])
