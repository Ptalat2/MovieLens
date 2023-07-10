import sqlite3
import objecttier


## Preet Talati
## Date: 3/1/23
## Description: A program that reads and updates the MovieLens database in SQLite

##################################################################  
# 
# stats
# Prints the total # of movies and reviews in the MovieLens database
#
def stats(db):
    movies = objecttier.num_movies(db)
    reviews = objecttier.num_reviews(db)

    print("General Stats:")
    print("  # of movies:", f"{movies:,}")
    print("  # of reviews:", f"{reviews:,}")
    print()

##################################################################  
 
# 
# one // command 1
# Given part of a movie name this function outputs the number of movies found
# with its title and release year
# However, if the # of movies found is capped of at 100
# Each element is a Tuple returned through a class object
# 
def one(db):
    print()
    movie_name = input("Enter movie name (wildcards _ and % supported): ")
    movies = objecttier.get_movies(db, movie_name)

    if movies != None:
        print()
        print("# of movies found:", len(movies))
        print()
        if len(movies) > 100:
            print()
            print("There are too many movies to display, please narrow your search and try again...")
        elif len(movies) == 0:
            pass
        else:
            for movie in movies:
                print(movie.Movie_ID,":", movie.Title,f"({movie.Release_Year})" )
        
    else:
         print("# of movies found:", 0)



##################################################################  
# two # // command 2
# Given a movie Id the Function outputs the Id, title release date, 
# runtime, Language, Budget Revenue, # of reviews, avg rating movie genres, 
# associated companies and the tagline. 
# Each element is a Tuple returned through a class object
# 
def two(db):
    print()
    id = input("Enter movie id: ")
    movie = objecttier.get_movie_details(db,id )
    print()
    if movie != None:
       
            print(movie.Movie_ID,":",movie.Title)
            print(" Release date:",movie.Release_Date)
            print(" Runtime:", movie.Runtime, "(mins)")
            print(" Orig language:", movie.Original_Language)
            print(" Budget:", f"${movie.Budget:,}", "(USD)")
            print(" Revenue:", f"${movie.Revenue:,}", "(USD)")
            print(" Num reviews:", movie.Num_Reviews)
            print(" Avg rating:", f"{movie.Avg_Rating:.2f}", "(0..10)")
            print(" Genres:", end = "")
            for entry in movie.Genres:
                print( "",entry,end=',')
            print()
          
            print(" Production companies:", end = "")
            for entry in  movie.Production_Companies:
                print( "",entry,end=',')
            print()

            print(" Tagline:", movie.Tagline)
    else:
         print("No such movie...")



##################################################################
#
#  three // command 3 
#  Outputs the top N movies based on their average rating 
#  with a minimum number of reviews.
#  Each element is a Tuple returned through a class object
#  
def three(db):
   
    N = int(input("\nN? "))
    
    if(int(N) <=0):
        print("Please enter a positive value for N...")
        return

    else:
     Max = int(input("min number of reviews? "))
     if(Max <= 0 ):
        print("Please enter a positive value for min number of reviews...")
        
     else:
        print()
        movies = objecttier.get_top_N_movies(db, int(N),int(Max))
        
    
        for movie in movies:
            print(movie.Movie_ID, ":", movie.Title, f"({movie.Release_Year}),", f"avg rating = {movie.Avg_Rating:.2f}", f"({movie.Num_Reviews} reviews)" )

    



#####################################################################
#
#  four // command 4
#  Given a rating (0-10) and movie_id we 
#  insert a new review into the database.
#  This is done through method of the objecttier
#
def four(db):
    ratin = input("\nEnter rating (0..10): ")

    if int(ratin) <0 or int(ratin) >10:
        print("Invalid rating...")
    
    else:
        id = int(input("Enter Movie id: "))
        yes = objecttier.add_review(db, int(id),int(ratin))
        
        if yes != 1:
            print("\nNo such movie...")
        else:
            print("\nReview successfully inserted")





#####################################################################
#
#  five // command 5
#  Given a tagline and movie_id we 
#  insert a new tagline into the database if it does not exit
#  Otherwise it updates it 
#  This is done through method of the objecttier
#
def five(db):
    tagline = input("\ntagline? ")
    id = int(input("movie id? "))
    yes = objecttier.set_tagline(db, int(id),tagline)
    if(yes ==0):
        print("\nNo such movie...")
    else:
        print("\nTagline successfully set")




#################################################################################


#
# main
#
# The body of code below calls the commands
# A loop will run and keep prompted for a command(1-5) until x is 
# given as an input
#
print('** Welcome to the MovieLens app **')

dbConn = sqlite3.connect('MovieLens.db')
stats(dbConn)

cmd = input("Please enter a command (1-5, x to exit): ")

while cmd != "x":
    if cmd == "1":
        one(dbConn)
    elif cmd == "2":
         two(dbConn)

    elif cmd == "3":
        three(dbConn)

    elif cmd == "4":
        four(dbConn)
    
    elif cmd == "5":
        five(dbConn)

       
    else:
        print("**Error, unknown command, try again...")

    print()
    cmd = input("Please enter a command (1-5, x to exit): ")

dbConn.close()
#
# done
#
