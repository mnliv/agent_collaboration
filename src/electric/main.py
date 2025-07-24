import json
import asyncio
import time

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from agents.electric_agent import ElectricAgent


streamable = True  # Set to True for streaming responses, False for batch processing
agent = ElectricAgent(streamable=streamable)
session_id = "example_session"

# 🖨️ Helper to print messages
def print_console(msg):
    if isinstance(msg, HumanMessage):
        print(f"\n\033[94m👤 User:\033[0m {msg.content}")
    elif isinstance(msg, AIMessage):
        print(f"\n\033[92m🤖 Agent:\033[0m {msg.content}")
    elif isinstance(msg, ToolMessage):
        print(f"\n\033[95m📦 Tool Response [{msg.name}]:\033[0m")
        print(msg.content)

class StreamAgentResult:
    def __init__(self):
        self.msg_id = None

    def log(self, streammod, response):
        if streammod == 'updates':
            if 'agent' in response:
                pass
            elif 'tools' in response:
                print_console(response["tools"]["messages"][-1])
        elif streammod == 'messages':            
            if response[0].content:
                if not isinstance(response[0], ToolMessage):
                    id = response[0].id
                    if self.msg_id != id:
                        self.msg_id = id
                        print(f"\n\033[92m🤖 Agent:\033[0m", end='', flush=True)
                    print(response[0].content, end='', flush=True)

# 🔁 Main loop (new session every time)
async def chat_loop(agent: ElectricAgent, streamable=False):
    print("\n\033[1m--- New Agent Chat Session Started (type 'exit' to quit) ---\033[0m\n")

    while True:
        user_input = input("\n\033[94m👤 User:\033[0m: ")
        if user_input.lower() in ("exit", "quit"):
            print("\n👋 Bye!")
            break
        if not streamable:
            responses = await agent.invoke(user_input, session_id)
            print_console(responses["messages"][-1])
        else:
            stream_agent_result = StreamAgentResult()
            async for streammod, res in agent.stream(user_input, session_id):
                # print(res)
                stream_agent_result.log(streammod, res)


if __name__ == "__main__":
    agent = ElectricAgent(streamable)
    asyncio.run(chat_loop(agent, streamable))