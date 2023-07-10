# File: objecttier.py
#
# objecttier
#
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
    def __init__(self,Movie_ID, Title, Release_Year):
      self._Movie_ID = Movie_ID
      self._Title = Title
      self._Release_Year = Release_Year

    @property
    def Movie_ID(self):
      return self._Movie_ID
    @property
    def Title(self):
      return self._Title 

    @property
    def  Release_Year(self):
      return self._Release_Year


   


##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:
   def __init__(self,Movie_ID, Title, Release_Year, Num_Reviews, Avg_Rating):
       self._Movie_ID =Movie_ID
       self._Title = Title
       self._Release_Year = Release_Year
       self._Num_Reviews = Num_Reviews
       self._Avg_Rating = Avg_Rating

   @property
   def Movie_ID(self):
      return self._Movie_ID
   @property
   def Title(self):
      return self._Title

   @property
   def Release_Year(self):
      return self._Release_Year
   
   @property
   def Num_Reviews(self):
      return self._Num_Reviews
   
   
   @property
   def Avg_Rating(self):
      return self._Avg_Rating
   





##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
# 
class MovieDetails:
    def __init__(self,Movie_ID, Title, Release_Date, Runtime, Original_Language,Budget,Revenue,Num_Reviews, Avg_Rating, Tagline,Genres,Production_Companies):
       self._Movie_ID = Movie_ID
       self._Title = Title
       self._Num_Reviews = Num_Reviews
       self._Avg_Rating = Avg_Rating
       self._Release_Date = Release_Date
       self._Runtime = Runtime
       self._Production_Companies = Production_Companies
       self._Tagline = Tagline
       self._Genres = Genres
       self._Original_Language = Original_Language
       self._Budget = Budget
       self._Revenue = Revenue
       #Movie_ID

    @property
    def Movie_ID(self):
      return self._Movie_ID

    @property
    def Title(self):
        return self._Title

    @property
    def Num_Reviews(self):
        return self._Num_Reviews

    @property
    def Avg_Rating(self):
        return self._Avg_Rating

    @property
    def Release_Date(self):
        return self._Release_Date

    @property
    def Runtime(self):
        return self._Runtime

    @property
    def Production_Companies(self):
        return self._Production_Companies

    @property
    def Tagline(self):
        return self._Tagline

    @property
    def Genres(self):
        return self._Genres

    @property
    def Original_Language(self):
        return self._Original_Language

    @property
    def Budget(self):
        return self._Budget

    @property
    def Revenue(self):
        return self._Revenue



##################################################################
# 
# num_movies:
#
# Returns: The # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
   param  = None
   sql = "SELECT count(Movie_ID) FROM Movies"
   OBJECT = datatier.select_one_row(dbConn,sql,param)
   if(OBJECT == () or OBJECT == None ):
      return -1

   return OBJECT[0]

   


##################################################################
# 
# num_reviews:
#
# Returns: The # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
    param  = None
    sql = "SELECT count(Rating) FROM Ratings"
    OBJECT = datatier.select_one_row(dbConn,sql,param)
    if(OBJECT == () or OBJECT == None ):
      return -1
      
    return OBJECT[0]


##################################################################
#
# get_movies:
#
# gets and returns all movies whose name include the 
# pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
   sql = " SELECT Movie_ID, Title,  strftime('%Y', Release_Date) From Movies Where Title like ? order by Movie_ID  asc"
   movies = []
   rows = datatier.select_n_rows(dbConn, sql, (pattern,))

   if(rows is not None):
    for entry in rows:
        work = Movie(entry[0], entry[1], entry[2])
        movies.append(work)
    return movies

##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
#
#
def get_movie_details(dbConn, movie_id):
    empty = []
    empty2 = []
    var_round =0
    var =0
    sql = "Select Distinct  Genre_Name FROM Genres JOIN Movie_Genres ON (Movie_Genres.Genre_ID = Genres.Genre_ID ) where Movie_Genres.Movie_ID = ? order by Genre_Name"
    entry2 = datatier.select_n_rows(dbConn, sql, (movie_id,))
    if len(entry2) is not 0:
     for stuff in entry2:
        empty.append(stuff[0]) #  append all the  Genres into a list of strings
   

    sql = "Select Distinct  Company_Name FROM Companies join  Movie_Production_Companies on (Companies.Company_ID = Movie_Production_Companies.Company_ID) where Movie_Production_Companies.Movie_ID= ?  order by Company_Name"
    entry3 = datatier.select_n_rows(dbConn, sql, (movie_id,))
    if len(entry3) is not 0:
     for stuff in entry3:
         empty2.append(stuff[0])  #  append all the Company names into a list of strings
   
    sql = "SELECT count(Rating) FROM Ratings Where Movie_ID = ?"
    entry1 = datatier.select_one_row(dbConn, sql, (movie_id,))
    if entry1[0] is 0:
        entry1 = (0,) + entry1[1:] # change the tuples value using this notation

    sql = "SELECT Movies.Movie_ID, Title, DATE(Release_Date), Runtime, Original_Language, Budget, Revenue,  sum(Rating)/Cast(count(Rating) as Double), Tagline FROM Movies Left JOIN Movie_Taglines on (Movies.Movie_ID = Movie_Taglines.Movie_ID)  Left Join Ratings on (Movies.Movie_ID = Ratings.Movie_ID)  group by  Movies.Movie_ID Having Movies.Movie_ID = ?"
   
    entry = datatier.select_one_row(dbConn, sql, (movie_id,))

    

    if( len(entry) != 0):
        if entry[7] is None:
           
            var_round =0 # grab the avg value and set to 0 if rating does not exist or entry
        else:
            var_round = (entry[7]) 
            
           
        if entry[8] is None:
            var = "" # set tagline to empty if entry in database is null
        else:
            var = entry[8] 
        # Split the string at the comma character
        work = MovieDetails(entry[0], entry[1], entry[2],entry[3], entry[4], (entry[5]), entry[6], entry1[0], var_round, var, empty, empty2)

        return work
    else:
        return None



         

##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average 
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error 
#          msg is already output).
#

def get_top_N_movies(dbConn, N, min_num_reviews):
    sql = "Select Movies.Movie_ID, Title, strftime('%Y', Release_Date), count(Rating) ,(cast(sum(Rating) as double) / cast(count(Rating) as double)) as Avg From Movies JOIN Ratings ON(Movies.Movie_ID= Ratings.Movie_ID) GROUP BY Movies.Movie_ID Having count(Rating) >= ? order by Avg desc Limit ? "
    Movie_N = []
    
    entry = datatier.select_n_rows(dbConn, sql, [min_num_reviews,N])
    if(entry is not None):
       
        for work in entry:
         add = MovieRating(work[0], work[1], work[2], work[3], round(work[4],2))
         Movie_N.append(add)
  

    return Movie_N






##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).

def add_review(dbConn, movie_id, rating):
    sql2 = "SELECT count(Movie_ID) from Movies where Movie_ID = ?" #  used to Check if movie exists
    result1 = datatier.select_one_row(dbConn,sql2,(movie_id,))
    if(result1[0] == 0):
        return 0
    sql = "Insert Into Ratings(Movie_ID, Rating) Values(?,?)"
    result = datatier.perform_action(dbConn, sql,[movie_id, rating])
    if result <=0:
        return 0
    
    return 1


##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
    sql = "Select Movies.Movie_ID, Tagline from Movies Left join Movie_Taglines on Movies.Movie_ID = Movie_Taglines.Movie_ID where  Movies.Movie_ID = ?" 
 
    result1 = datatier.select_one_row(dbConn,sql,(movie_id,))
    if len(result1) == 0:
        return 0
    
    if result1[1] is None:
        sql = "Insert Into  Movie_Taglines(Movie_ID, Tagline) Values(?,?)" # inserts a new tagline if nonexistent
        result = datatier.perform_action(dbConn, sql,[movie_id, tagline])
        if result <=0:
           return 0

        return 1
    else:
        sql = "Update Movie_Taglines SET Tagline = ? WHERE Movie_ID = ?" # updates a tagline if exists
        result = datatier.perform_action(dbConn, sql,[tagline,movie_id])
        if result <=0:
           return 0
        return 1

