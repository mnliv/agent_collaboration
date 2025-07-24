import json
import asyncio
import time
import httpx

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from agents.home_assistant import HomeAssistantAgent

async def main():
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
            # print("response", response)
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
    async def chat_loop(agent: HomeAssistantAgent, streamable=False):
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
    async with httpx.AsyncClient() as httpx_client:
        agent = await HomeAssistantAgent.create(httpx_client=httpx_client)
        session_id = "example_session"
        await chat_loop(agent, streamable=True)


if __name__ == "__main__":
    asyncio.run(main())