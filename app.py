import streamlit as st
import pickle
import requests
import time

def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=0a17f2c0c35553b988319b763e54f0da&language=en-US'.format(movie_id)

    for _ in range(3):  # retry 3 times
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

        except requests.exceptions.RequestException as e:
            print("Error:", e)
            time.sleep(1)  # wait before retry

    return "https://via.placeholder.com/500x750?text=No+Image"
#def fetch_poster(movie_id):
 #   response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=0a17f2c0c35553b988319b763e54f0da&language=en-US'.format(movie_id))
  #  data=response.json()
   # return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
def recommand(movie):
    m=movies_list[movies_list["title"]==movie].index[0]
    distances = similarity[m]
    movies_list['similarity'] = distances

    movies_sorted = movies_list.sort_values(by='similarity', ascending=False)
    a = movies_sorted.iloc[1:6]['id'].values
    recommanded_movies=[]
    recommanded_movies_poster=[]
    for i in a:
        recommanded_movies.append(movies_list[movies_list["id"]==i]["title"].values[0])
        recommanded_movies_poster.append(fetch_poster(i))
        time.sleep(0.2)
    return recommanded_movies,recommanded_movies_poster
movies_list=pickle.load(open('movies.pkl','rb'))
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# create similarity dynamically
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies_list['tags']).toarray()

similarity = cosine_similarity(vectors)
movies_title=movies_list["title"].values
st.title("movie Recommendation System")
#st.header("Movie Recommendation System12")
selected_movie_name=st.selectbox("Select an option",movies_title)
if st.button("Recommend"):
    recommandation,posters=recommand(selected_movie_name)
  #  for i in recommandation:
   #     st.write(i)
    c1,c2,c3,c4,c5=st.columns(5)
    with c1:
        st.text(recommandation[0])
        st.image(posters[0])
    with c2:
        st.text(recommandation[1])
        st.image(posters[1])
    with c3:
        st.text(recommandation[2])
        st.image(posters[2])
    with c4:
        st.text(recommandation[3])
        st.image(posters[3])
    with c5:
        st.text(recommandation[4])
        st.image(posters[4])