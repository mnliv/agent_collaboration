import os

from dataclasses import dataclass


@dataclass
class Config:
    @dataclass
    class OPENAI:
        api_key = os.getenv("OPENAI_API_KEY", "OPENAI_API_KEY")
