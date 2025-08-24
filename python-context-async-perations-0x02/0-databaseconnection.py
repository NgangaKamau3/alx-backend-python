import sqlite3
import os


class DatabaseConnection:
	"""
	A custom class-based context manager for handling database connections.
	Automatically opens connection on enter and closes on exit.
	"""

	def __init__(self, database_path):
		"""
		Initialise the context manager with database path.
		Args:
		    database_path(str): Path to the database file
			"""
		self.database_path = database_path
		self.connection = None
		self.cursor = None

	def __enter__(self):
		"""
		Enter the context manager - establish database connection.
		
		Returns:
		    sqlite3.cursor: Database cursor for executing queries
			"""
		try:
			print(f"Opening database connection to: {self.database_path}")
			self.connection = sqlite3.connect(self.database_path)
			self.cursor = self.connection.cursor()
			print(f"Database connection established successfully.")
			return self.cursor
		except sqlite3.Error as e:
			print(f"Error establishing database connection: {e}")
			raise

	def __exit__(self, exc_type, exc_value, traceback):
		"""
		Exit the context manager - clean up database connection.
		
		Args:
		    exc_type: Exception type (if any)
		    exc_value: Exception value (if any)
		    traceback: Traceback object (if any)
			"""
		if self.cursor:
			self.cursor.close()
			print("Database cursor closed.")
		if self.connection:
			if exc_type is None:
				self.connection.commit()
				print("Transaction committed.")
			else:
				self.connection.rollback()
				print(f"Transaction rolled back due to: {exc_value}")
			
			self.connection.close()
			print("Database connection closed.")

		return False  # Propagate exceptions if any
	

	def setup_sample_database(db_path):
		"""
		Create a sample database with users table for demoing
		"""
		conn = sqlite3.connect(db_path)
		cursor = conn.cursor()

		cursor.execute('''
			CREATE TABLE IF NOT EXISTS users (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL,
				age INTEGER
			)
		''')

	    # Insert sample data
		sample_users = [
			('John Doe', 'john.doe@example.com', 30),
			('Jane Smith', 'jane.smith@example.com', 25),
			('Bob Johnson', 'bob.johnson@example.com', 35),
			('Alice Williams', 'alice.williams@example.com', 28)
		]

		cursor.executemany('''
			INSERT OR IGNORE INTO users (name, email, age) VALUES (?, ?, ?)
		''', sample_users)

		conn.commit()
		cursor.close()
		conn.close()
		print(f"Sample database setup completed at: {db_path}")

def main():
		"""Demonstrate the DatabaseConnection context manager usage
		"""
		db_path = 'sample_database.db'

		# Setup sample database
		DatabaseConnection.setup_sample_database(db_path)

		print("\n" + "=" * 50)
		print("Demonstrating DatabaseConnection context manager")
		print("=" * 50)

		# Use the context manager to query the DB
		try:
			with DatabaseConnection(db_path) as cursor:
				cursor.execute('SELECT * FROM users')
				users = cursor.fetchall()
				print("Users in the database:")
				for user in users:
					print(user)
		except Exception as e:
			print(f"An error occurred: {e}")

		print("\n" + "=" * 50)
		print("Demonstration completed")
		print("=" * 50)

		# Cleanup - remove sample database
		try:
			os.remove(db_path)
			print(f"Sample database file '{db_path}' removed.")
		except OSError:
			pass

if __name__ == "__main__":
    main()