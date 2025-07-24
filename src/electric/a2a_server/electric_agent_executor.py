import logging
import json

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils.errors import ServerError
from a2a.types import (
    FilePart,
    FileWithBytes,
    InvalidParamsError,
    Part,
    Task,
    TextPart,
    TaskState,
    UnsupportedOperationError,
)
from a2a.utils import (
    new_agent_text_message,
    new_task,
)
from a2a.server.tasks import TaskUpdater
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from agents.electric_agent import ElectricAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ElectricAgentExecutor(AgentExecutor):
    """Executor for the Electric Agent to handle requests and responses."""

    def __init__(self):
        super().__init__()
        self.agent = ElectricAgent()

    async def execute(
        self, 
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None :
        """Execute the Electric Agent with the provided context and event queue."""
        if not self._validate_request(context):
            raise ServerError(error=InvalidParamsError())
        
        query = context.get_user_input()
        task = context.current_task
        if not task:
            task = new_task(context.message) # type: ignore
            await event_queue.enqueue_event(task)
        updater = TaskUpdater(event_queue, task.id, task.contextId)

        async for streammode, res in self.agent.stream(query, context.task_id, stream_mode=['messages']):
            print(res[0].text(), end='', flush=True)
            if (isinstance(res[0], AIMessage)):
                if(res[0].text()):
                    await updater.update_status(
                        TaskState.working,
                        new_agent_text_message(
                            res[0].text(),
                            task.contextId,
                            task.id,
                        ),
                    )
        await updater.complete()


    
    async def cancel(
        self, request: RequestContext, event_queue: EventQueue
    ) -> Task | None:
        raise ServerError(error=UnsupportedOperationError())
        
    
    def _validate_request(self, context: RequestContext) -> bool:
        """Validate the request context before processing."""
        return True
