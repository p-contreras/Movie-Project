def uno():
	print('stuff uno')

def dos():
	print('stuff dos')

def main():
	uno()
	dos()

	info = {"Date": '28-07-2020', 
			"Theme": "Action", 
			"People": ["Ringo", "George", "Paul", "John"], 
			"Movie Choices": {"Ringo": ["TDK", "T2"], 
								"George": ["Saw", "Rocketman"], 
								"Paul": ["Die Hard", "Matrix"], 
								"John": ["Indiana Jones", "Godfather"]}, 
			"Winner": "Godfather"}

	return info
	
if __name__ == '__main__':
	main()
