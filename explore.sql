SELECT *
FROM Movies;

SELECT *
FROM Voting_Data;

SELECT *
FROM Voting_Info;

SELECT *
FROM People;

SELECT Voting_Data.Date, Voting_Data.Theme, Movies.Title, Voting_Data.Winner_Movie_ID
FROM Voting_Data INNER JOIN Movies
	WHERE Voting_Data.Winner_Movie_ID = Movies.Movie_ID;

SELECT Voting_Info.Voting_Data_ID, Voting_Data.Date, Voting_Data.Theme, People.Name,
		Movies.Movie_ID, Movies.Title
FROM Voting_Info INNER JOIN Voting_Data
	ON Voting_Info.Voting_Data_ID = Voting_Data.ID
    INNER JOIN Movies
    ON Voting_Info.Movie_ID = Movies.Movie_ID
    INNER JOIN People
    ON Voting_Info.People_ID = People.People_ID;
