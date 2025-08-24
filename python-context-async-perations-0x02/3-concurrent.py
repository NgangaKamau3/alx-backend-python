import asyncio
import aiosqlite
import os
import time

async def setup_sample_database(db_path):
	"""
	Create a sample database with users table for demonstration purposes.
	"""
	async with aiosqlite.connect(db_path) as db:
		await conn.execute('''
					CREATE TABLE IF NOT EXISTS users (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL,
			    email TEXT UNIQUE NOT NULL,
				age INTEGER
			)
		''')

		sample_users = [
			('John Doe', 'john.doe@example.com', 30),
			('Jane Smith', 'jane.smith@example.com', 25),
			('Bob Johnson', 'bob.johnson@example.com', 35),
			('Alice Williams', 'alice.williams@example.com', 28),
			('Charlie Brown', 'charlie.brown@example.com', 32),
			('David Wilson', 'david.wilson@example.com', 40),
			('Eva Green', 'eva.green@example.com', 29),
			('Frank Castle', 'frank.castle@example.com', 35),
			('Grace Lee', 'grace.lee@example.com', 27),
			('Henry Adams', 'henry.adams@example.com', 45),
			('Isabella Martinez', 'isabella.martinez@example.com', 31),
			('Jack Daniels', 'jack.daniels@example.com', 38)
		]

		await conn.executemany('''
			INSERT INTO users (name, email, age) VALUES (?, ?, ?)
		''', sample_users)
		
		await conn.commit()
		print(f"Sample database setup completed at: {db_path}")
	
async def async_fetch_users():
	"""
	Asynchronously fetch all users from the database.
	Returns:
	    list: All users from the database
	"""
	print("🔍 Fetching users...")
	start_time = time.time()

	db_path = "async_sample_database.db"  # Define db_path within function

	try:
		async with aiosqlite.connect(db_path) as conn:
			await asyncio.sleep(0.1)
			cursor = await conn.execute('SELECT * FROM users')
			users = await cursor.fetchall()
			await cursor.close()

			end_time = time.time()
			print(f"✅ Fetched {len(users)} users in {end_time - start_time:.2f} seconds")

			return users
	
	except Exception as e:
		print(f"❌ An error occurred while fetching users: {e}")
		raise

async def async_fetch_older_users():
	"""
	Asynchronously fetch users older than 40 from the DB
	Returns:
	    list: Users older than 40
		"""
	
	print("🔍 Fetching users older than 40...")
	start_time = time.time()
	db_path = "async_sample_database.db"  # Define db_path within function

	try:
		async with aiosqlite.connect(db_path) as conn:
			await asyncio.sleep(0.1)
			cursor = await conn.execute('SELECT * FROM users WHERE age > ?', (40,))
			users = await cursor.fetchall()
			await cursor.close()

			end_time = time.time()
			print(f"✅ Fetched {len(users)} users older than 40 in {end_time - start_time:.2f} seconds")

			return users
	
	except Exception as e:
			print(f"❌ An error occurred while fetching users: {e}")
			raise
	
async def fetch_concurrently():
	"""
	Execute both database queries concurrently using asyncio.gather()
	Returns:
        tuple: Results from both queries(all_users, older_users)
	"""

	print("\n" + "=" * 60)
	print("🚀 Executing concurrent database queries")
	print("=" * 60)

	start_time = time.time()

	try:
		# Run both fetch functions concurrently using asyncio.gather()
		all_users_task = async_fetch_users()
		older_users_task = async_fetch_older_users()

		all_users, older_users = await asyncio.gather(all_users_task, older_users_task)

		end_time = time.time()
		total_time = end_time - start_time
		

		print(f"✅ Concurrent queries completed in {total_time:.3f} seconds")
		print("=" * 60)

		return all_users, older_users
	
	except Exception as e:
		print(f"❌ An error occurred during concurrent execution: {e}")
		raise

async def fetch_concurrently_with_path(db_path):
	"""
	Execute both database queries concurrently with asycio.gather()
	
	Args:
	    db_path (str): Path to the database file
		
	Returns:
	    tuple: Results from both queries (all_users, older_users)
	"""
	print("\n" + "=" * 60)
	print("🚀 Executing concurrent database queries")
	print("=" * 60)

	start_time = time.time()

	try:
		# Run both fetch functions concurrently using asyncio.gather()
		all_users_task = async_fetch_users()
		older_users_task = async_fetch_older_users()

		all_users, older_users = await asyncio.gather(all_users_task, older_users_task)

		end_time = time.time()
		total_time = end_time - start_time

		print(f"✅ Concurrent queries completed in {total_time:.3f} seconds")
		print("=" * 60)

		return all_users, older_users

	except Exception as e:
		print(f"❌ An error occurred during concurrent execution: {e}")
		raise

def display_results(all_users, older_users):
	"""
	Display the results of the database queries.
	Args:
	    all_users (list): List of all users
	    older_users (list): List of users older than 40
	"""
	print("\n" + "=" * 60)
	print("📊 Displaying Results:")
	print("=" * 60)

	print("All Users:")
	for user in all_users:
		print(user)

	print("\nUsers Older Than 40:")
	for user in older_users:
		print(user)

async def main():
	"""
	Main function to demonstrate concurrent execution of database queries.
	"""
	db_path = "async_sample_database.db"

	# Setup sample database
	await setup_sample_database(db_path)

	# Execute queries concurrently
	all_users, older_users = await fetch_concurretly()

	# Display results
	display_results(all_users, older_users)

	# Cleanup - remove sample database
	try:
		os.remove(db_path)
		print(f"Sample database file '{db_path}' removed.")
	except OSError:
		pass

def run_concurrent_queries():
	"""
	Entry point function using asyncio.run()
	"""
	print("Starting concurrent database queries")
	print("Using aiosqlite for async DB operations")
	print("Using asyncio.gather() for concurrent execution")

	asyncio.run(main())

if __name__ == "__main__":
	run_concurrent_queries()