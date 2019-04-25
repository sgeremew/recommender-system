


import pandas as pd 
  
# Get the data 
train_col_name = ['userID', 'movieID', 'rating'] #1
tags_col_name=['id','value'] #2
test_col_name=['userID', 'movieID']
movie_tags_col_name=['movieID','tagID','tagWeight'] #3
movie_generes_col_name=['movieID','genre'] #4
movie_directors_col_name=['movieID','directorID','directorName'] #5
movie_actors_col_name=['movieID','actorID','actorName','ranking'] #6
user_taggedmovies_col_name=['userID', 'movieID' ,'tagID']






  

# train = pd.read_csv('train.dat', sep='\t', names=train_col_name)
# tags=pd.read_csv('tags.dat', sep='\t', names=tags_col_name)
# test=tags=pd.read_csv('test.dat', sep=' ', names=test_col_name)
# movie_tags=tags=pd.read_csv('movie_tags', sep='\t', names=movie_tags_col_name)
# movie_generes=tags=pd.read_csv('movie_genres.dat', sep='\t', names=movie_generes_col_name)
# movie_dir=tags=pd.read_csv('movie_directors', sep='\t', names=movie_directors_col_name)
# movie_act=tags=pd.read_csv('movie_actors', sep='\t', names=movie_actors_col_name)
# user_tmov=pd.read_csv('user_taggedmovies.dat', sep=' ', names=user_taggedmovies_col_name)

# Check the head of the data 
df.head() 

traindf = pd.read_csv('train.dat', sep=' ',skiprows=1,names=train_col_name)
train.head()

tagsdf=pd.read_csv('tags.dat', sep='\t', skiprows=1,names=tags_col_name, \
													encoding = "ISO-8859-1")
tags.head()

testdf=pd.read_csv('test.dat', sep=' ',skiprows=1, names=test_col_name)
test.head()

movie_tagsdf=pd.read_csv('movie_tags.dat', sep='\t', skiprows=1, \
													names=movie_tags_col_name)
movie_tags.head()

movie_generesdf=pd.read_csv('movie_genres.dat', sep='\t',skiprows=1, \
												names=movie_generes_col_name)
movie_generes.head()

movie_actdf=pd.read_csv('movie_actors.dat', sep='\t',skiprows=1, \
						encoding = "ISO-8859-1", names=movie_actors_col_name)
movie_actdf.head()

movie_dirdf=pd.read_csv('movie_directors.dat', encoding = "ISO-8859-1", \
						skiprows=1,sep='\t', names=movie_directors_col_name)
movie_dirdf.head()

user_tmovdf=pd.read_csv('user_taggedmovies.dat', sep=' ', \
											names=user_taggedmovies_col_name)

user_tmovdf.head()
