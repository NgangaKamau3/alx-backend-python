"""Implement a class based custom context manager ExecuteQuery
Args:
    Query: SELECT * FROM users WHERE age > ?
    Parameters: 25
Returns the result of the query
IMPORTANT: Use the __enter__() and __exit__() methods."""

import sqlite3
import os


class ExecuteQuery:
    def __init__(self, query, database_path, parameters=None):
        self.query = query
        self.parameters = parameters or ()
        self.cursor = None
        self.conn = None
        self.results = None
        self.database_path = database_path

    def __enter__(self):
        # This is where we write the logic to be executed in our query
        try:
            print(f"Opening database connection to {self.database_path}")
            self.conn = sqlite3.connect(self.database_path)
            self.cursor = self.conn.cursor()
            print(f"Database connection established successfully")

            # Execute the query with parameters
            print(f"Executing query: {self.query}")
            if self.parameters:
                print(f"Query parameters: {self.parameters}")
                self.cursor.execute(self.query, self.parameters)
            else:
                self.cursor.execute(self.query)

            # Fetch the results for SELECT queries
            if self.query.strip().upper().startswith("SELECT"):
                self.results = self.cursor.fetchall()
                print(f"Query results: {self.results}")
            else:
                self.conn.commit()
                print("Query executed successfully")

            return self.results
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            raise e

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager - clean up the database connection.
        
        Args:
            exc_type: Exception type(if any)
            exc_value: Exception value(if any)
            traceback: Exception traceback(if any)
        """
        if self.cursor:
            self.cursor.close()
            print("Database cursor closed")
            
        if self.conn:
            if exc_type is None:
                self.conn.commit()
                print("Transaction committed successfully")
            else:
                self.conn.rollback()
                print(f"Database transaction rolled back due to exception: {exc_value}")
                
            self.conn.close()
            print("Database connection closed")
            
        return False


def setup_sample_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER)
            ''')
    
    sample_users = [
        ("Alice", "alice@example.com", 30),
        ("Bob", "bob@example.com", 25),
        ("Charlie", "charlie@example.com", 35),
        ("David", "david@example.com", 28),
        ("Eve", "eve@example.com", 22)
    ]

    cursor.executemany("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", sample_users)
    conn.commit()
    conn.close()
    print(f"Sample database created at {db_path}")


def main():
    """
    Demonstrate the ExecuteQuery context manager usage"""
    db_path = "sample_database.db"
    # Setup sample database
    setup_sample_database(db_path)
    
    print("\n" + "="*60)
    print("Using ExecuteQuery Context Manager")
    print("="*60)
    
    # Example 1: Query users with age > 25
    print("\nExample 1: SELECT * FROM users WHERE age > ?")
    print("-" * 50)
    
    try:
        with ExecuteQuery("SELECT * FROM users WHERE age > ?", db_path, (25,)) as results:
            print("\nQuery results:")
            print("-" * 50)
            print(f"{'ID':<5} {'Name':<15} {'Email':<25} {'Age':<5}")
            print("-" * 50)
            
            for row in results:
                print(f"{row[0]:<5} {row[1]:<15} {row[2]:<25} {row[3]:<5}")
            
            print(f"\nUsers with age > 25: {len(results)}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    # Example 2: Different query - users with specific age
    print("\n" + "="*60)
    print("Additional Example: SELECT * FROM users WHERE age = ?")
    print("-" * 50)
    
    try:
        with ExecuteQuery("SELECT * FROM users WHERE age = ?", db_path, (30,)) as results:
            print("\nQuery results:")
            print("-" * 40)
            print(f"{'ID':<5} {'Name':<15} {'Email':<25} {'Age':<5}")
            print("-" * 40)
            
            for row in results:
                print(f"{row[0]:<5} {row[1]:<15} {row[2]:<25} {row[3]:<5}")
            
            print(f"\nUsers with age = 30: {len(results)}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    # Example 3: Query without parameters
    print("\n" + "="*60)
    print("Example with no parameters: SELECT COUNT(*) FROM users")
    print("-" * 50)
    
    try:
        with ExecuteQuery("SELECT COUNT(*) FROM users", db_path) as results:
            print(f"\nTotal number of users: {results[0][0]}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    print("\n" + "="*60)
    print("ExecuteQuery context manager demonstration completed")
    print("="*60)
    
    # Clean up - remove sample database
    try:
        os.remove(db_path)
        print(f"Sample database {db_path} removed")
    except OSError:
        pass


if __name__ == "__main__":
    main()