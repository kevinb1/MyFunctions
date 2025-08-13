import sqlite3
import pandas as pd


class SQLiteDatabase:
    """
    SQLite Database handler
    """

    def __init__(self, db_name):
        """
        Initializes the SQLite database connection.

        Args:
            db_name (str): Name of the SQLite database file.
        """
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        """
        Executes a SQL query on the database.

        Args:
            query (str): SQLite query to execute. Use ? for parameterized queries.
            params (tuple or list of tuple, optional): Parameters for the query.
        """
        if params is None:
            self.cursor.execute(query)
        elif isinstance(params, list) and all(isinstance(p, tuple) for p in params):
            # Multiple rows, so use executemany
            self.cursor.executemany(query, params)
        else:
            # Single row, so use execute
            self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_all(self):
        """
        Retrieves all results from the last executed query.

        Returns:
            list: list of tuples containing the results of the query.
        """
        return self.cursor.fetchall()

    def to_pandas(self):
        """
        Retrieves all results from the last executed query and returns them as a pandas DataFrame.

        Returns:
            pandas.DataFrame: DataFrame containing the query results.
        """
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        return pd.DataFrame(rows, columns=columns)

    def close(self):
        """
        Closes the database connection.
        """
        self.connection.close()

    def create_table(self, table_name, columns):
        """
        Method for easier table cration in the SQlite database, using the exceute_query method.

        Args:
            table_name (str): name of the table to create
            columns (dict): Dictionary with column names as keys and their types as values.
        """
        columns_with_types = ', '.join(
            f"{col} {typ}" for col, typ in columns.items())
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})"
        self.execute_query(create_table_query)
        self.connection.commit()

    def insert_data(self, table_name, data):
        """
        Inserts one or multiple rows into a specified table.

        Args:
            table_name (str): Table name.
            data (dict or list of dict): Row(s) to insert.
        """
        if isinstance(data, dict):
            data = [data]
        if not data:
            raise ValueError("No data provided for insertion.")

        columns = list(data[0].keys())
        placeholders = ', '.join('?' * len(columns))
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

        values = [tuple(row[col] for col in columns) for row in data]
        self.execute_query(insert_query, values)

    def update_record(self, table_name, data, condition):
        """
        Updates records in a specified table based on one or multiple conditions.

        Args:
            table_name (str): Table name.
            data (dict): Column-value pairs to update.
            condition (str or dict): 
                - str: Raw SQL condition with placeholders (e.g., "id = ? AND name = ?").
                - dict: Column-value pairs for conditions (joined with AND).
        """
        if not data:
            raise ValueError("No data provided for update.")

        set_clause = ', '.join(f"{col} = ?" for col in data.keys())

        # Handle conditions
        if isinstance(condition, dict):
            condition_clause = ' AND '.join(
                f"{col} = ?" for col in condition.keys())
            params = tuple(data.values()) + tuple(condition.values())
        elif isinstance(condition, str):
            condition_clause = condition
            params = tuple(data.values())
        else:
            raise ValueError("Condition must be a string or dictionary.")

        update_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition_clause}"
        self.execute_query(update_query, params)

    def delete_record(self, table_name, condition):
        """
        Deletes records from a specified table based on one or multiple conditions.

        Args:
            table_name (str): Table name.
            condition (str or dict): 
                - str: Raw SQL condition with placeholders (e.g., "id = ? AND name = ?").
                - dict: Column-value pairs for conditions (joined with AND).
        """
        if isinstance(condition, dict):
            condition_clause = ' AND '.join(
                f"{col} = ?" for col in condition.keys())
            params = tuple(condition.values())
        elif isinstance(condition, str):
            condition_clause = condition
            params = None  # assumes placeholders are handled externally
        else:
            raise ValueError("Condition must be a string or dictionary.")

        delete_query = f"DELETE FROM {table_name} WHERE {condition_clause}"
        self.execute_query(delete_query, params)
