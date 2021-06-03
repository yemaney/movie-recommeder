import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

import streamlit as st


@st.cache
def create_link(title):
    x = str(df[df['title'] == title]['imdbid'].values[0])
    if len(x) < 6:
        x = '0' + x
    return 'https://www.imdb.com/title/tt0' + x

@st.cache
def get_images(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'lxml')
    poster  = soup.find('img', class_="ipc-image")
    link = poster.get('src')
    return  link

df = pd.read_csv('streamlit/movie_meta.csv')
    
type = st.sidebar.selectbox('Type',
                            ('Home', 'Content Based','Collabrative'))

if type == 'Home':
    st.title('Movie Recommender')
    
    ## explain the purpose of app
    st.markdown('''
                ## This is an app that uses python to make movie suggestions
                Recommendation can be:
                - Content based
                - Collabrative filtering
                
                Use the side bar to navigate through the different approaches
                ''')
    
    
    ## Set main page image
    st.image('https://images.unsplash.com/photo-1478720568477-152d9b164e26?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=750&q=80')

if type == 'Content Based':
    st.title('Content Based Recommendations')
    
    ## Explain how content based works
    st.markdown('''
                ## Content based recommnendations are the most intuitive.
                The general appraoch is to recommend items with similar
                contents to a selected item. In the example of movies,
                the system may recommend movies with similar themes,
                actors, etc.
                
                
                ''')
        
    st.markdown('---')

    ## Set content page image
    st.image('https://storage.googleapis.com/morphl-static-assets/blog/wp-content/uploads/2020/03/content-based-filtering-01.png')
    
    st.markdown('---')
    st.markdown('## Catalog')

    df
    
    cosine_sim = np.load('streamlit/cosine_sim.npy')
    
    @st.cache
    def get_movie_idx(title, df=df):
        return df[df['title'] == title].index[0]

    @st.cache
    def get_top_3(title, df=df):
    
        recommended_movies = []
        idx = get_movie_idx(title)
        score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
        top_10_indices = list(new_func(score_series).index)
        # top_10_indices = list(score_series.iloc[1:4].index)
        
        cont1 = df.loc[top_10_indices[0], 'title']
        cont2 = df.loc[top_10_indices[1], 'title']
        cont3 = df.loc[top_10_indices[2], 'title']
        
        return cont1, cont2, cont3

    def new_func(score_series):
        return score_series.iloc[1:4]
 
    st.markdown('---')
   
    st.markdown('## Choose a movie')
    
    title = st.selectbox('Movie title', df.title.values)
    
    if title is not None:
        a, b, c = get_top_3(title)
        st.markdown('## Here are your recommendations')
        
        links = []
        for i in [a,b,c]:
            link = create_link(i)
            links.append(link)
                
        images = []
        for i in links:
            image = get_images(i)
            images.append(image)        

        col1, col2, col3 = st.beta_columns(3)
        with col1:
            st.image(images[0])
            st.markdown(f'[{a}]({links[0]})')
        with col2:
            st.image(images[1])
            st.markdown(f'[{b}]({links[1]})')
        with col3:
            st.image(images[2])
            st.markdown(f'[{c}]({links[2]})')

if type == 'Collabrative':
    st.title('Collabrative Filtering')
    
    st.markdown('''
                Collabrative based recommendation systems try to make
                recommendations based on item similarity. However it
                uses implicit information about the item to determine 
                their level of similarity. One way to think about it is,
                items should be recommended to users based on what similar
                users choices.
                
                ---
                ''')
    st.image('https://www.xpertup.com/wp-content/uploads/edd/2020/07/movie-recommender.png')
    
    st.markdown('---')
    st.markdown('## Catalog')
    
    df 
    
    corr_mat = np.load('streamlit/item_colab.npy')
    ratings = pd.read_csv('streamlit/ratings.csv')
    
    @st.cache
    def item_colab(title, ratings=ratings, corr_mat=corr_mat):
        col_idx = ratings.columns.get_loc(title)

        corr_specific = corr_mat[col_idx]
        item1,item2,item3 = np.argsort(corr_specific)[::-1][1:4]
        
        item1 = ratings.columns[item1]
        item2 = ratings.columns[item2]
        item3 = ratings.columns[item3]
        
        return item1, item2, item3
    
    st.markdown('---')

    st.markdown('## Choose a movie')

    title = st.selectbox('Movie title', df.title.values)

    
    
    if title is not None:
        a, b, c = item_colab(title)
        st.markdown('## Here are your recommendations')
        
        links = []
        for i in [a,b,c]:
            link = create_link(i)
            links.append(link)
                
        images = []
        for i in links:
            image = get_images(i)
            images.append(image)        

        col1, col2, col3 = st.beta_columns(3)
        with col1:
            st.image(images[0])
            st.markdown(f'[{a}]({links[0]})')
        with col2:
            st.image(images[1])
            st.markdown(f'[{b}]({links[1]})')
        with col3:
            st.image(images[2])
            st.markdown(f'[{c}]({links[2]})')
    
    st.markdown('---')
