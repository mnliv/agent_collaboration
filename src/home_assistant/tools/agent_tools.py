from agents.energy_agent import EnergyAgent

class AgentTools:

    agent = EnergyAgent()

    @classmethod
    def analyze_energy_usage(cls):
        """
        Analyze energy usage data to identify patterns and anomalies.

        """
        output = cls.agent.invoke()
        return output

        