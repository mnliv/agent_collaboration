import os

from dataclasses import dataclass


@dataclass
class Config:
    @dataclass
    class MCP:
        host: str = "localhost"
        port: int = 3000
        transport: str = "streamable-http"
        url: str = "http://localhost:3000/mcp/"
    
    @dataclass
    class OPENAI:
        api_key = os.getenv("OPENAI_API_KEY", "OPENAI_API_KEY")
