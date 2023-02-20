import pandas as pd 
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def main(title):
    df = pd.read_csv('tcc_ceds_music.csv')
    size = len(df)+1
    df.insert(0, 'song_id', range(1, size))

    df = df[['song_id','artist_name','release_date','genre', 'topic', 'age', 'track_name']]

    df['release_date'] = df['release_date'].astype("str")

    df["tags"] = df["topic"] +","+ df["genre"] +","+ df["release_date"]

    df = df.head(1000)

    count = CountVectorizer(stop_words='english')

    count_matrix = count.fit_transform(df['tags'])

    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    indices_from_title = pd.Series(df.index, index=df['track_name'])
    indices_from_food_id = pd.Series(df.index, index=df['song_id'])

    idx=-1

    if idx == -1 and title != "":
        idx = indices_from_title[title]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    sim_scores = sim_scores[1:6]

    song_indices = [i[0] for i in sim_scores]

    df1 = df.loc[song_indices]

    return (df1['track_name'].values.tolist())
    # print(df1['track_name'])
