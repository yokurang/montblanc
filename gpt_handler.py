"""
This file contains the GPTHandler class, which is responsible for
"""
from instructor import patch
from openai import OpenAI

from commands import UserResponse


class GPTHandler:
    """
    This class is responsible for handling the GPT-4 API
    """

    def __init__(self):
        self.client = patch(OpenAI())
        self.COMMAND_PROMPT = """
        You are categorizing the Question in the context into one of the following commands.
        1. SQLQuery: A question that can be answered with a SQL query from the provided context
        2. Error: A question that cannot be answered with a SQL query from the provided context
        Make sure to adhere to the requested response format.
        If you are unsure of the exact command to classify the question into,
        do not return a result and instead return an error message explaining
        why you are unable to do so in the requested format.
        """

    def strip_indentation(self, text: str) -> str:
        """
        Strip the indentation from a string.
        """
        return text.strip()

    def parse_user_command(self, text: str) -> UserResponse:
        """
        This function parses the user's command and returns the result
        as a UserResponse object
        """
        completion: UserResponse = self.client.chat.completions.create(
            model="gpt-4-0613",
            response_model=UserResponse,
            messages=[
                {
                    "role": "system",
                    "content": self.strip_indentation(self.COMMAND_PROMPT),
                },
                {"role": "user", "content": text},
            ],
            max_retries=0,
        )
        return completion

    def ask_gpt_4_vanilla(self, question, schema_info):
        """
        This function asks GPT-4 a question
        """
        prompt = f"""Given the following schema information,
        what is the SQL query to answer the question? 
        Just provide the SQL query.
        \n\n{schema_info}
        \n\nQuestion: {question}
        \n\nSQL Query:"""
        response = self.client.chat.completions.create(
            model="gpt-4-0613",
            messages=[
                {
                    "role": "system",
                    "content": "You are a world class helpful assistant. Your",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
        )

        return response.choices[0].message.content
