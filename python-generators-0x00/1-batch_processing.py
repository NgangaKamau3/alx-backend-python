def stream_users_in_batches(batch_size):
	"""Fetch userrs in batches of a specified size
	
	Args:
	    batch_size(int): The number of userss to fetch in each batch
		
	Yields:
	    A list of user records"""
	if batch_size <= 0:
	    raise ValueError("Batch size must be a positive integer")
	
	# Assume that a database connection is established
	cursor = db_connection.cursor()

	offset = 0
	while True:
		# Fetch one batch from the our connection
		cursor.execute('SELECT * FROM user_data ORDER BY id LIMIT $s OFFSET $s'
				(batch_size, offset)
				)
		batch= cursor.fetchall()

		# If no more records, stop thie iteration
		if not batch:
			break

		# Move to the next batch
		offset += batch_size

##########################################################################

def batch_processing(batch_size=100):
	"""Process users in batches and filter those over the age of 25
	Args:
	    batch_size(int): The number of users to fetch in each batch
		
	Returns: A list of users above the age of 25"""

	filtered_users = []

	# Use the stream_users_in_batches function written earlier
	for batch in stream_users_in_batches(batch_size):

		# Process each user in the current batch
		for user in batch:
			# Assuming 'user' is a dict or object with an 'age' attribute
			# Adapt this according to your actual data structure
			if user['age'] > 25:
				filtered_users.append(user)
	    # Optionally, you can showcase the number of users that have been generated thus far
		print(f"Processed {len(filtered_users)} so far...")
		return filtered_users
	
###################################################

def stream_users_in_batches(batch_size):
	"""Fetch user rows in batches of specified size
	Args: batch_size(int): The number of users to fetch in each batch
	
	Yields: A list of user records"""
	if batch_size <= 0:
	    raise ValueError("Batch size must be a positive integer")
	
	# Assume that a database connection is established
	cursor = db_connection.cursor()

	offset = 0
	while True:
		# Fetch one batch from our connection
		cursor.execute('SELECT * FROM user_data ORDER BY id LIMIT %s OFFSET %s'
				(batch_size, offset)
				)
		batch = cursor.fetchall()
		# If no more records, stop the iteration	
		if not batch:
			break

		yield batch
		offset += batch_size

def batch_processing(batch_size):
	"""Process users in batches and yield those over the age of 25
	Args: batch_size(int): The number of users in each batch
	Yields: 
	    dict: The number of users above the age of 25"""
	# Use the stream_users_in_batches function
	for batch in stream_users_in_batches(batch_size):
		filtered_count = 0

		#process each user in the current batch
		for user in batch:
			# Yield users over 25 directly instead of collecting in a list
			if user['age'] > 25:
				yield user
				filtered_count += 1


		# Print progress information
		print(f"Processed {filtered_count} users above 25 so far...")