import numpy as np

import streamlit as st
import pickle
import pandas as pd
import requests

movie_dict = pickle.load(open('movies_dict.pkl', 'rb'))            # this is the new_df dataframe(in a dictionary form) which we took from the jupyter notebook using pickle
movies = pd.DataFrame(movie_dict)                         # converted the dict to a dataframe

sim = pickle.load(open('similarity_matrix.pkl', 'rb'))                 # this is the sim matrix which we took from the jupyter notebook using pickle

original_dataset_dict = pickle.load(open('original_dataset_dict.pkl', 'rb'))      # original tmdb dataset to be used for getting movie links
original_dataset = pd.DataFrame(original_dataset_dict)

def recommend(movie_name, movie_database=movies, similarity_score=sim):      # same recommender function like the one in the jupyter notebook
    movie_id = movie_database.id[movie_database['title'] == movie_name]
    movie_index = movie_database[movie_database['title'] == movie_name].index

    l = list(enumerate(similarity_score[movie_index[0]]))

    l = sorted(l, reverse=True, key=lambda x: x[1])

    best_rcmds = l[1:6]

    index_of_best_rcmds = []
    for i in best_rcmds:
        index_of_best_rcmds.append(i[0])

    titles_of_best_rcmds = []
    for i in index_of_best_rcmds:
        titles_of_best_rcmds.append(movie_database.title[i])

    ids_of_best_rcmds = []
    for i in index_of_best_rcmds:
        ids_of_best_rcmds.append(movie_database.id[i])

    posters_of_best_rcmds=[]                                             # fetches the movie posters' path using fetch_movie_poster()
    for i in ids_of_best_rcmds:
        posters_of_best_rcmds.append(fetch_movie_poster(i))


    return titles_of_best_rcmds,posters_of_best_rcmds

def fetch_movie_poster(movie_id):                    # helps in finding the correct path of the poster from the tmdb website

    url = "https://api.themoviedb.org/3/movie/{}?api_key=1efb08f20220f8a95a51eb6e1f3e4758&language=en-US".format( movie_id )   # url of coresponding movie_id
    data = requests.get(url)
    data = data.json()                                              # data was converted into json format
    poster_path = data['poster_path']                               # poster path is extracted from the json obj of the movie(doesnt give the complete path)
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

st.title( 'Movie Recommender' )

selected_movie_name = st.selectbox(                                     # used to create the drop down list
    'Enter your movie name',
    movies.title.values                                   # movies to select from in the dropdown list
)

if st.button('Recommend'):                                 # creates a button which will trigger certain function when clicked

    top_5_recommendation_names,top_5_recommendation_posters = recommend(selected_movie_name)         # lists which store output from recommend func

    for i in top_5_recommendation_names:

        link = list(original_dataset[original_dataset.title==i].homepage.values)

        st.write(i, ' : ', link[0])                                                # prints the elements on the website


    col1, col2, col3, col4, col5 = st.columns(5)                       # creates 5 columns
    with col1:
        st.text(top_5_recommendation_names[0])                     # displays names (text-small size text;header-larger sized text)
        st.image(top_5_recommendation_posters[0])                  # displays image/poster
    with col2:
        st.text(top_5_recommendation_names[1])
        st.image(top_5_recommendation_posters[1])
    with col3:
        st.text(top_5_recommendation_names[2])
        st.image(top_5_recommendation_posters[2])
    with col4:
        st.text(top_5_recommendation_names[3])
        st.image(top_5_recommendation_posters[3])
    with col5:
        st.text(top_5_recommendation_names[4])
        st.image(top_5_recommendation_posters[4])
