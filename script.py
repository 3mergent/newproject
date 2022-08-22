import requests
from bs4 import BeautifulSoup

def main():
	# Begin input
	movie = input_movie()
	get_movie_data(movie)


def find_movie_id(movie):

	searchUrl = ("https://www.imdb.com/find?q=" + movie)

	# Request IMDB search page
	src = requests.get(searchUrl)
	soup = BeautifulSoup(src.text,'html.parser')
	
	# Select first result and retrieve URL phrase & create ID from it
	soup = soup.find('td', class_='result_text')
	movieUrl = soup.find('a', href=True)['href']
	movieID = movieUrl.split('/')
	movieID = movieID[2]

	return movieID

def make_url_ready(string):
	strings = string.split(" ")
	url_string = "+".join(strings)

	return url_string

def get_movie_data(movieID):

	moviePage = ("https://www.imdb.com/title/" + movieID + "/")

	# Request IMDB search page
	src = requests.get(moviePage)
	soup = BeautifulSoup(src.text,'html.parser')
	soup = soup.find('body') # Is it worth reducing size?

	# Get full title
	movieTitle = soup.find('h1').get_text()

	# Get release date
	dateSoup = soup.find('li', attrs={'data-testid':'title-details-releasedate'})
	dateSoup = dateSoup.find('li')
	movieDate = dateSoup.find('a').get_text()

	# Get rating
	ratingSoup = soup.find('div', 'rating-bar__base-button')
	movieRating = ratingSoup.find('span').get_text()

	# Get Language
	languageSoup = soup.find('li', attrs={'data-testid':'title-details-languages'})
	languageSoup = languageSoup.find('li')
	movieLanguage = languageSoup.find('a').get_text()

	# Get Directors
	directorSoup = soup.find('section', "title-cast--movie")
	directorSoup = directorSoup.find('ul', 'ipc-metadata-list').find('li')
	directorSoup = directorSoup.findAll('a')

	directors = []

	for director in directorSoup:
	 	movieDirector = director.get_text()
	 	directors.append(movieDirector)

	movieDirectors = directors

	# Get Cast
	castSoup = soup.findAll('div', attrs={'data-testid':'title-cast-item'})

	castMembers = []

	for actor in castSoup:
		castMember = actor.find('a', attrs={'data-testid':'title-cast-item__actor'}).get_text()
		castMembers.append(castMember)


	movieCast = castMembers



	print("Title: " + movieTitle)
	print("Release: " + movieDate)
	print("Rating: " + movieRating)
	print("Language: " + movieLanguage)
	print("Cast: ")
	print(movieCast)
	print("Director: ")
	print(movieDirectors)



# def get_actor_data():
# 	pass


# def input_type():
# 	# Take input for query type, actor or movie
# 	print("Actor or Movie?")

# 	query = input(": ")
# 	cleanquery = str.lower(query)

# 	if cleanquery == 'actor':
# 		input_actor()
# 	elif cleanquery == 'movie':
# 		input_movie()
# 	else:
# 		print("Invalid entry.")

# def input_actor():
# 	# Take input for actor name
# 	print ("Actor Name:")

# 	query = input(": ")
# 	cleanquery = str.lower(query)

# 	print("Perform scrape for actor: " + query)

def input_movie():
	# Take input for movie name
	print ("Movie Name:")

	query = input(": ")
	cleanQuery = str.lower(query)

	output = find_movie_id(cleanQuery)

	return output

# Run Main
main()