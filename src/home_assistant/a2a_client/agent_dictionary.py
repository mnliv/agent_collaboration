import json
import httpx
import base64
import uuid
import asyncio

from typing import Dict
from typing import List
from collections import defaultdict

from a2a.client import A2ACardResolver
from a2a.types import AgentCard
from a2a.client import A2AClient
from a2a.types import (
    AgentCard,
    DataPart,
    Message,
    MessageSendConfiguration,
    MessageSendParams,
    SendStreamingMessageRequest,
    SendMessageRequest,
    SendMessageResponse,
    Part,
    Task,
    TaskState,
    TextPart,
)


class AgentDictionary:

    def __init__(self, agents_urls: List[str], httpx_client: httpx.AsyncClient):
        self.agents_urls = agents_urls
        self.agents_context: str = "There's no remote agent available."
        self.cards: dict[str, AgentCard] = {}
        self.a2a_clients: dict[str, Dict] = {}
        self.httpx_client = httpx_client
    
    @classmethod
    async def create(cls, agents_urls: List[str], httpx_client: httpx.AsyncClient):
        self = cls(agents_urls, httpx_client)
        await self.init_remote_agents()
        return self

    async def init_remote_agents(self):
        async with asyncio.TaskGroup() as task_group:
            for address in self.agents_urls:
                task_group.create_task(self.retrieve_card(address))

    async def retrieve_card(self, address: str):
        card_resolver = A2ACardResolver(self.httpx_client, address)
        card = await card_resolver.get_agent_card()
        await self.register_agent_card(card)
    
    async def register_agent_card(self, card: AgentCard):
        self.cards[card.name] = card
        timeout = httpx.Timeout(30)
        self.a2a_clients[card.name] = {
            "client": await A2AClient.get_client_from_agent_card_url(
                base_url=card.url,
                httpx_client=self.httpx_client,
                http_kwargs={"timeout": timeout}
            ),
            "context_id": None,
        }
        agent_info = []
        for ra in self.list_remote_agents():
            agent_info.append(json.dumps(ra))
        self.agents_context = '\n'.join(agent_info)

    def list_remote_agents(self):
        """List the available remote agents you can use to delegate the task."""
        if not self.a2a_clients:
            return []

        remote_agent_info = []
        for card in self.cards.values():
            remote_agent_info.append(
                {'name': card.name, 'description': card.description}
            )
        return remote_agent_info
    
    async def send_message(
        self, agent_name: str, message: str,
    ):
        """Sends a task either streaming (if supported) or non-streaming.

        This will send a message to the remote agent named agent_name.

        Args:
          agent_name: The name of the agent to send the task to.
          message: The message to send to the agent for the task.
          tool_context: The tool context this method runs in.

        Yields:
          A dictionary of JSON data.
        """
        try:
            print(f"Sending message to {agent_name}: {message} ...")
            if agent_name not in self.a2a_clients:
                raise ValueError(f'Agent {agent_name} not found')
            client: A2AClient = self.a2a_clients[agent_name]["client"]
            if not client:
                raise ValueError(f'Client not available for {agent_name}')
            
            messageId = str(uuid.uuid4())
            contextId = self.a2a_clients[agent_name]["context_id"]

            messsage_params: MessageSendParams = MessageSendParams(
                **{
                    'message': {
                        'role': 'user',
                        'parts': [
                            {'kind': 'text', 'text': message}
                        ],
                        'messageId': messageId,
                        'contextId': contextId,
                    },
                }
            )

            streaming_request = SendStreamingMessageRequest(
                id=str(uuid.uuid4()), params=messsage_params
            )
            response: SendMessageResponse = client.send_message_streaming(streaming_request)
            messages = []
            async for chunk in response:
                chunk = chunk.model_dump(mode='json', exclude_none=True)
                if "message" in chunk["result"]['status']:
                    word = chunk["result"]["status"]["message"]["parts"][0]["text"]
                    print(word, end='', flush=True)
                    messages.append(word)
                    
            self.a2a_clients[agent_name]["context_id"] = chunk["result"]["contextId"]
            output = ''.join(messages)
            print(f"Response from {agent_name}: {output}")
            return output
        except Exception as e:
            print(f"Error sending message to {agent_name}: {e}")
            breakpoint()
            return {"error": str(e)}


def group_messages_by_task(messages):
    grouped = defaultdict(lambda: {'user': '', 'agent': ''})

    for msg in messages:
        task_id = getattr(msg, 'taskId', None)
        role = getattr(msg, 'role', None)
        parts = getattr(msg, 'parts', [])

        if not task_id or not role:
            continue  # Skip if missing taskId or role

        role_str = role.value if hasattr(role, 'value') else str(role)

        text_content = ''
        for part in parts:
            root = getattr(part, 'root', None)
            if root and getattr(root, 'kind', '') == 'text':
                text_content += getattr(root, 'text', '')

        grouped[task_id][role_str] += text_content + ' '

    # Strip trailing spaces
    for task in grouped.values():
        task['user'] = task['user'].strip()
        task['agent'] = task['agent'].strip()

    return dict(grouped)