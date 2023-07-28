# recommender-system

Samuel Geremew
Kedir Brian

# Content-Based Recommender System
In this assignment, we are tasked to implement a movie recommender system that Is able to learn from the user’s movie view history and ratings of movie they have watched in order to predict what the user would give to a movie that they have not rated.  In order to build the movie recommender system, we are provided with data on users and movies. The dataset includes information on actors, directors, ratings, genres,  user tags, and movies. To build the movie recommender system, we implemented a content-based filtering approach in Python where the algorithm uses keywords to determine movie similarities and predicts ratings for movies depending on the user.

## Pre-processing
Since the dataset comes from different files and tables, we started by first filtering and converting the genres, actors, directors, and user tags datasets into pandas data frames ordered by the ‘movieID’ field. Then we assembled the movie profiles. We combined the genres, actorIDs, directorIDs, and movie tags into a data frame and ordered the table by the ‘movieID’ so it will be easier for us to retrieve information later in other preprocessing and classification steps. One thing we have noticed is, since all the data comes from different sources, there are missing information on some features when we tried to merge all the data into one. This could have an impact on our scores. So, we had to give these empty features default values in order to not hugely impact our scores.

## Feature Reduction
Now, before combining the data frames we removed certain features that we deemed either unnecessary, redundant, or not very useful. For example we kept actorID’s and directorID’s but removed all of their corresponding names. For the actors we only included actors with a rating of 10 or higher. Then for the tags we only included  tags that were added by 4 or more users. This greatly helped reduce the time to run our program and surprising helped in our score as well.

## Bag of words
Our goal with the movie profiles is to create description (document) vectors similar to Homework Assignment 1. First we cleaned up the text data in each column by removing stop words and making all the tags lower case to differentiate them from the genres. Then we combined all the rows to create our bag of words which is really a set of key words of the movie description.

## Vectorize and Similarity
From our bag of words we take each movie description and vectorize it using a term frequency vector function from sklearn module call CountVectorizer. It gives importance to words that occur less often in the entire collection of key words for our movie database. We did not use the inverse-term-frequency function because it would give less importance to some of our actors and directors who do not appear very often. Now, after we have vectorized our movies we will create a similarity matrix. We use the cosine similarity to compute the matrix.

## Recommender
Finally, using our training data, which is essentially a very barebones user profile we use the movies they have watched to predict the rating of the movie that they have not watched yet. Our recommender function takes in the userID and produces the list of movies the user has watched. From their watched list it gets, from the similarity matrix, the similarities compared to the unwatched film. Then we simply pick the top 5 most similar movies from the user’s profile and average them to get the rating prediction for the new movie.

## Results and Conclusion
There were a few things that we attempted that did not work or were difficult to implement. For instance we did not include the /user_taggedmovies.dat file because we did not believe it would help or hurt with our chosen implementation. Our first implementation was to use the /train.dat file and append some of the content features to it. This did technically work and we used a Decision Tree Classifier however it did not have great results but it did run extremely fast. We scored a RMSE of 1.28 using the Decision Tree Classifier. After taking a look at the provided chapter from Piazza and doing more research we decided to use the movie profile and user profile approach. This allowed a more personalized movie rating scheme. In this approach we removed redundant features, uninformative features, and reduced specific unimportant features. An example of specific unimportant features would be user tags that appeared only once for a given movie. We also tried to optimize many of the functions and methods we used. For example we used the time library to time how long the ‘ ‘.join function took to run versus using ‘+’ to add two data frames together. This approach resulted in a RMSE score of 1.09.
