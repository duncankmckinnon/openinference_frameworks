from pydantic import BaseModel, Field
from typing import Optional, Union, Dict
from datetime import datetime


class RequestFormat(BaseModel):
    conversation_hash: str = Field(
        description="The conversation hash associated with the request"
    )
    request_timestamp: Optional[str] = Field(
        default=datetime.now().isoformat(), description="The timestamp of the request"
    )
    customer_message: str = Field(description="The message of the request")


class ResponseFormat(BaseModel):
    response: str = Field(description="The response to the request")


class State(BaseModel):
    request: str = Field(description="The request to the agent")
    context: Optional[Union[str, Dict]] = Field(
        description="The context of the request"
    )
    response: Optional[str] = Field(description="The response to the request")
