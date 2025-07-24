from a2a.types import AgentCard, AgentCapabilities
from a2a_server.agent_skills import  check_electric_bill, support_customer_issue

agent_card = AgentCard(
    name="Electric Utility Agent",
    description="An agent for managing electric utility tasks,\ " \
    "including checking bills and supporting customer issues.",
    url="http://localhost:9000/",
    version="1.0.0",
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    skills=[check_electric_bill, support_customer_issue],   
)