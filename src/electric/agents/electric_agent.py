import sys
import os
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(project_root)

import asyncio

from typing import Dict, Any, AsyncIterable

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient

from settings.config import Config
from settings.prompts import ELECTRIC_AGENT
from agents.base_agent import BaseAgent


memory = MemorySaver()

async def get_tools():
    try:
        client = MultiServerMCPClient(
            {
                "Electric Utility Server": {
                    "url": Config.MCP.url,
                    "transport": "streamable_http",
                }
            }
        )
            # Load tools from the MCP server
        mcp_tools = await client.get_tools()
        return mcp_tools
    except Exception as e:
        print(f"Error connecting to MCP server: {str(e)}")
        raise



class ElectricAgent(BaseAgent):
    def __init__(self, streamable=True):
        super().__init__(
            agent_name="ElectricAgent",
            description="An agent for managing electric utility tasks.",
            content_types=['text', 'text/plain'],
        )

        asyncio.run(self._setup_graph(streamable))

    
    async def _setup_graph(self, streamable=False):
        """Setup the graph with necessary configurations."""
        self.model = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.0,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            n=1,
            stop=None,
            api_key=Config.OPENAI.api_key
        )

        tools = await get_tools()

        self.graph = create_react_agent(
            self.model,
            checkpointer=memory,
            prompt=ELECTRIC_AGENT,
            tools=tools
        )

    async def invoke(self, query, sessionId) -> str:
        config = {'configurable': {'thread_id': sessionId}}
        response = await self.graph.ainvoke({'messages': [('user', query)]}, config)
        return response

    async def stream(
        self, query, sessionId, stream_mode=['updates', 'messages']
    ) -> AsyncIterable[Dict[str, Any]]:
        inputs = {'messages': [('user', query)]}
        config = {'configurable': {'thread_id': sessionId}}

        async for stream_mode, chunk in self.graph.astream(inputs, config, stream_mode=stream_mode):
            yield stream_mode, chunk

if __name__ == "__main__":
    agent = ElectricAgent()
    # Example usage
    session_id = "example_session"
    query = "Assign an electrician to fix a broken light switch at 123 Main St."
    response = asyncio.run(agent.invoke(query, session_id))
    print("response:", response)
    
