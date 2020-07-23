import random, operator
from datetime import date


def FINAL(movie_info):
	return "rifus is cheese"


def PAIRINGS(movie_info):
	# we'll use ASM pairing method (1 v 4, 2 v 3)
	movies = movie_info[1]
	# 1 v 4
	pairing1 = [movies[0], movies[3]]
	# 2 v 3
	pairing2 = [movies[1], movies[2]]
	print("The two films in this pairing are:", pairing1)
	vote1 = int(input("How many people vote for: " + pairing1[0] + "? "))
	vote2 = len(movie_info[0]["People"]) - vote1
	if vote1 > vote2:
		pairing1.pop()
	elif vote2 > vote1:
		pairing1.pop(0)
	else:
		print("Coin toss!")
		result = random.choice(pairing1)
		print(result + " passes")
		pairing1 = [result]

	print("The two films in this pairing are:", pairing2)
	vote1 = int(input("How many people vote for: " + pairing2[0] + "? "))
	vote2 = len(movie_info[0]["People"]) - vote1
	if vote1 > vote2:
		pairing2.pop()
	elif vote2 > vote1:
		pairing2.pop(0)
	else:
		print("Coin toss!")
		result = random.choice(pairing2)
		print(result + " passes")
		pairing2 = [result]
	# at this point we have our two finalists
	movie_info[1] = [pairing1[0], pairing2[0]]
	return FINAL(movie_info)


def RANKING(movie_info):
	# key = person, val = dictionary with movie rankings
	people = {}
	# dictionary of size n
	n_films = movie_info[1]
	# key = movie, val = points?
	movies = {}
	for person in n_films:
		# every movie will start at 0
		movies[n_films[person]] = 0
		print(n_films.values())
		print("These are the films available.  Please rank your top 4 (or 3) from best to worst!")
		movie_ranks = {}
		for i in range(1, len(n_films) + 1):
			movie = input("#" + str(i) + "? ")
			movie_ranks[i] = movie
		# each person has their own dictionary of movies and their ranks
		people[person] = movie_ranks
	# tally up the ranks
	for person in people:
		for rank in people[person]:
			movie = people[person][rank]
			movies[movie] += rank
	# sort the dictionary based on the values
	movies = dict(sorted(movies.items(), key=operator.itemgetter(1)))
	# if we have 3 films, we go directly to the FINAL
	if len(movies) < 4:
		# remove film with highest number of points
		movies.popitem()
		movie_info[1] = [movie for movie in movies]
		return FINAL(movie_info)
	else:
		movie_info[1] = [movie for movie in movies]
		return PAIRINGS(movie_info)


# this function takes in a dictionary with names as keys and movie lists as values
# returns the dictionary with half the number of films!
def ROUND1(movie_info):
	# key = person, val = 1 film
	n_films = {}
	movie_dictionary = movie_info[0]["Movie Choices"]
	# iterate thru dictionary with 2n films
	# should finish with n films
	for person in movie_dictionary:
		print("These are your two films: ", movie_dictionary[person])
		vote1 = int(input("How many people vote for " + movie_dictionary[person][0] + "? "))
		# second film gets (n - vote1) votes
		vote2 = (len(movie_dictionary) - vote1)
		if vote1 > vote2:
			n_films[person] = movie_dictionary[person][0]
		elif vote2 > vote1:
			n_films[person] = movie_dictionary[person][1]
		else:
			print("Coin toss!")
			result = random.choice(movie_dictionary[person])
			print(result + " passes")
			n_films[person] = result
	# at this point we eliminated n films
	movie_info.append(n_films)
	return RANKING(movie_info)


def movie_choices():
	day = date.today()
	theme = input("What's the movie theme for tonight? ")
	people = []
	num_people = int(input("How many people are there in the table? "))

	for person in range(num_people):
		name = input("Input a name: ")
		people.append(name)

	# people as keys and movie lists as values
	movie_dict = dict()

	for name in people:
		movie1 = input("1st movie for " + name + "? ")
		movie2 = input("2nd movie for " + name + "? ")
		# each person has two movies
		movie_dict[name] = [movie1, movie2]
	info = [{"Date": day, "Theme": theme, "People": people, "Movie Choices": movie_dict}]
	return ROUND1(info)


def main():
	movie_choices()


if __name__ == '__main__':
	main()
