import streamlit as st
import pickle
import requests
import time

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.markdown("<h1 style='text-align: center; color: red;'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)
st.write("Find movies similar to your favorite ones 🍿")

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    return pickle.load(open('movies.pkl', 'rb'))

try:
    movies_list = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# -------------------- COMPUTE SIMILARITY (OPTIMIZED) --------------------
@st.cache_data
def compute_similarity(data):
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    cv = CountVectorizer(max_features=1500, stop_words='english')
    vectors = cv.fit_transform(data['tags'])   # ❗ removed .toarray()

    return cosine_similarity(vectors)

similarity = compute_similarity(movies_list)

# -------------------- FETCH POSTER --------------------
def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=0a17f2c0c35553b988319b763e54f0da'
        response = requests.get(url, timeout=3)
        data = response.json()

        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"
    except:
        return "https://via.placeholder.com/300x450?text=No+Image"

# -------------------- RECOMMEND FUNCTION --------------------
def recommend(movie):
    index = movies_list[movies_list["title"] == movie].index[0]
    distances = similarity[index]

    movies_list['similarity'] = distances
    movies_sorted = movies_list.sort_values(by='similarity', ascending=False)

    top_movies = movies_sorted.iloc[1:6]

    names = []
    posters = []

    for _, row in top_movies.iterrows():
        names.append(row['title'])
        posters.append(fetch_poster(row['id']))

    return names, posters

# -------------------- UI --------------------
movie_list = movies_list["title"].values

selected_movie = st.selectbox("🔍 Select a Movie", movie_list)

if st.button("🎯 Recommend"):
    with st.spinner("Finding best movies for you..."):
        names, posters = recommend(selected_movie)

    st.markdown("## 🎥 Top Recommendations")

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.markdown(f"**{names[i]}**")