# Content-Based Recommender System
Samuel Geremew and Kedir Birhan

## Overview
The goal is to implement a **movie recommender system** that learns from a user's view history and movie ratings to predict their rating for an unseen movie. The provided dataset includes users, movies, actors, directors, ratings, genres, and tags. We implemented a content-based, filtering approach in Python that uses keywords to determine movie similarity and predict ratings based on the user.

## Pre-processing
The dataset came from different files and tables. We converted genres, actors, directors, and tags into Pandas dataframes ordered by movieID. We assembled movie profiles by combining genres, actorIDs, directorIDs, and tags into one dataframe ordered by movieID. Merging data caused some features to be missing, which could impact scores. So we filled in missing values with defaults.

## Feature Reduction
Before combining dataframes, we removed unnecessary features like actor names and only kept actor IDs. We filtered for highly-rated actors above a threshold. We only kept tags used by many users. Reducing features cut runtime and improved our [Root Mean Square Error (RMSE)](https://en.wikipedia.org/wiki/Root-mean-square_deviation).

## Bag of words
We created document vectors for movie profiles. We cleaned text by removing stopwords and lowercasing tags to differentiate from genres. We combined rows into a bag of words representing important keywords from movie descriptions. This created a vocabulary of descriptive terms for the recommender system.

## Vectorize and Similarity
Vectorized movie descriptions using scikit-learn's [CountVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html) ordered by term frequency. This gave more weight to rare words in the keyword vocabulary. [Inverse document frequency](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) allowed giving more weight to actors/directors that were in very few movies. After vectorizing, we computed a similarity matrix between all movies using cosine similarity. This allowed finding movies most similar to a user's preferences.

## Recommender
From the training data, we built a basic user profile of movies they've watched. Our recommender system takes a userID, gets their watched movies, and finds similarity scores to the unseen movie from the matrix. It averages the scores of the 5 most similar watched movies to predict the user's rating for the new movie. This personalized content-based filtering approach recommends movies based on inferred user preferences.

## Results and Conclusion
Our first implementation was to use the /train.dat file and append some of the content features to it. This did technically work and we used a Decision Tree Classifier. However, this approach did not have great results even though it ran extremely fast. The Decision Tree Classifier resulted in a RMSE of 1.28.

The second approach was to use the movie profile and user profiles. This allowed us to personalize the movie rating scheme. We removed redundant features, uninformative features, and reduced specific unimportant features (e.g. a specific unimportant feature would be user tags that appeared only once for a given movie). Optimized many of the functions and methods used. A simple example was by timing how long the ‘ ‘.join function took to run versus using ‘+’ to add two data frames together. The vectorized movie profile and user profile approach resulted in a RMSE of 1.09.
