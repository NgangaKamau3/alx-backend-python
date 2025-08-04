def stream_user_ages():
	"""
	Generator function that streams user ages one by one from the database.
	This avoids loading the entire dataset into memory.
	
	Yields:
	    int: Age of each user, one at a time
		"""
	# Simulate database connection setup
	# In a real application: conn = database.connect(...)

	# We'll use batched fetching under the hood for efficiency
	# This is an implementation detail hidden from the caller
	offset = 0
	batch_size  = 100 # Process in small batches for efficiency

	while True:
		# Construct SQL query to fetch a batch of user records
		# Note: We're NOT using SQL's AVG function as required
		query = f"SELECT age from users LIMIT {batch_size} OFFSET {offset}"
		