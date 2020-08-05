import mysql.connector
import datetime
import sys

import voting

'''
TO-DO - 8/5/2020

1. Check password hashing (encryption)
2. Add unique movie choices
3. Add unique people choices

'''



DB = 'msp'
TEST = input('Is this a TEST? 1 for yes 0 for no')

def movies(mdict):
	sql_statement_movies = "INSERT INTO Movies(Title,Test) VALUES (\""

	for i in range(len(mdict['Movie List'])):
		sql_statement_movies += mdict['Movie List'][i]

		if i == len(mdict['Movie List']) -1:
			sql_statement_movies += '\",%s)' %(TEST)
		else:
			sql_statement_movies += '\",%s),(\"' %(TEST)

	return sql_statement_movies

def people(mdict):
	sql_statement_people = "INSERT INTO People(Name,Test) VALUES (\""

	for i in range(len(mdict['People'])):
		sql_statement_people += mdict['People'][i]

		if i == len(mdict['People']) -1:
			sql_statement_people += '\",%s)' %(TEST)
		else:
			sql_statement_people += '\",%s),(\"' %(TEST)

	return sql_statement_people


def query(cnx, tableName, winningMovie, mdict):

	if winningMovie is not None:
		sql_query = "SELECT * FROM %s WHERE " %(tableName)

		if tableName == 'Movies':
			sql_query += 'Title like \'%s\' ' %(winningMovie)
			#print(sql_query)

		try:
			crs = cnx.cursor(buffered = True)
			crs.execute(sql_query)
		except Exception as e:
			print(e)

		if crs.rowcount > 1:
			print('We have more than one movie matching that Title.  Check the db')
			winning_movie_id = 'IMMOLATION'
		elif crs.rowcount == 1:
			for rifus in crs:
				winning_movie_id = rifus[0]
		else:
			print('Movie is not in the db for some reason. Check the db.')
			winning_movie_id = 'IMMOLATION'

		return winning_movie_id

	else:
		#get all relevant IDs first
		for t in tableName:
			sql_query = "SELECT * FROM %s WHERE " %(t)

			if t == 'Voting_Data':
				sql_query += "Date like '%s%%' ORDER BY Date DESC LIMIT 1" %(datetime.date.today())
				print(sql_query)
				try:
					crs = cnx.cursor(buffered = True)
					crs.execute(sql_query)

					if crs.rowcount == 1:
						for rifus in crs:
							voting_data_id = rifus[0]
					else:
						voting_data_id = 'IMMOLATION'

				except Exception as e:
					print(e)

			elif t == 'People':		
				sql_query += "Name in ("

				for p in mdict['People']:
					if p == mdict['People'][-1]:
						sql_query += '\"%s\")' %(p)
					else:
						sql_query += '\"%s\",' %(p)

				try:
					crs = cnx.cursor(buffered = True)
					crs.execute(sql_query)

					if crs.rowcount > len(mdict['People']):
						print('There are more rows than people in the voting.  Check the db for names.')
						pid = 'IMMOLATION'
					elif crs.rowcount == len(mdict['People']):
						pid = {}
						for rifus in crs:
							pid[rifus[1]] = rifus[0]
					else:
						print('There are less rows than people in the voting.  Check the db for names.')
						pid = 'IMMOLATION'

				except Exception as e:
					print(e)

			elif t == 'Movies':
				sql_query += 'Title in ('

				for m in mdict['Movie List']:
					if m == mdict['Movie List'][-1]:
						sql_query += '\"%s\")' %(m)
					else:
						sql_query += '\"%s\",' %(m)

				try:
					crs = cnx.cursor(buffered = True)
					crs.execute(sql_query)

					if crs.rowcount > len(mdict['Movie List']):
						print('There are more rows than movies in the voting.  Check the db for titles.')
						mid = 'IMMOLATION'
					elif crs.rowcount == len(mdict['Movie List']):
						mid = {}
						for rifus in crs:
							mid[rifus[1]] = rifus[0]
					else:
						print('There are less rows than movies in the voting.  Check the db for titles.')
						mid = 'IMMOLATION'

				except Exception as e:
					print(e)

		return voting_data_id, pid, mid



def voting_info(cnx, mdict):
	sql_statement_voting_info = "INSERT INTO Voting_Info(Voting_Data_ID,People_ID,Movie_ID,Test) VALUES ("

	table_names = ['Voting_Data','People','Movies']

	vd_id, people_ids, movie_ids = query(cnx,table_names,None,mdict)

	if vd_id == 'IMMOLATION' or people_ids == 'IMMOLATION' or movie_ids == 'IMMOLATION':
		print('ERROR: One of these is IMMOLATION')
		print('vd_id',vd_id)
		print('people_ids',people_ids)
		print('movie_ids',movie_ids)

		sql_statement_voting_info == None

	else:
		for i in movie_ids:
			mid = movie_ids[i]

			for p in mdict['Movie Choices']:
				for mc in mdict['Movie Choices'][p]:
					if i == mc:
						pid = people_ids[p]
						if i == list(movie_ids.keys())[-1]:
							sql_statement_voting_info += "%s,%s,%s,%s)" %(vd_id,pid,mid,TEST)
						else:
							sql_statement_voting_info += "%s,%s,%s,%s),(" %(vd_id,pid,mid,TEST)
					else:
						pass

	return sql_statement_voting_info
	

def voting_data(cnx, mdict):
	sql_statement_voting_data = "INSERT INTO Voting_Data(Date,Theme,Num_People,Winner_Movie_ID,Test) VALUES (\""
	
	table_name = 'Movies'

	date = mdict['Date']
	theme = mdict['Theme']
	num_p = len(mdict['People'])
	winner = mdict['Winner']

	winning_movie_id = query(cnx,table_name,winner,None)
	#print(winning_movie_id)

	if winning_movie_id != 'IMMOLATION':
		#print('We have what we need for voting data INSERT')

		sql_statement_voting_data += '%s\",\"%s\",%s,%s,%s)' %(date,theme,num_p,winning_movie_id,TEST)
		#print(sql_statement_voting_data)
	else:
		print('ERROR: Something happened retrieving movie data.')
		sql_statement_voting_data = 'FAIL'

	return sql_statement_voting_data


def write_data(cnx, sqlStatement):

	crs = cnx.cursor()

	for s in sqlStatement:
		#Send statemnt to db
		try:
			print('Executing statement...')
			crs.execute(s)
			print('Execution complete.')

			try:
				print('Commiting changes to db...')
				cnx.commit()
				print('Commit complete.')
			except Exception as e:
				print('ERROR:',e)

		except Exception as e:
			print('ERROR:',e)

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
		print('ERROR: Something happened, cannot close connection.  Error -', e)

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
		print('ERROR: Error while connecting:', e)
		return None

def main():
	print('hello Rifus')

	movie_dict = voting.main()
	#movie_dict = {"Date": str(datetime.datetime.now()), "Theme": "Action", "People": ["Ringo", "George", "Paul", "John"], "Movie Choices": {"Ringo": ["TDK", "T2"], "George": ["Saw", "Rocketman"], "Paul": ["Die Hard", "Matrix"], "John": ["Indiana Jones", "Godfather"]}, "Winner": "Godfather"}

	movie_dict = new_movie_dict(movie_dict)
	print(movie_dict)

	
	conn = start_connection(DB)

	if conn is not None:
		sql_statement = []

		#movies
		sql_statement.append(movies(movie_dict))
		#people
		sql_statement.append(people(movie_dict))

		try:
			print('Writing People and Movie data first...')
			write_data(conn, sql_statement)
			print('Success. People and Movie data inserted')
		except Exception as e:
			print('ERROR: Something happened writing Movie and People data -',e)
			close_connection(conn)
			
			sys.exit('Goodbye')


		sql_statement = []
		#voting data
		sql_statement.append(voting_data(conn,movie_dict))
		

		try:
			print('Writing voting data to db now...')
			write_data(conn, sql_statement)
			print('Success. Voting data inserted')
		except Exception as e:
			print('ERROR: Something happened writing voting data -',e)
			sys.exit('Goodbye')

		sql_statement = []
		#voting info
		sql_statement.append(voting_info(conn,movie_dict))

		try:
			print('Writing voting info to db now...')
			write_data(conn, sql_statement)
			print('Success. Voting info inserted')
		except Exception as e:
			print('ERROR: Something happened writing voting info -',e)
			sys.exit('Goodbye')
		



		close_connection(conn)
	else:
		print('goodbye')

	
	print('I am a Jedi')

if __name__ == '__main__':
	main()