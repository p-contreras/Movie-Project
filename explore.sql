use msp;

SELECT *
FROM Movies;

DESCRIBE Movies;

SELECT *
FROM TV_Shows;

SELECT *
FROM Voting_Data;

SELECT *
FROM Voting_Info;

SELECT *
FROM People;

SELECT Voting_Data.Date, Voting_Data.Theme, Movies.Title, Voting_Data.Winner_Movie_ID
FROM Voting_Data INNER JOIN Movies
	WHERE Voting_Data.Winner_Movie_ID = Movies.Movie_ID;

SELECT vi.Voting_Data_ID, vd.Date, vd.Theme, p.Name,
		m.Movie_ID, m.Title
FROM Voting_Info vi
	INNER JOIN Voting_Data vd
	ON vi.Voting_Data_ID = vd.ID
    INNER JOIN Movies m
    ON vi.Movie_ID = m.Movie_ID
    INNER JOIN People p
    ON vi.People_ID = p.People_ID;
    
# how many votes per person per voting instance?    
SELECT v.Voting_Data_ID, v.People_ID, p.Name, COUNT(v.People_ID) AS Num_Movies
FROM Voting_Info v
	INNER JOIN People p
    ON v.People_ID = p.People_ID
GROUP BY Voting_Data_ID, People_ID;
