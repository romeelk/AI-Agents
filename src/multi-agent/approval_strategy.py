from semantic_kernel.agents.strategies import TerminationStrategy
class ApprovalTerminationStrategy(TerminationStrategy):
    """A strategy for determining when an agent should terminate."""
    async def should_agent_terminate(self, agent, history):
     """Check if the agent should terminate."""
     return "no action needed" in history[-1].content.lower()
    