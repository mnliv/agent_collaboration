from typing import TypedDict, Annotated

class CustomState(TypedDict):
    context: str
    historical_messages: list
    last_messages: list
    messages_count: int
