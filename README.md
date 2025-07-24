# Agent Collaboration Project

A comprehensive demonstration of modern AI agent architectures featuring **Agent-to-Agent (A2A)** communication, **Model Context Protocol (MCP)**, multi-agent systems, and local tool integration.

## 🌟 Project Overview

This project showcases the complete ecosystem of AI agent collaboration, demonstrating how different agents can work together to solve complex real-world problems. It serves as a practical example of why A2A communication is essential and how it enables seamless agent interactions.

### Why A2A (Agent-to-Agent) Communication?

Modern AI applications require multiple specialized agents working together. A2A communication enables:

- **Distributed Intelligence**: Different agents handle their areas of expertise
- **Scalability**: Add new agents without modifying existing ones
- **Resilience**: System continues working even if individual agents fail
- **Specialization**: Each agent focuses on specific domains and tools
- **Dynamic Collaboration**: Agents discover and communicate with each other at runtime

### How A2A Works in This Project

1. **Agent Discovery**: Agents register their capabilities in a shared directory
2. **Dynamic Communication**: Agents can find and communicate with other agents based on needs
3. **Protocol Standardization**: A2A provides a consistent communication protocol
4. **Task Delegation**: Complex tasks are broken down and distributed among specialized agents

## 🏗️ Architecture Components

### 1. A2A Communication Layer
- **A2A Server**: Enables agent-to-agent communication and discovery
- **Agent Cards**: Define agent capabilities and communication interfaces
- **Request Handlers**: Process inter-agent communication requests
- **Task Management**: Coordinate complex multi-agent workflows

### 2. MCP (Model Context Protocol) Integration
- **Electric Utility MCP Server**: Provides standardized tools for electrical services
- **Tool Discovery**: Agents can dynamically discover and use MCP tools
- **Resource Management**: Access to shared resources across agents
- **Prompt Templates**: Standardized interaction patterns

### 3. Multi-Agent System
- **Electric Agent**: Specialized in electricity billing and technician assignment
- **Home Assistant Agent**: Manages smart home devices and energy optimization
- **Base Agent Framework**: Common foundation for all agents
- **State Management**: Persistent conversation and task state

### 4. Local Tools & Integration
- **Energy Tools**: Smart home device control and energy monitoring
- **Agent Tools**: Cross-agent communication and coordination
- **Local Data Sources**: Electrician databases, work orders, billing systems

## 🤖 Agents in the System

### Electric Agent (`src/electric/`)
**Purpose**: Manages electric utility operations and services

**Capabilities**:
- Check electricity bills for customers
- Assign electricians to service requests
- Access work order history
- Manage available electrician resources

**Tools**:
- `check_bill(electric_code, month, year)`
- `assign_electrician(address, issue_description)`

### Home Assistant Agent (`src/home_assistant/`)
**Purpose**: Manages smart home automation and energy optimization

**Capabilities**:
- Control smart home devices
- Monitor energy consumption
- Coordinate with Electric Agent for billing inquiries
- Optimize energy usage patterns

**Tools**:
- Energy monitoring and control tools
- Device management functions
- Agent communication tools

## 🔄 Agent Collaboration Scenarios

### Scenario 1: Smart Energy Management
1. **Home Assistant** detects high energy usage
2. **Home Assistant** communicates with **Electric Agent** via A2A
3. **Electric Agent** checks current billing rates and usage patterns
4. **Home Assistant** adjusts device schedules based on rate information

### Scenario 2: Service Request Coordination
1. **Home Assistant** detects electrical issue (e.g., power outage)
2. **Home Assistant** sends service request to **Electric Agent** via A2A
3. **Electric Agent** assigns appropriate electrician
4. **Electric Agent** sends status updates back to **Home Assistant**
5. **Home Assistant** notifies homeowner of service progress

## 📁 Project Structure

```
agent_collaboration/
├── README.md                          # This file
├── requirements_electric.txt          # Main dependencies
│
├── src/
│   ├── electric/                      # Electric Utility Agent
│   │   ├── agents/                    # Agent implementations
│   │   │   ├── base_agent.py         # Base agent framework
│   │   │   ├── electric_agent.py     # Electric utility agent
│   │   │   └── state.py              # Agent state management
│   │   ├── a2a_server/               # Agent-to-Agent server
│   │   │   ├── server.py             # A2A server implementation
│   │   │   ├── agent_card.py         # Agent capability definition
│   │   │   ├── agent_skills.py       # Agent skill definitions
│   │   │   └── electric_agent_executor.py # Agent execution logic
│   │   ├── mcp/                      # Model Context Protocol
│   │   │   ├── electric_tools.py     # MCP tools implementation
│   │   │   └── mcp_server.py         # MCP server
│   │   ├── mcps/                     # MCP server instances
│   │   ├── settings/                 # Configuration and prompts
│   │   ├── tests/                    # Test suite
│   │   └── demo.py                   # Demo script
│   │
│   ├── home_assistant/               # Home Assistant Agent
│   │   ├── agents/                   # Agent implementations
│   │   │   ├── base_agent.py         # Base agent framework
│   │   │   ├── home_assistant.py     # Home assistant agent
│   │   │   └── energy_agent.py       # Energy management agent
│   │   ├── a2a_client/              # A2A client for communication
│   │   │   ├── agent_dictionary.py   # Agent discovery system
│   │   │   └── agent_dictionary.jsonl # Agent registry
│   │   ├── tools/                    # Local tools
│   │   │   ├── energy_tools.py       # Energy monitoring tools
│   │   │   └── agent_tools.py        # Inter-agent communication
│   │   ├── settings/                 # Configuration
│   │   └── main.py                   # Entry point
│   │
│   ├── food_provider/                # Future: Food delivery agent
│   └── minimart/                     # Future: Retail agent
```

## 🔧 Key Technologies

- **A2A (Agent-to-Agent)**: Inter-agent communication protocol
- **MCP (Model Context Protocol)**: Standardized tool and resource access
- **LangGraph**: Agent workflow orchestration
- **LangChain**: LLM integration and tool management
- **OpenAI GPT-4**: Language model for agent reasoning
- **FastAPI/Uvicorn**: Web server for A2A communication
- **AsyncIO**: Asynchronous agent operations
- **Pytest**: Comprehensive testing framework

## 🎯 Use Cases Demonstrated

1. **Smart Home Energy Management**: Coordinated energy optimization across multiple systems
2. **Service Request Automation**: Automated electrician dispatch and scheduling
3. **Cross-Domain Problem Solving**: Agents with different specializations working together
4. **Real-time Communication**: Dynamic agent discovery and task delegation
5. **Scalable Architecture**: Easy addition of new agents and capabilities

## 🔮 Future Enhancements

- **Food Provider Agent**: Restaurant and delivery coordination
- **Minimart Agent**: Retail inventory and ordering
- **Weather Agent**: Weather-based energy optimization
- **Security Agent**: Home security integration
- **Voice Interface**: Natural language interaction with the multi-agent system

## 📖 Learning Outcomes

This project demonstrates:

- **Why A2A is essential** for modern AI applications
- **How to implement** multi-agent communication patterns
- **MCP integration** for standardized tool access
- **Real-world agent collaboration** scenarios
- **Scalable agent architecture** design
- **Testing strategies** for multi-agent systems

---

**This project serves as a complete reference for building production-ready multi-agent systems with A2A communication, showcasing the future of distributed AI applications.**