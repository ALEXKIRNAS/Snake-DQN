from agent.base import BaseAgent
from gameplay.snake import SnakeActions


class PlayerAgent(BaseAgent):
    """
    Represents an agent that is operated by a human (can be used by the GUI).
    """

    def next_action(self, observation, reward):
        return SnakeActions.MAINTAIN_DIRECTION
