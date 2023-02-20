import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

st.title("Song Recommender")

df=pd.read_csv('tcc_ceds_music.csv')

size = len(df)+1
df.insert(0, 'song_id', range(1, size))

df = df[['song_id','artist_name','release_date','genre', 'topic', 'age', 'track_name']]

df['release_date'] = df['release_date'].astype("str")
df["tags"] = df["topic"] +","+ df["genre"] +","+ df["release_date"]

# df = df.iloc[-500:]

df = df.head(1000)

count = CountVectorizer(stop_words='english')

count_matrix = count.fit_transform(df['tags'])

cosine_sim = cosine_similarity(count_matrix, count_matrix)

indices_from_title = pd.Series(df.index, index=df['track_name'])
indices_from_song_id = pd.Series(df.index, index=df['song_id'])


def get_recommendations(title="", cosine_sim=cosine_sim, idx=-1):
    if idx == -1 and title != "":
        idx = indices_from_title[title]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    sim_scores = sim_scores[1:3]

    song_indices = [i[0] for i in sim_scores]

    return song_indices

song = st.text_input('Enter your favorite song', '')

df1 = df.loc[get_recommendations(title=song)]

rec = []


if song=="":
    st.write("")
else:
    st.header("Recommendations for you")
    for i in (df1["track_name"]):
        st.write(i)