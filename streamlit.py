import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd 
import numpy as np

st.title("Food Recommender")

df1=pd.read_csv('food.csv')
df1.columns = ['food_id','title','price', 'num_orders', 'category', 'avg_rating', 'num_rating', 'tags']

def create_soup(x):            
    tags = x['tags'].lower().split(', ')
    tags.extend(x['title'].lower().split())
    tags.extend(x['category'].lower().split())
    return " ".join(sorted(set(tags), key=tags.index))

df1['soup'] = df1.apply(create_soup, axis=1)

count = CountVectorizer(stop_words='english')

count_matrix = count.fit_transform(df1['soup'])

cosine_sim = cosine_similarity(count_matrix, count_matrix)

indices_from_title = pd.Series(df1.index, index=df1['title'])
indices_from_food_id = pd.Series(df1.index, index=df1['food_id'])

def get_recommendations(title="", cosine_sim=cosine_sim, idx=-1):
    if idx == -1 and title != "":
        idx = indices_from_title[title]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    sim_scores = sim_scores[1:3]

    food_indices = [i[0] for i in sim_scores]

    return food_indices

food = st.text_input('Enter your favorite food', '')

df2 = df1.loc[get_recommendations(title=food)]

rec = []


if food=="":
    st.write("")
else:
    st.header("Recommendations for you")
    for i in (df2["title"]):
        # st.write(df2["title"])
        st.write(i)