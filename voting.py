import random, operator, time
from datetime import date


def vote(obj, num_participants):
	if len(obj) > 2:
		t = obj["Type"]
		mt_choices = obj["%s Choices" % t]
		mts = {}
		for person in mt_choices:
			print(("These are the two %s" + "s for " + person + ": ") % t.lower(), mt_choices[person])
			vote1 = int(input("How many people vote for " + mt_choices[person][0] + "? "))
			# second film gets (n - vote1) votes
			vote2 = (num_participants - vote1)
			if vote1 > vote2:
				mts[person] = mt_choices[person][0]
				print("\n")
			elif vote2 > vote1:
				mts[person] = mt_choices[person][1]
				print("\n")
			else:
				print("Coin toss!")
				print("...")
				time.sleep(5)
				result = random.choice(mt_choices[person])
				print(result + " passes!")
				mts[person] = result
				print("\n")
		# (ex: {"Nico": "TDK", "Britt": "Saw", "RFs": "T2"}
		return mts
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


def RANKING(movie_dict):
	# key = person, val = dictionary with movie rankings
	people = {}
	# key = movie, val = points?
	movies = {}
	for person in movie_dict:
		# every movie will start at 0 (i.e., TDK: 0)
		movies[movie_dict[person]] = 0
		print([movie_dict[movie] for movie in movie_dict])
		print(person + ", these are the films available.  Please rank your top 4 (or 3) from best to worst!")
		movie_ranks = {}
		for i in range(1, len(movie_dict) + 1):
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
		final = [movie for movie in movies]
		return final
	else:
		ranks = [movie for movie in movies]
		return ranks


def main():
	day = date.today()
	mt = int(input("Are we voting for a movie or a tv show?  (For movie type 0, for tv show type 1) "))
	mt = "Movie" if mt == 0 else "TV Show"
	if mt == "Movie":
		theme = input("What's the movie theme for tonight? ")
	else:
		theme = "NULL"
	num_people = int(input("How many people are there in the table? "))
	people = [input("Input a name: ") for person in range(num_people)]
	print("\n")
	# people as keys and movie/tv lists as values
	mt_dict = dict()
	for name in people:
		choice1 = input(("1st %s for " + name + "? ") % mt.lower())
		choice2 = input(("2nd %s for " + name + "? ") % mt.lower())
		# each person has two movies/tv shows
		mt_dict[name] = [choice1, choice2]
		print("\n")
	info = {"Date": day, "Type": mt, "Theme": theme, "People": people, "%s Choices" % mt: mt_dict}
	print("\n")
	# ROUND 1
	# key = person, val = 1 film/tv show
	# should finish with n films/tv shows
	n_films = vote(info, len(info["People"]))
	print("\n")
	# RANKING
	semis = RANKING(n_films)
	# PAIRING/FINAL
	if len(semis) > 2:
		# 1 v 4
		pairing1 = [semis[0], semis[3]]
		# 2 v 3
		pairing2 = [semis[1], semis[2]]
		winner1 = vote(pairing1, len(info["People"]))
		winner2 = vote(pairing2, len(info["People"]))
		print("FINAL!")
		info["Winner"] = vote([winner1, winner2], len(info["People"]))
		print("And the winner is ... " + info["Winner"] + "!")
	else:
		print("FINAL!")
		info["Winner"] = vote(semis, len(info["People"]))
		print("And the winner is ... " + info["Winner"] + "!")

	print('RFs is a Jedi')
	
	return info

	


if __name__ == '__main__':
	main()
