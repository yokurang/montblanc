"""
A file to test the GPTHandler class
"""

import os
import sys

from dotenv import load_dotenv

from commands import Error, SQLQuery, UserResponse
from gpt_handler import GPTHandler

load_dotenv()

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    sys.exit(1)

gpt_handler = GPTHandler()


def test_sql_query():
    """
    The test function for viable SQL queries
    """
    sample_query1 = """Please give me all of the batch
    ids that have a status of FAILURE"""

    queries = [sample_query1]
    for query in queries:
        result: UserResponse = gpt_handler.parse_user_command(query)
        assert result.result is not None, result.message
        assert isinstance(
            result.result.response, SQLQuery
        ), f"Expected SQLQuery, got {type(result)}"
        print("\nTest passed!\n")


def test_error():
    """
    The test function for unviable SQL queries
    """
    sample_query1 = "Am I a good intern?"
    queries = [sample_query1]
    for query in queries:
        result: UserResponse = gpt_handler.parse_user_command(query)
        print("result: ", result)
        assert result.response is str, result.message
        print("\nTest passed!\n")


if __name__ == "__main__":
    test_sql_query()
    test_error()
