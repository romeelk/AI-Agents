from semantic_kernel.agents.strategies import  SequentialSelectionStrategy
from semantic_kernel.contents.utils.author_role import AuthorRole

import agent_constants
class SelectionStrategy(SequentialSelectionStrategy):
    async def select_agent(self, agents, history):
        """Check which agent is next in turn in the group chat"""
        if(history[-1].name == agent_constants.CODE_AGENT or history[-1].role == AuthorRole.USER):
            agent_name = agent_constants.DEPLOYMENT_AGENT
            return next((agent for agent in agents if agent.name == agent_name), None)
        return next((agent for agent in agents if agent.name == agent_constants.DEPLOYMENT_AGENT), None)