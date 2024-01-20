"""
This is the main file of the application.
"""

import logging
import os
import sys

from dotenv import load_dotenv

from db_handler import DBHandler
from gpt_handler import GPTHandler

# Load environment variables
load_dotenv()

# Database credentials
MARIADB_USER = os.getenv("MARIADB_USER", "root")
MARIADB_PASSWORD = os.getenv("MARIADB_PASSWORD", "Alan4ang")
MARIADB_HOST = os.getenv("MARIADB_HOST", "127.0.0.1")
MARIADB_PORT = os.getenv("MARIADB_PORT", "3306")
MARIADB_DATABASE_NAME = os.getenv("MARIADB_DATABASE_NAME", "evooq_test")

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logging.error("OpenAI API key not found in environment variables.")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)


def main():
    """
    The entry point of the application
    """
    logging.info("Starting LLM...")

    # Initialize DBHandler
    db_handler = DBHandler(
        MARIADB_USER,
        MARIADB_PASSWORD,
        MARIADB_HOST,
        MARIADB_PORT,
        MARIADB_DATABASE_NAME,
    )

    # Connect to MariaDB server and collect tables and column information
    tables_columns_info = db_handler.get_table_columns_and_info()

    # Format the information for ChatGPT
    schema_info = db_handler.format_schema_for_gpt(tables_columns_info)

    logging.debug(f"Schema information: {schema_info}")

    # Initialize GPTHandler
    gpt_handler = GPTHandler()

    # Wait for a question from the user
    user_question = input("Enter your question or 'exit' to quit: ")
    if user_question.lower() == "exit":
        return

    user_query = gpt_handler.parse_user_command(user_question)
    logging.debug(f"User query: {user_query}")
    if not user_query.result:
        logging.info("We could not understand your command. Please try again.")
        return

    # Ask the question to OpenAI API
    response = gpt_handler.ask_gpt_4_vanilla(user_question, schema_info)
    logging.debug(f"Response: {response}")
    print(f"Response: {response}")

    # Parse the response
    parsed_sql_response = db_handler.parse_sql_response(response)
    logging.debug(f"Parsed response: {parsed_sql_response}")
    print(f"Parsed response: {parsed_sql_response}")

    # Execute the SQL queries
    db_handler.execute_sql_commands(parsed_sql_response)

    logging.info("LLM finished successfully.")
    print("LLM finished successfully.")


if __name__ == "__main__":
    main()
