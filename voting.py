import random
import operator
import time
import datetime


# "mt" = movie or tv show

def vote(obj, num_participants):
	if isinstance(obj, dict):
		mt_choices = obj["Choices"]
		n_mts = {}
		for person in mt_choices:
			print("These are the two options for " + person + ": ", mt_choices[person])
			while True:
				vote1 = int(input("How many people vote for " + mt_choices[person][0] + "? "))
				# second film gets (n - vote1) votes
				vote2 = (num_participants - vote1)
				if vote_check(vote1, vote2, num_participants):
					break
				print("Incorrect number of votes!  Please try again")
			if vote1 > vote2:
				n_mts[person] = mt_choices[person][0]
				print("\n")
			elif vote2 > vote1:
				n_mts[person] = mt_choices[person][1]
				print("\n")
			else:
				print("Coin toss!")
				print("...")
				time.sleep(5)
				result = random.choice(mt_choices[person])
				print(result + " passes!")
				n_mts[person] = result
				print("\n")
		# (ex: {"Nico": "TDK", "Britt": "Saw", "RFs": "T2"}
		return n_mts
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


def ranking(mts_dict):
	# key = person, val = dictionary with movie/tv show rankings
	people = {}
	# key = movie/tv show, val = sum of ranks
	mts = {}
	for person in mts_dict:
		# every movie/tv show will start at 0 (i.e., TDK: 0)
		mts[mts_dict[person]] = 0
		print([mts_dict[mt] for mt in mts_dict])
		print(person + ", these are the options available.  Please rank them from best to worst!")
		mts_ranks = {}
		for i in range(1, len(mts_dict) + 1):
			while True:
				mt = input("#" + str(i) + "? ")
				if mt in [mts_dict[x] for x in mts_dict]:
					break
				print("Please type in the movie correctly!  (Case sensitive)")
			mts_ranks[i] = mt
		# each person has their own dictionary of movies and their ranks
		people[person] = mts_ranks
		print("\n")
	# tally up the ranks
	for person in people:
		for rank in people[person]:
			mt = people[person][rank]
			mts[mt] += rank
	# sort the dictionary based on the values
	mts = dict(sorted(mts.items(), key=operator.itemgetter(1)))
	if len(mts) == 3:
		mts.popitem()
		final = [mt for mt in mts]
		return final
	while len(mts) > 4:
		mts.popitem()
	ranks = [mt for mt in mts]
	return ranks


def main():
	day = datetime.datetime.today()
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
	info = {"Date": day, "Type": mt, "Theme": theme, "People": people, "Choices": mt_dict}
	print("\n")
	# ROUND 1
	# should finish with n films/tv shows
	n_mts = vote(info, len(info["People"]))
	print("\n")
	# RANKING
	semis = ranking(n_mts)
	print("These are the remaining options! ", semis)
	time.sleep(3)
	# PAIRING/FINAL
	if len(semis) > 2:
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
	else:
		print("FINAL!", semis)
		info["Winner"] = vote(semis, len(info["People"]))
		print("And the winner is ... " + info["Winner"] + "!")

	print(info)
	print('RFs is a Jedi')

	return info


if __name__ == '__main__':
	main()
