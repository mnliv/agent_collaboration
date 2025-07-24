from crewai import Agent, Task, Crew
from crewai.tools import BaseTool


from agents.base_agent import BaseAgent
from tools.energy_tools import EnergyTools


class GetHistoricalData(BaseTool):
    name: str = "get_historical_data"
    description: str = "Retrieve historical data of device usage."

    def _run(self) -> str:
        return EnergyTools.get_historical_data()
    
class EnergyAgent(BaseAgent):
    def __init__(self, streamable=False):
        super().__init__(
            agent_name="EnergyAgent",
            description="An agent for analyzing and managing energy consumption and production.",
            content_types=['text', 'text/plain'],
        )
        self._set_up_crew()
    
    def _set_up_crew(self) -> Crew:
        get_historical_data_tool = GetHistoricalData()

        # 🧠 Agent 1: Phân tích lịch sử
        analyzer_agent = Agent(
            role="Usage Pattern Analyzer",
            goal="Analyze device usage patterns from historical data",
            backstory="An AI analyst who finds patterns in usage logs",
            tools=[get_historical_data_tool]
        )

        # 🧠 Agent 2: Lên kế hoạch tiết kiệm
        planner_agent = Agent(
            role="Energy Saving Planner",
            goal="Suggest energy-saving plans based on usage analysis",
            backstory="An expert who helps reduce electricity consumption intelligently"
        )

        # 📝 Task 1: Phân tích thói quen sử dụng
        analyze_task = Task(
            description="Use the tool to fetch device usage history and detect patterns by device and room.",
            expected_output="Summary of usage trends and repeated behaviors.",
            agent=analyzer_agent
        )

        # 📝 Task 2: Lên lịch tối ưu
        plan_task = Task(
            description="Use the output from the analysis to suggest energy-saving schedules.",
            expected_output="Recommended changes in usage schedule for LIGHT and AIR_CONDITIONER.",
            agent=planner_agent
        )

        # 👥 Tổ đội Crew
        crew = Crew(
            agents=[analyzer_agent, planner_agent],
            tasks=[analyze_task, plan_task]
        )
        self.crew = crew

    def invoke(self) -> str:
        result = self.crew.kickoff()
        return {"output": result}

if __name__ == "__main__":
    agent = EnergyAgent()
    output = agent.invoke()
    print(output)