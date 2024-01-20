"""
A module to categorize commands for the LLM application.
"""

from typing import List, Optional, Union

from pydantic import BaseModel, Field


class SQLQuery(BaseModel):
    """
    A viable SQL query from the user.
    """

    keywords: List[str] = Field(
        description="""The important keywords from the
        prompt relevant to generating the desired query"""
    )
    sub_queries: List[str] = Field(
        description="""A list of sub questions that need to
        be answered before answering the main query"""
    )


class Error(BaseModel):
    """
    An unviable query from the user.
    """

    error_reason: str = Field("The reason why the query is invalid.")


class MaybeResponse(BaseModel):
    """
    A response from the LLM application.
    """

    response: Union[SQLQuery, Error] = Field(
        description="""The response from the LLM application.
        If the query is invalid, the response will be an error."""
    )


class UserResponse(BaseModel):
    """
    The response from the LLM application to the user.
    """

    result: Optional[MaybeResponse] = Field(default=None)
    is_error: bool = Field(default=False)
    message: Optional[str] = Field(default=None)
