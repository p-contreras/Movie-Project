import random, operator, time
from datetime import date


def vote(obj, num_participants):
	if len(obj) > 2:
		films = {}
		for person in obj:
			print("These are the two films for " + person + ": ", obj[person])
			vote1 = int(input("How many people vote for " + obj[person][0] + "? "))
			# second film gets (n - vote1) votes
			vote2 = (num_participants - vote1)
			if vote1 > vote2:
				films[person] = obj[person][0]
				print("\n")
			elif vote2 > vote1:
				films[person] = obj[person][1]
				print("\n")
			else:
				print("Coin toss!")
				print("...")
				time.sleep(5)
				result = random.choice(obj[person])
				print(result + " passes!")
				films[person] = result
				print("\n")
		return films
	elif len(obj) == 2:
		print("The two movies are:", obj)
		vote1 = int(input("How many people vote for " + obj[0] + "? "))
		# second film gets (n - vote1) votes
		vote2 = (num_participants - vote1)
		if vote1 > vote2:
			return obj[0]
		elif vote2 > vote1:
			return obj[1]
		else:
			print("Coin toss!")
			time.sleep(5)
			result = random.choice(obj)
			print(result + " passes")
			return result


def RANKING(movie_info):
	# key = person, val = dictionary with movie rankings
	people = {}
	# dictionary of size n
	n_films = movie_info[1]
	# key = movie, val = points?
	movies = {}
	for person in n_films:
		# every movie will start at 0 (i.e., TDK: 0)
		movies[n_films[person]] = 0
		print([n_films[movie] for movie in n_films])
		print(person + ", these are the films available.  Please rank your top 4 (or 3) from best to worst!")
		movie_ranks = {}
		for i in range(1, len(n_films) + 1):
			movie = input("#" + str(i) + "? ")
			movie_ranks[i] = movie
		# each person has their own dictionary of movies and their ranks
		people[person] = movie_ranks
		print("\n")
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
		return movie_info
	else:
		movie_info[1] = [movie for movie in movies]
		return movie_info


def main():
	day = date.today()
	theme = input("What's the movie theme for tonight? ")
	people = []
	num_people = int(input("How many people are there in the table? "))
	for person in range(num_people):
		name = input("Input a name: ")
		people.append(name)
	print("\n")
	# people as keys and movie lists as values
	movie_dict = dict()
	for name in people:
		movie1 = input("1st movie for " + name + "? ")
		movie2 = input("2nd movie for " + name + "? ")
		# each person has two movies
		movie_dict[name] = [movie1, movie2]
		print("\n")
	info = [{"Date": day, "Theme": theme, "People": people, "Movie Choices": movie_dict}]
	print("\n")
	# ROUND 1
	# key = person, val = 1 film
	# should finish with n films
	n_films = vote(movie_dict, len(info["People"]))
	info.append(n_films)
	print("\n")
	# RANKING
	info = RANKING(info)
	# PAIRING/FINAL
	if len(info[1]) > 2:
		movies = info[1]
		# 1 v 4
		pairing1 = [movies[0], movies[3]]
		# 2 v 3
		pairing2 = [movies[1], movies[2]]
		winner1 = vote(pairing1, len(info["People"]))
		winner2 = vote(pairing2, len(info["People"]))
		print("FINAL!")
		winner = vote([winner1, winner2], len(info["People"]))
		info.append(winner)
		print("And the winner is ... " + winner + "!")
		return info
	else:
		print("FINAL!")
		winner = vote(info[1], len(info["People"]))
		info.append(winner)
		print("And the winner is ... " + winner + "!")
		return info


if __name__ == '__main__':
	main()
