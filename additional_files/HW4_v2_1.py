#!/usr/bin/env python
# coding: utf-8

# In[11]:


import time
import pandas as pd
from rake_nltk import Rake
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

# column header names for the dataframes
train_col_name = ['userID', 'movieID', 'rating'] #1
tags_col_name=['id','value'] #2
test_col_name=['userID', 'movieID']
movie_tags_col_name=['movieID','tagID','tagWeight'] #3
movie_generes_col_name=['movieID','genre'] #4
movie_directors_col_name=['movieID','directorID','directorName'] #5
movie_actors_col_name=['movieID','actorID','actorName','ranking'] #6
user_taggedmovies_col_name=['userID', 'movieID' ,'tagID'] #7


# reading in data from data files and translating into dataframes
traindf = pd.read_csv('train.dat', sep=' ',skiprows=1,names=train_col_name)
tagsdf=pd.read_csv('tags.dat', sep='\t', skiprows=1,names=tags_col_name, encoding = "ISO-8859-1")
tagsdf.set_index('id', inplace=True) # makes the tagsdf indecies the 'id'

small_testdf=pd.read_csv('small_test.dat', sep=' ',skiprows=1, names=test_col_name)
testdf=pd.read_csv('test.dat', sep=' ',skiprows=1, names=test_col_name)
movie_tagsdf=pd.read_csv('movie_tags.dat', sep='\t',skiprows=1, names=movie_tags_col_name)
movie_generesdf=pd.read_csv('movie_genres.dat', sep='\t',skiprows=1, names=movie_generes_col_name)
movie_actdf=pd.read_csv('movie_actors.dat', sep='\t',skiprows=1,encoding = "ISO-8859-1", names=movie_actors_col_name)
movie_dirdf=pd.read_csv('movie_directors.dat', encoding = "ISO-8859-1",skiprows=1,sep='\t', names=movie_directors_col_name)
user_tmovdf=pd.read_csv('user_taggedmovies.dat', sep=' ', names=user_taggedmovies_col_name)
print("done with reading//")

# print(len(movie_actdf['movieID'].unique()))
# print(len(movie_dirdf['movieID'].unique()))
# print(len(movie_generesdf['movieID'].unique()))


# In[12]:


# this removes the tags that are used n times or less
movie_tagsdf = movie_tagsdf[movie_tagsdf.tagWeight > 4]
# this removes the actors who have a rating lower than m
movie_actdf = movie_actdf[movie_actdf.ranking > 10]

# ^ removing rows messes with the indices, so here we reset the indices from 0 to n-1
movie_actdf = movie_actdf.reset_index(drop=True)
movie_tagsdf = movie_tagsdf.reset_index(drop=True)
# movie_tagsdf


# In[13]:


def movieProfiles():
    newdf=movie_generesdf.groupby('movieID').agg(lambda x:' '.join(x)) #combine generes into single row

    actorsdf1=movie_actdf.drop('ranking',axis=1) #remove columns/features that don't provide additional info.
    actorsdf1=movie_actdf.drop('actorName',axis=1)
    
    actorsdf1=movie_actdf.groupby('movieID').agg(lambda x:' '.join(x)) #combine actors into single row
    movie_dirdf1=     movie_dirdf.drop('directorName',axis=1).groupby('movieID').agg(lambda x:' '.join(x)) #combine directors
                                                                                         #and remove column
    arr=[]
    temp=[]
    nextMovieID=1; #start iteration of movie_tagsdf at row 1 because row 0 has column header names
    movie_tags1=movie_tagsdf.drop("tagWeight",axis=1) #removes tagWeight column
    
    for i in range(len(movie_tags1)): # constructing movie tags arrays
        currMovieID = movie_tags1['movieID'][i]
        tagID=movie_tags1['tagID'][i]
        tag=tagsdf['value'][tagID]
        if(currMovieID==nextMovieID):
            temp.append(tag) #add the next tag to the temp array
        else:
            arr.append(temp) #put all the tags we collected in arr position i
            temp=[] #clear them array
            temp.append(tag) #add the next tag to the temp array
            nextMovieID=currMovieID #update the movieID
            
    arr.append(temp)
    
    # converts arrays of tags into strings
    for i in range(len(arr)):
        arr[i]=' '.join(arr[i])
    
    # removes duplicate movie entries and produces a data frame
    ids=movie_tags1['movieID'].unique()
    movie_tags_uniquedf=pd.DataFrame(ids)
    movie_tags_uniquedf['tags']=arr
    movie_tags_uniquedf.columns=["movieID","Movie_tags"]
    
    # we merge on left so that we do not lose any movie due to empty attributes!
    itemProfile=newdf.merge(actorsdf1, how='left',on='movieID')
    itemProfile=itemProfile.merge(movie_dirdf1, how='left',on='movieID')
    itemProfile=itemProfile.merge(movie_tags_uniquedf, how='left',on='movieID')
    
    return itemProfile



# In[14]:


# Timer
timeMovieProfile = time.time()
itemProfile = movieProfiles()
print("\tCreating Movie Profiles...\n--- %s seconds ---" % (time.time() - timeMovieProfile))
itemProfile.head()

cell = itemProfile['Movie_tags'][3]
print(f'Empty Cell in row 4 column \'tags\', {cell},is of type:{type(cell)}')


# In[15]:


# Timer
timeNan = time.time()
itemProfile = itemProfile.fillna('emptycell')
print("\tReplace NaN float with 'none' str...\n--- %s seconds ---" % (time.time() - timeNan))
itemProfile.head()

cell = itemProfile['Movie_tags'][3]
print(f'Empty Cell in row 4 column \'tags\', cell, is of type:{type(cell)}')

itemProfile


# In[16]:



def keyWords(columnName):

    for index, row in itemProfile.iterrows():
        feature = row[columnName]

        # instantiating Rake, by default it uses english stopwords from NLTK
        # and discards all puntuation characters as well
        r = Rake()

        # extracting the words by passing the text
        r.extract_keywords_from_text(feature)

        # getting the dictionary whith key words as keys and their scores as values
        key_words_dict_scores = r.get_word_degrees()

        # assigning the key words to the new column for the corresponding movie
        row[columnName] = list(key_words_dict_scores.keys())
#         rowed = row[columnName]
#         if(index < 3):
#     #         print(f'tags = {tags}\n\nkey_words = {list(key_words_dict_scores.keys())}\n----\n')
#             print(f'tags = {feature}\n\nkey_words = {rowed}\n----\n')


# In[17]:


timeTags = time.time()
keyWords('Movie_tags')
print("\tCleaning movie tags...\n--- %s seconds ---" % (time.time() - timeTags))


# In[18]:


timeGenre = time.time()
keyWords('genre')
print("\tCleaning genres...\n--- %s seconds ---" % (time.time() - timeGenre))


# In[19]:


itemProfile.head()


# In[20]:


#now we join the columns to create our bag of words

itemProfile['Bag'] = itemProfile['genre'].astype(str)+' '+ itemProfile['actorID']                             +' '+itemProfile['directorID']+' '+itemProfile['Movie_tags']
keywordProfile = itemProfile.drop(['genre','actorID','directorID','Movie_tags'],axis=1)
keywordProfile.head()


# In[21]:


# instantiating and generating the count matrix
count = CountVectorizer()
# count = TfidfVectorizer()

timeCount = time.time()
count_matrix = count.fit_transform(keywordProfile['Bag'])
print("\tCreating count matrix...\n--- %s seconds ---" % (time.time() - timeCount))


# In[22]:


# generating the cosine similarity matrix
timeCos_sim = time.time()
cosine_sim = cosine_similarity(count_matrix, count_matrix)
print("\tComputing cosine similarities...\n--- %s seconds ---" % (time.time() - timeCos_sim))


# In[23]:


# creating a Series for the movie titles so they are associated to an ordered numerical
# list I will use in the function to match the indexes
movieIDs = pd.Series(keywordProfile.movieID)
movieIDs.head()


# In[60]:



# Needed: defining the function that takes in userID and movieID and determines
# the rating the user will give this movie
# Nice if it could: already watched the movie? then we just use the same rating!
def recommendations(userID, movieID, cosine_sim = cosine_sim):

    idx = movieIDs[movieIDs == movieID].index[0] #use iloc to index the keywordProfile with idx!!!
    #idx is the index in keywordProfile!
    sim_movie_arr = cosine_sim[idx]
    watched = traindf[traindf['userID'] == userID]
    watchedIDs = pd.DataFrame(watched.movieID)
    
    #creates a user profile of movies watched and their ratings
    user_sim_dict = {"movieID":[],"similarity":[]}
    for i in range(len(movieIDs)):
        this_movie = movieIDs[i]
        if this_movie in watchedIDs.values:
            user_sim_dict['movieID'].append(this_movie)
            user_sim_dict['similarity'].append(sim_movie_arr[i])
    #sorts user movies by similarity to the new movie
    user_sim_df = pd.DataFrame(user_sim_dict).sort_values('similarity',ascending=False)
    user_sim_df.reset_index(inplace=True)
    
    #averages ratings of top 5 similar movies the user has watched
    emptyrating = 3
    emptycount = 1
    rating = 0
    count = 0
    for i in range(5):
        index = user_sim_df['index'][i]
        if(index in watched.index):
            count += 1
#             print(watched['rating'][index])
            rating += watched['rating'][index]
        elif(i == 0):
            count = emptycount
            rating = emptyrating
        
        
#     avg_rating = rating/5
    avg_rating = rating/count
#     avg_rating = rating
    
    return avg_rating


# In[61]:


timeRecommend = time.time()
rating = recommendations(75, 1, cosine_sim = cosine_sim)
print("\tFinding one user rating prediction...\n--- %s seconds ---" % (time.time() - timeRecommend))
print(f'user rating = {rating}')


# In[62]:


testdf.head()


# In[64]:


timeTEST = time.time()

file1 = open("entries.txt","a")
# for i in range(len(small_testdf)):
for i in range(1000):
#     print(f'run {i}')
    rating = recommendations(testdf['userID'][i],testdf['movieID'][i],cosine_sim = cosine_sim)
    file1.write(f'{rating}\n')
file1.close()

print("\tRunning test file...\n--- %s seconds ---" % (time.time() - timeTEST))
# type(small_testdf['movieID'][0])


# In[ ]:




