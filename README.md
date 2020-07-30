# Movie-Project

voting.py
	output object:  dictionary
	e.g: {"Date": 28-07-2020, 
			"Theme": "Action", 
			"People": ["Ringo", "George", "Paul", "John"], 
			"Movie Choices": {"Ringo": ["TDK", "T2"], 
								"George": ["Saw", "Rocketman"], 
								"Paul": ["Die Hard", "Matrix"], 
								"John": ["Indiana Jones", "Godfather"]}, 
			"Winner": "Godfather"}
			
{"Date": "28-07-2020", "Theme": "Action", "People": ["Ringo", "George", "Paul", "John"], "Movie Choices": {"Ringo": ["TDK", "T2"], "George": ["Saw", "Rocketman"], "Paul": ["Die Hard", "Matrix"], "John": ["Indiana Jones", "Godfather"]}, "Winner": "Godfather"}


DB name: msp

TABLES: Movies, Voting_Data, People, Voting_Info

- Movies: ID, Title
- Voting_Data: ID, Date, Theme, Num_People, Winner_Movie_ID
- People: ID, Name
- Voting_Info: ID, Voting_Data_ID, People_ID, Movie_ID
