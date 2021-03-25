# movie-recommeder

# Recommendation Systems

The rise of large corporations with extensive item catalogs and customer bases, has made recommendation systems more important in today's economy. 

In traditional commerce, were an individual would travel to a physical store to purchase products, the range of options is limited by the shelf-space of the store. This inherent scarcity made it reasonably easy for a person to figure out what to buy.

But in today's world with large companies, like Amazon and Netflix, who boast catalogs of thousands to millions of products, it is near impossible for an individual to find everything they would otherwise be willing to purchase. An opportunity cost that results in recommendations systems being pertinent  for such companies. 

---

This project's purpose is an attempt to prototype a recommender system. The data used is `movie-lens`.

Three approaches to making a recommendation will be taken:
1. Content based approach
    - webscrape imdb website for metadata of movies to be recommended
    - cleaning the text data recieved
    - vectorized the text data
    - compute the cosine similarites between movies (items) 
    - make recommendation based on movie selected

2. Item-Based Collabrative approach
    - construct a M by N utility matrix, with the columns being the users and the index being the movies, and the values being the ratings users give to a movie
    - this matrix will have a lot of NaN values, since most people have not seen most movies, thus the missing values
        - thus the values will be mean centered, and the missing entries will be replace by zeros
    - use svd to reduce the dimensionaliy of the matrix, 
        - I choose to go with 19 because the movie lens data has 19 movie genres
    - compute cosine similariy between movies 
    - make recommendation based on movie selected and rating given to it

3. User-Based Collabrative approach
- user matrix factorization model approach with scikit surprise
- modeling
    - cross validate compare svd, svdpp, nmf
        - pick model with lowest error
        - grid-search for hyperparameter tuning
- create new "customer profiles"
    - children movie watcher vs horror movie watcher
    - train model on everything including customer profile
    - use model to predict on this new profile

---