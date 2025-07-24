import uvicorn

from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.apps import A2AStarletteApplication

from a2a_server.electric_agent_executor import ElectricAgentExecutor
from a2a_server.agent_card import agent_card

def main():
    request_handler = DefaultRequestHandler(
        agent_executor=ElectricAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    uvicorn.run(server.build(), host='0.0.0.0', port=9000)

if __name__ == "__main__":
    main()