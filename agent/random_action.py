import random

from .base import BaseAgent
from ..gameplay.snake import SnakeActions


class PlayerAgent(BaseAgent):
    """
    Represents an agent that is operated by a human (can be used by the GUI).
    """

    def __init__(self):
        self.ALL_SNAKE_ACTIONS = [
            SnakeActions.TURN_LEFT,
            SnakeActions.TURN_RIGHT,
            SnakeActions.MAINTAIN_DIRECTION,
        ]

    def next_action(self, observation, reward):
        return random.choice(self.ALL_SNAKE_ACTIONS)
