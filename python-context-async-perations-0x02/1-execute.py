"""Implement a class based custom context manager ExecuteQuery
Args:
    Query: SELECT * FROM users WHERE age > ?
	Parameters: 25
Returns the result of the query
IMPORTANT: Use the __enter__() and __exit__() methods."""
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
                import sqlite3
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
            exc_type: Execption type(if any)
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
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 25))
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 30))
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Charlie", 35))
        conn.commit()
        conn.close()


