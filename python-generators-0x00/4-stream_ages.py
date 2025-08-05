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
		
		# For simulation purposes only -  in a real app you'd execute the query
		print(f"Executing query: {query}")
		# Simulate fetching the batch of user records
		# In a real application: cursor = conn.cursor(); cursor.execute(query); results = cursor.fetchall()
		# Create simulated data - would be your actual query results
		# Asssume we have 1000 users total
		all_ages = [20 + (i % 60) for i in range(1, 1001)]  # Ages between 20-79

		start_idx = offset
		end_idx = min(offset + batch_size, len(all_ages))

		# Check if we've processed all records
		if start_idx >= len(all_ages):
			break

		# Get the current batch of ages
		current_batch = all_ages[start_idx:end_idx]

		# Yield each age in the current batch
		for age in current_batch:
			yield age

		# Move to the next batch
		offset += batch_size

def calculate_average_age():
	"""
	Calculates the average age of all users in the database.

	Returns:
	    float: Average age of all users
		"""
	total_age = 0
	user_count = 0

	# Iterate over the ages streamed from the database
	for age in stream_user_ages():
		total_age += age
		user_count += 1

	# Calculate and return the average age
	return total_age / user_count if user_count > 0 else 0


# Main execution
if __name__ == "__main__":
	avg_age = calculate_average_age()
	print(f"Average age of users: {avg_age:.2f}")