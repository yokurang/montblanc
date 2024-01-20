"""
A class that handles the connection to the MariaDB database
"""
import json
import re
import sys
from typing import List

import mariadb


class DBHandler:
    """
    The class that handles the connection to the MariaDB database
    """

    def __init__(
        self, user: str, password: str, hostname: str, port: str, database_name: str
    ):
        self.user = user
        self.password = password
        self.hostname = hostname
        self.port = port
        self.database_name = database_name
        self.connection = None
        self.cursor = None
        self.start_mariadb_connection()

    def start_mariadb_connection(self):
        """
        This function starts the connection with the MariaDB database
        """
        try:
            self.connection = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.hostname,
                port=int(self.port),
                database=self.database_name,
            )
            self.cursor = self.connection.cursor()
        except mariadb.Error as error:
            print(f"Error connecting to MariaDB Platform: {error}")
            sys.exit(1)

    def get_table_columns_and_info(self) -> dict:
        """
        This function gets the columns and
        specifications of all tables in the database
        """
        tables_columns_info = {}

        column_query = f"""
        SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{self.database_name}'
        ORDER BY TABLE_NAME, ORDINAL_POSITION;
        """

        try:
            self.cursor.execute(column_query)
        except mariadb.Error as error:
            print(f"Error: {error}")
            sys.exit(1)

        for table_name, column_name, data_type in self.cursor:
            if table_name not in tables_columns_info:
                tables_columns_info[table_name] = []
            tables_columns_info[table_name].append((column_name, data_type))

        return tables_columns_info

    @staticmethod
    def print_table_columns_and_info(tables_columns_info: dict) -> None:
        """
        This function prints the columns and specifications
        of all tables in the database
        """
        for table_name, columns in tables_columns_info.items():
            print(f"Table: {table_name}")
            for column_name, data_type in columns:
                print(f"Column: {column_name}, Data Type: {data_type}")
                print()

    @staticmethod
    def format_schema_for_gpt(columns_info: dict) -> str:
        """
        This function formats the columns and specifications
        of all tables in the database
        """
        schema_description = "The following is the schema of the database:\n"
        for table, columns in columns_info.items():
            schema_description += f"Table {table} has columns: "
            schema_description += ", ".join(
                [
                    f"{column_name} (type: {data_type})"
                    for column_name, data_type in columns
                ]
            )
            schema_description += ".\n"
        return schema_description

    @staticmethod
    def parse_sql_response(response):
        """Parses a multi-statement SQL
        response into a list of individual SELECT SQL commands.
        Args:
            response (str): The response string containing
            multiple SQL statements.

        Returns:
            List[str]: A list of individual SELECT SQL statements.
        """
        # Regex pattern to match SQL
        # statements that start with SELECT and end with ;
        pattern = r"SELECT.*?;"

        # Find all occurrences of the pattern
        sql_commands = re.findall(pattern, response, re.IGNORECASE | re.DOTALL)

        # Strip whitespace from each command
        sql_commands = [cmd.strip() for cmd in sql_commands]

        return sql_commands

    def execute_sql_commands(self, sql_commands: List[str]) -> str:
        """
        Executes a list of SQL commands and stores their
        results in JSON format.

        Args:
            sql_commands (List[str]): A list of SQL commands to execute.

        Returns:
            None
        """
        results_json = {}
        for command in sql_commands:
            try:
                self.cursor.execute(command)
                # Check if the command is a 'SELECT' query
                if command.strip().lower().startswith("select"):
                    rows = self.cursor.fetchall()
                    columns = [col[0] for col in self.cursor.description]
                    results = [dict(zip(columns, row)) for row in rows]

                    # Store results in a dict with the command as the key
                    results_json[command] = results
                else:
                    print(f"Executed successfully (no output): {command}")
            except mariadb.Error as e:
                print(f"Error executing command: {command}")
                print(f"MariaDB Error: {e}")

        json_output = json.dumps(results_json, indent=4)
        print("Execution Results in JSON format:")
        print(json_output)
        return json_output
