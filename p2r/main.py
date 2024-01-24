'''
Expanding Search Queries (RAG)

    In summary, this code is about using LLM to take a piece of text,
    generate search queries from it, then execute those queries. It's
    a combination of AI-powered analysis and automated search execution.
    I think we can use this code in some way to get the LLM to analyse
    our data and provide an appropriate proposal/rationale.

Code derived from: https://jxnl.github.io/instructor/examples/search/
'''

import enum
from pydantic import Field, BaseModel
from typing import List
from instructor.dsl import MultiTask
import instructor
from openai import OpenAI
import asyncio
import os
import logging
import sys
# from dotenv import load_dotenv
from db_handler import DBHandler

# load_dotenv()

client = instructor.patch(OpenAI())

# I think we might need to use dbhandler or maybe even everything else but not sure
# Database credentials and initialise DBHandler
# MARIADB_USER = os.getenv("MARIADB_USER", "root")
# MARIADB_PASSWORD = os.getenv("MARIADB_PASSWORD", "Alan4ang")
# MARIADB_HOST = os.getenv("MARIADB_HOST", "127.0.0.1")
# MARIADB_PORT = os.getenv("MARIADB_PORT", "3306")
# MARIADB_DATABASE_NAME = os.getenv("MARIADB_DATABASE_NAME", "evooq_test")

# db_handler = DBHandler(
#     MARIADB_USER,
#     MARIADB_PASSWORD,
#     MARIADB_HOST,
#     MARIADB_PORT,
#     MARIADB_DATABASE_NAME,
# )

class SearchType(str, enum.Enum):
    """
    Enumeration representing the types of searches that can be performed.
    """
    SEARCH_TYPE = "idk what to put here. enriched_proposals maybe?"
    MERGE_MULTIPLE_RESPONSES = "MERGE_MULTIPLE_RESPONSES"

class Search(BaseModel):
    """
    Class representing a single search query.
    """
    title: str = Field(..., description="Title of the request")
    query: str = Field(..., description="Query to search for relevant content")
    type: SearchType = Field(..., description="Type of search")

    async def execute(self):
        print(f"Searching for `{self.title}` with query `{self.query}` using `{self.type}`")



class MultiSearch(BaseModel):
    "Correctly segmented set of search results"
    tasks: List[Search]


MultiSearch = MultiTask(Search)


def segment(data: str) -> MultiSearch:
    return client.chat.completions.create(
        model="gpt-4-0613",
        temperature=0.1,
        functions=[MultiSearch.openai_schema],
        function_call={"name": MultiSearch.openai_schema["name"]},
        messages=[
            {
                "role": "user",
                "content": f"Consider the data below: '\n{data}' and segment it into multiple search queries",
            },
        ],
        max_tokens=1000,
    )


queries = segment("Please send me the ______.")

async def execute_queries(queries: MultiSearch):
    await asyncio.gather(*[q.execute() for q in queries.tasks])

loop = asyncio.get_event_loop()
loop.run_until_complete(execute_queries())
loop.close()

