import httpx
import asyncio

from typing import Dict, Any, AsyncIterable

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI

from agents.base_agent import BaseAgent
from settings.config import Config
from settings.prompts import HOME_ASSISTANT_AGENT
from tools.energy_tools import EnergyTools
from tools.agent_tools import AgentTools
from a2a_client.agent_dictionary import AgentDictionary

memory = MemorySaver()

class HomeAssistantAgent(BaseAgent):
    """A class representing a Home Assistant agent."""
    
    def __init__(self, httpx_client: httpx.AsyncClient = None):
        super().__init__(
            agent_name="HomeAssistantAgent",
            description="An agent for managing smart home tasks",
            content_types=['text', 'text/plain'],
        )
        self.httpx_client = httpx_client
    
    @classmethod
    async def create(cls, httpx_client):
        """Create an instance of HomeAssistantAgent."""
        self = cls(httpx_client=httpx_client)
        await self._setup_graph()
        return self
    
    async def _setup_graph(self):
        """Setup the graph with necessary configurations."""
        # This method would typically set up the agent's graph and tools.
        # For now, we can leave it empty or implement specific logic as needed.
        
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

        agent_dictionary = await AgentDictionary.create(
            agents_urls=["http://localhost:9000"],
            httpx_client=self.httpx_client
        )
        a2a_agent_instruction = agent_dictionary.agents_context
        print(a2a_agent_instruction)

        tools = [
            EnergyTools.change_light_status,
            EnergyTools.change_air_conditioner_status,
            AgentTools.analyze_energy_usage,
            agent_dictionary.list_remote_agents,
            agent_dictionary.send_message,
            ]
        
        self.graph = create_react_agent(
            self.model,
            checkpointer=memory,
            prompt=HOME_ASSISTANT_AGENT.format(a2a_agent_instruction=a2a_agent_instruction),
            tools=tools
        )


    
    async def invoke(self, query, sessionId) -> str:
        config = {'configurable': {'thread_id': sessionId}}
        response = await self.graph.ainvoke({'messages': [('user', query)]}, config)
        return response

    async def stream(
        self, query, sessionId
    ) -> AsyncIterable[Dict[str, Any]]:
        inputs = {'messages': [('user', query)]}
        config = {'configurable': {'thread_id': sessionId}}

        async for stream_mode, chunk in self.graph.astream(inputs, config, stream_mode=['updates', 'messages']):
            yield stream_mode, chunk