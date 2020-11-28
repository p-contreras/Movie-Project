import numpy as np
import random
import operator
import time
import datetime


def vote(obj, num_participants):
	if isinstance(obj, dict):
		choices = obj["Choices"]
		n_choices = {}
		for person in choices:
			print("These are the two options for " + person + ": ", choices[person])
			while True:
				vote1 = int(input("How many people vote for " + choices[person][0] + "? "))
				# second film gets (n - vote1) votes
				vote2 = (num_participants - vote1)
				if vote_check(vote1, vote2, num_participants):
					break
				print("Incorrect number of votes!  Please try again")
			if vote1 > vote2:
				n_choices[person] = choices[person][0]
				print("\n")
			elif vote2 > vote1:
				n_choices[person] = choices[person][1]
				print("\n")
			else:
				print("Coin toss!")
				print("...")
				time.sleep(5)
				result = random.choice(choices[person])
				print(result + " passes!")
				n_choices[person] = result
				print("\n")
		# (ex: {"Nico": "TDK", "Britt": "Saw", "RFs": "T2"}
		return n_choices
	elif isinstance(obj, list):
		while True:
			vote1 = int(input("How many people vote for " + obj[0] + "? "))
			# second film gets (n - vote1) votes
			vote2 = (num_participants - vote1)
			if vote_check(vote1, vote2, num_participants):
				break
			print("Incorrect number of votes!  Please try again")
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


def vote_check(vote1, vote2, num_participants):
	return (vote1 >= 0 and vote2 >= 0) and (vote1 + vote2 == num_participants)


def ranking(n_choices):
	# key = person, val = dictionary with movie/tv show rankings
	people = {}
	# key = movie/tv show, val = sum of ranks
	mts = {}
	for person in n_choices:
		# every movie/tv show will start at 0 (i.e., TDK: 0)
		mts[n_choices[person]] = 0
		print([n_choices[p] for p in n_choices])
		print(person + ", these are the options available.  Please rank them from best to worst!")
		# ex: {1: "TDK", 2: "Taxi Driver", 3: "Casino"}
		mts_ranks = {}
		for i in range(1, len(n_choices) + 1):
			while True:
				choice = input("#" + str(i) + "? ")
				if choice in [n_choices[p] for p in n_choices]:
					break
				print("Please type in the movie correctly!  (Case sensitive)")
			mts_ranks[i] = choice
		# each person has their own dictionary of movies and their ranks
		# ex: {"John": {1: "TDK", 2: "Taxi Driver", 3: "Casino"}, 
		#	   "Paul": {1: "Casino", 2: "Taxi Driver", 3: "TDK"},
		#      "George": {1: "TDK", 2: "Taxi Driver", 3: "Casino"}}
		people[person] = mts_ranks
		print("\n")
	# tally up the ranks
	for person in people:
		for rank in people[person]:
			choice = people[person][rank]
			mts[choice] += rank
	# sort the dictionary based on the values
	mts = dict(sorted(mts.items(), key = operator.itemgetter(1)))
	print("mts is: ", mts)
	print("\n")
	# ex: mts = {"TDK": 5, "Casino": 6, "Taxi Driver": 7}
	if len(mts) == 3:
		# every movie has the same number
		all_tie = list(mts.values())[0] == list(mts.values())[2]
		# last two are tied
		last_two_tied = list(mts.values())[1] == list(mts.values())[2]
		if all_tie:
			dists = random_number(n_choices)
			people = list(dists.keys())
			pair = [n_choices[person] for person in people[1:]]
			print(pair)
			final = [n_choices[people[0]], vote(pair, len(n_choices))]
			return final
		elif last_two_tied:
			pair = [choice for choice in list(mts.keys())[1:]]
			final = [list(mts.keys())[0], vote(pair, len(n_choices))]
			return final
		else:
			final = [choice for choice in list(mts.keys())[:2]]
			print("final is: ", final)
			return final
	else:
		while len(mts) > 4:
			mts.popitem()
		ranks = [mt for mt in mts]
		return ranks

def random_number(n_choices):
	dists = {}
	r_number = random.randint(0, 100)
	for person in n_choices:
		dists[person] = int(input(person + ", choose a number between 0 and 100. "))
		dists[person] = abs(r_number - dists[person])
	# dictionary with each person and dist from random number
	dists = dict(sorted(dists.items(), key = operator.itemgetter(1)))
	# minimum dist
	minimum = min(dists.values())
	# if there's a minimum dist, we have a winner
	if sum(minimum == np.array(list(dists.values()))) == 1:
		return dists
	# if we have a tie, we repeat
	else:
		return random_number(n_choices)
	

def main():
	day = datetime.datetime.today()
	mt = input("Are we voting for a movie or a tv show? ").lower()
	if mt == "movie":
		sql_table = "Movies"
		theme = input("What's the movie theme for tonight? ")
	else:
		sql_table = "TV_Shows"
		theme = "NULL"
	num_people = int(input("How many people are participating? "))
	people = [input("Input a name: ") for person in range(num_people)]
	print("\n")
	# people as keys and movie/tv lists as values
	choices = dict()
	for name in people:
		choice1 = input(("1st {} for " + name + "? ").format(mt))
		choice2 = input(("2nd {} for " + name + "? ").format(mt))
		# each person has two movies/tv shows
		choices[name] = [choice1, choice2]
		print("\n")

	info = {"Date": day, "Type": mt, "SQL Table": sql_table, "Theme": theme, 
			"People": people, "Choices": choices}
	print("\n")

	# ROUND 1
	# should finish with n films/tv shows
	n_choices = vote(info, len(info["People"]))
	print("\n")
	print("n_choices is: ", n_choices)

	# RANKING
	semis = ranking(n_choices)
	print(semis)

	# PAIRING/FINAL
	if len(semis) == 4:
		# 1 v 4
		pairing1 = [semis[0], semis[3]]
		# 2 v 3
		pairing2 = [semis[1], semis[2]]
		print("The first pairing is:", pairing1)
		winner1 = vote(pairing1, len(info["People"]))
		print("The second pairing is:", pairing2)
		winner2 = vote(pairing2, len(info["People"]))
		print("FINAL!", [winner1, winner2])
		info["Winner"] = vote([winner1, winner2], len(info["People"]))
		print("And the winner is ... " + info["Winner"] + "!")
	elif len(semis) == 2:
		print("FINAL!", semis)
		info["Winner"] = vote(semis, len(info["People"]))
		print("And the winner is ... " + info["Winner"] + "!")

	print('RFs is a Jedi')

	return info


if __name__ == '__main__':
	main()
