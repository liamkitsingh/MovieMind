import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import vstack,load_npz

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")       #configure page
st.title("Movie Recommender")

#input
st.header("If you liked...")

with st.form("movie_form"):                     #accept user movies
    movies=[]
    years=[]
    for i in range(1,6):
        
        col1, col2 = st.columns([2,1])
        
        with col1:
            movie=st.text_input(                        #movie column
                f"Movie {i} Title",
                key=f"movie_{i}",
                placeholder="Enter Movie Title"
            )
            movies.append(movie)

        
        with col2:
            yr_range = list(range(2025, 1949, -1))
            year = st.selectbox(f"Release Year",          #year column 
                                options=yr_range, 
                                index=0,
                                key=f"year_{i}"
                                )
            years.append(year)
        
        if i<5:
            st.markdown("---")

    submitted=st.form_submit_button("Get recommendations!")     #submit data

if submitted:

    for i in range(5):
        if movies[i]:
            movies[i]=movies[i].strip().lower().replace("-"," ")                                                    #format movie

    movies_db=pd.read_csv("movies_db.csv")
    search_df=movies_db[['title','release_year']].copy()
    search_df['title']=search_df['title'].apply(lambda x: x.strip().lower().replace("-"," "))               #format searchable df


    tf_matrix=load_npz("tf_matrix.npz")                                     #load sparse matrix
    mv_vectors=[]

    for i in range(5):
        if movies[i] and (movies[i] in search_df["title"].values):                 #if user input movie and movie is valid
            match=search_df[(search_df["title"]==movies[i])&(search_df["release_year"]==years[i])]
            if not match.empty:
                idx=match.index[0]
                mv_vectors.append(tf_matrix[idx])                                           #add movie vector to list

    
    if mv_vectors:                                                                      #if vectors exist

        user_vector = np.asarray(vstack(mv_vectors).mean(axis=0))                       #calculate average vector for movies that user likes
        sim=cosine_similarity(user_vector,tf_matrix)                                    #get cosine similarity for each movie
        sim=sim.flatten()                                                               #convert to 1D array
        sim=sim.argsort()[::-1]                                                         #sort in descending order
        recs=[]
        for index in sim:
            title=movies_db.iloc[index]['title']
            year=movies_db.iloc[index]['release_year']
            if title.strip().lower().replace("-"," ") not in movies:
                recs.append((title,year))
            if len(recs)>=10:                                                             #limit to 10 recommendations
                break

        st.header("You should watch...")

        for rec in recs:
            st.markdown(f"- {rec[0]} ({rec[1]})")                               #list recs




