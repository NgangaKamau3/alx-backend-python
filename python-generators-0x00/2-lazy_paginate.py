def paginate_users(page_size, offset):
	"""
	Fetches a page of users from a database.
	Args:
	    page_size(int): Number of users to fetch per page
		offset(int): Starting position for fetching users
		
	Returns:
	    list: A list of user records for the requested page"""
	
	# Simulating database connection
	# In a real application, you would use a proper database connection
	# Example with sqlite3:
	# conn = sqlite3.connect('users.db')
	# cursor = conn.cursor()

	# Constructing the SQL query with LIMIT and OFFSET for pagination
	query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"

	# simulating execution of the query
	# In a real application:
	# cursor.execute(query)
	# results = cursor.fetchall()

	# For simulation purposes, generating mock results
	# Assuming we have 100 users in the database
	all_users = [{"id": i, "name": f"User {i}", "email": f"User{i}@example.com"} for i in range (1, 101)]

	# Calculate which users to return based on LIMIT and OFFSET
	start_index = offset																					
	end_index = min(offset + page_size, len(all_users))

	# Return empty list if we're out of range
	if start_index >= len(all_users):
		return []
	
	# Log the query that would be executed
	print(f"Executing query: {query}")

	return all_users[start_index:end_index]


def lazy_paginate_users(page_size):
	"""
	Generator function that lazily loads pages of users from a database.
	Only fetches the next page when needed.

	Args:
	    page_size(int): Number of users to fetch per page

	Yields:
	    list: A list of user records for the current page"""

	offset = 0
	while True:
		current_page = paginate_users(page_size, offset)
		if not current_page:
			break

		# Yield each user record individually
		for user in current_page:
			yield user

			
	    # Update offset for the next page
		offset += page_size				 