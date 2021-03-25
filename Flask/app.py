# imports
from flask import Flask, request, render_template
from flask_restful import Api
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import re
from PIL import Image
from io import BytesIO
import io
import base64


df = pd.read_csv('info/movie_meta.csv')
cosine_sim = np.load('info/cosine_sim.npy')
corr_mat = np.load('info/item_colab_corr.npy')
ratings = pd.read_csv('info/ratings.csv')

def item_colab(title, ratings=ratings, corr_mat=corr_mat):
    col_idx = ratings.columns.get_loc(title)

    corr_specific = corr_mat[col_idx]
    item1,item2,item3 = np.argsort(corr_specific)[::-1][1:4]
    
    item1 = ratings.columns[item1]
    item2 = ratings.columns[item2]
    item3 = ratings.columns[item3]
    
    return item1, item2, item3


def create_link(title):
    x = str(df[df['title'] == title]['imdbid'].values[0])
    if len(x) < 6:
        x = '0' + x
    return 'https://www.imdb.com/title/tt0' + x

def get_movie_idx(title, df=df):
    return df[df['title'] == title].index[0]



app = Flask(__name__)
api = Api(app)


@app.route('/')
def welcome():
    return render_template('form.html')


def get_top_3(title, df=df):
    
    recommended_movies = []
    idx = get_movie_idx(title)
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    top_10_indices = list(score_series.iloc[1:4].index)
    
    cont1 = df.loc[top_10_indices[0], 'title']
    cont2 = df.loc[top_10_indices[1], 'title']
    cont3 = df.loc[top_10_indices[2], 'title']
    
    return cont1, cont2, cont3

def get_image(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'lxml')
    poster  = soup.find('div', class_="poster")
    link = poster.find('img').get('src')
    r = requests.get(link)
    im = Image.open(BytesIO(r.content))
    # Full Script.
    data = io.BytesIO()
    im.save(data, "JPEG")
    return base64.b64encode(data.getvalue())    


@app.route('/result', methods=['POST'])
def result(cosine_sim = cosine_sim):
    title = request.form.get("var_1", type=str)
    profile = request.form.get("var_2", type=str)

    
    cont1, cont2, cont3 = get_top_3(title)
    item1, item2, item3 = item_colab(title)
    
    link1 = create_link(str(cont1))
    image1 = get_image(link1).decode('utf-8')
    
    link2 = create_link(str(cont2))
    image2 = get_image(link2).decode('utf-8')
    
    link3 = create_link(str(cont3))
    image3 = get_image(link3).decode('utf-8')
    
    item_link1 = create_link(str(item1))
    item_image1 = get_image(item_link1).decode('utf-8')
    
    item_link2 = create_link(str(item2))
    item_image2 = get_image(item_link2).decode('utf-8')     
    
    item_link3 = create_link(str(item3))
    item_image3 = get_image(item_link3).decode('utf-8')    
    
    
    if profile == 'child':
        links = ['https://www.imdb.com/title/tt0086190/', 'https://www.imdb.com/title/tt0076759/','https://www.imdb.com/title/tt0109830/']
        svd_movie = ['star wars: episode vi - return of the jedi (1983)', 'star wars (1977)' ,'forrest gump (1994)']
    else:
        links = ['https://www.imdb.com/title/tt0044081',
'https://www.imdb.com/title/tt0268126',
'https://www.imdb.com/title/tt0117589']
        svd_movie = ['a streetcar named desire (1951)',
 'adaptation. (2002)',
 'secrets & lies (1996)']
    
    svd_im1 = get_image(links[0]).decode('utf-8')
    svd_im2 = get_image(links[1]).decode('utf-8')
    svd_im3 = get_image(links[2]).decode('utf-8')
       
    svd1 = svd_movie[0]
    svd2 = svd_movie[1]
    svd3 = svd_movie[2]

    
    
    return render_template('result.html', 
            cont1=cont1, cont2=cont2, cont3=cont3, 
            img_data1=image1, img_data2=image2, img_data3=image3,
            col1=item1,col2=item2,col3=item3,
            item_image1=item_image1,
            item_image2=item_image2,
            item_image3=item_image3,
                          svd_im1=svd_im1,svd_im2=svd_im2,svd_im3=svd_im3,
                          svd1=svd1, svd2=svd2, svd3=svd3)



if __name__ == '__main__':
    app.run( debug=False)