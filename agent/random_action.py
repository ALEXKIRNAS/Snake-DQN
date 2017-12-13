import random

from agent.base import BaseAgent
from gameplay.snake import ALL_SNAKE_ACTIONS


class RandomAgent(BaseAgent):
    """
    Represents an agent that is operated by a human (can be used by the GUI).
    """

    def next_action(self, observation, reward):
        return random.choice(ALL_SNAKE_ACTIONS)
