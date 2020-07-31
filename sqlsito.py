import mysql.connector

import voting


DB = 'msp'
TEST = 1

def write_data(cnx, table_name, mdict):
	crs = cnx.cursor()

	if table_name == 'Movies':

		sql_statement = "INSERT INTO Movies(Title,Test) VALUES (\""

		for i in range(len(mdict['Movie List'])):
			sql_statement += mdict['Movie List'][i]

			if i == len(mdict['Movie List']) -1:
				sql_statement += '\",%s)' %(TEST)
			else:
				sql_statement += '\",%s),(\"' %(TEST)

#####THIS IS WHERE I LEFT OFF 7/30				
	else:
		print('Table is something else')
	
	print(sql_statement)

	try:
		print('Executing statement...')
		crs.execute(sql_statement)
		print('Execution complete.')
	except Exception as e:
		print(e)

	try:
		print('Commiting changes to db...')
		cnx.commit()
		print('Commit complete.')
	except Exception as e:
		print(e)

def new_movie_dict(mdict):
	movies = []
	for i in mdict['Movie Choices']:
		for m in mdict['Movie Choices'][i]:
			movies.append(m)

	mdict['Movie List'] = movies

	return mdict

def close_connection(cnx):
	print('Closing connection...')
	try:
		cnx.close()
		print('Connection = closed')
	except Exception as e:
		print('Something happened, cannot close connection.  Error -', e)

def start_connection(db_name):
	try:
		print('Attempting connection...')
		connection = mysql.connector.connect(user = 'root',
								password = 'themiskyrifus_db',
								host = '192.168.1.106',
								database = db_name)
		print('Connection successful')
		return connection

	except Exception as e:	
		print('Error while connecting:', e)
		return None

def main():
	print('hello Rifus')

	movie_dict = voting.main()
	#movie_dict = {"Date": "28-07-2020", "Theme": "Action", "People": ["Ringo", "George", "Paul", "John"], "Movie Choices": {"Ringo": ["TDK", "T2"], "George": ["Saw", "Rocketman"], "Paul": ["Die Hard", "Matrix"], "John": ["Indiana Jones", "Godfather"]}, "Winner": "Godfather"}

	movie_dict = new_movie_dict(movie_dict)

	conn = start_connection(DB)

	if conn is not None:
		#Movie table
		write_data(conn, 'Movies', movie_dict)

		close_connection(conn)
	else:
		print('goodbye')

	
	print('I am a Jedi')

if __name__ == '__main__':
	main()