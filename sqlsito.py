import mysql.connector

import voting

CLOSE_CONNECTION = 'Y'
DB = 'msp'


def write_data(cnx, table_name, mdict):
	crs = cnx.cursor()

	if table_name = 'Movies':

		sql_statement = '''INSERT into Movies(Title)
							VALUES ('''

		for i in range(len(mdict['Movie List'])):
			sql_statement += mdict['Movie List'][i]

			if i == len(mdict['Movie List']) -1:
				sql_statement += ')'
			else:
				sql_statement += '),('

#####THIS IS WHERE I LEFT OFF				
	elif table_name

	try:
		crs.execute(sql_statement)
	except Exception as e:
		print(e)

	try:
		cnx.commit()
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
	except Exception as e:
		print('Something happened, cannot close connection.  Error -', e)

def start_connection(db_name):
	try:
		print('Attempting connection...')
		connection = connect(user = 'root',
								password = 'password',
								host = '192.168.0.1',
								database = db_name)
		print('Connection successful')

	except Exception as e:	
		print('Error while connecting:', e)

	if connection:
		return connection
	else:
		return None

def main():
	print('hello Rifus')

	movie_dict = voting.main()

	movie_dict = new_movie_dict(movie_dict)

	conn = start_connection(DB)

	if conn is not None:
		#Movie table
		write_data(conn, 'Movies', movie_dict)
		
	else:
		print('goodbye')

	close_connection(conn)
	print('I am a Jedi')

if __name__ == '__main__':
	main()