import numpy as np
import pygame

from pygame.locals import KEYDOWN, QUIT

from gui.colors import Colors
from agent.player import PlayerAgent
from gameplay.field import CellType
from gameplay.snake import SnakeActions, SnakeDirections
from utils.stopwatch import Stopwatch


class GameGUI:

    FPS_LIMIT = 60
    AI_TIMESTEP_DELAY = 100
    HUMAN_TIMESTEP_DELAY = 1000
    CELL_SIZE = 20

    SNAKE_CONTROL_KEYS = [
        pygame.K_UP,
        pygame.K_LEFT,
        pygame.K_DOWN,
        pygame.K_RIGHT
    ]

    def __init__(self):
        pygame.init()
        self.agent = PlayerAgent()
        self.env = None
        self.screen = None
        self.fps_clock = None
        self.timestep_watch = Stopwatch()

    def load_environment(self, environment):
        """
        Load the RL environment into the GUI.
        """

        self.env = environment
        screen_size = (self.env.field.size * self.CELL_SIZE,
                       self.env.field.size * self.CELL_SIZE)

        self.screen = pygame.display.set_mode(screen_size)
        self.screen.fill(Colors.SCREEN_BACKGROUND)
        pygame.display.set_caption('Snake')

    def load_agent(self, agent):
        """ Load the RL agent into the GUI. """
        self.agent = agent

    def render_cell(self, x, y):
        """
        Draw the cell specified by the field coordinates.
        """

        cell_coordinates = pygame.Rect(
            x * self.CELL_SIZE,
            y * self.CELL_SIZE,
            self.CELL_SIZE,
            self.CELL_SIZE,
        )

        if self.env.field[x, y] == CellType.EMPTY:
            pygame.draw.rect(self.screen,
                             Colors.SCREEN_BACKGROUND,
                             cell_coordinates)
        else:
            color = Colors.CELL_TYPE[self.env.field[x, y]]
            pygame.draw.rect(self.screen, color, cell_coordinates, 1)

            internal_padding = self.CELL_SIZE // 6 * 2
            internal_padding = (-internal_padding, -internal_padding)
            internal_square_coords = cell_coordinates.inflate(*internal_padding)
            pygame.draw.rect(self.screen, color, internal_square_coords)

    def render(self):
        """ Draw the entire game frame. """
        for x in range(self.env.field.size):
            for y in range(self.env.field.size):
                self.render_cell(x, y)

    def map_key_to_snake_action(self, key):
        """ Convert a keystroke to an environment action. """
        actions = [
            SnakeActions.MAINTAIN_DIRECTION,
            SnakeActions.TURN_LEFT,
            SnakeActions.MAINTAIN_DIRECTION,
            SnakeActions.TURN_RIGHT,
        ]

        ALL_SNAKE_DIRECTIONS = [
            SnakeDirections.NORTH,
            SnakeDirections.EAST,
            SnakeDirections.SOUTH,
            SnakeDirections.WEST,
        ]

        key_idx = self.SNAKE_CONTROL_KEYS.index(key)
        direction_idx = ALL_SNAKE_DIRECTIONS.index(self.env.snake.direction)
        return np.roll(actions, -key_idx)[direction_idx]

    def run(self, num_episodes=1):
        """ Run the GUI player for the specified number of episodes. """
        pygame.display.update()
        self.fps_clock = pygame.time.Clock()

        for episode in range(num_episodes):
            try:
                self.run_episode()
            except QuitRequestedError:
                break

            pygame.time.wait(1500)

    def run_episode(self):
        """ Run the GUI player for a single episode. """

        timestep_result = self.initialize_env()
        is_human_agent = isinstance(self.agent, PlayerAgent)
        timestep_delay = self.get_timestep_delay(is_human_agent)

        default_action = SnakeActions.MAINTAIN_DIRECTION

        while True:
            action = default_action

            for event in pygame.event.get():
                print('Event ', event.type)

                if event.type == KEYDOWN:
                    if is_human_agent and event.key in self.SNAKE_CONTROL_KEYS:
                        action = self.map_key_to_snake_action(event.key)
                    if event.key == pygame.K_ESCAPE:
                        raise QuitRequestedError

                if event.type == QUIT:
                    raise QuitRequestedError

            # Update game state.
            timestep_timed_out = self.timestep_watch.time() >= timestep_delay
            human_made_move = is_human_agent and action != default_action

            if timestep_timed_out or human_made_move:
                self.timestep_watch.reset()

                if not is_human_agent:
                    action = self.agent.next_action(timestep_result.observation,
                                                    timestep_result.reward)

                self.env.choose_action(action)
                timestep_result = self.env.timestep()

                if timestep_result.is_episode_end:
                    self.agent.end_episode()
                    break

            self.render_scene()

    def initialize_env(self):
        """ Initialize environment for new session. """
        self.timestep_watch.reset()
        timestep_result = self.env.new_episode()
        self.agent.reset_state()

        return timestep_result

    def get_timestep_delay(self, is_human_agent):
        if is_human_agent:
            return self.HUMAN_TIMESTEP_DELAY
        else:
            return self.AI_TIMESTEP_DELAY

    def render_scene(self):
        """ Render current scene. """
        self.render()
        score = self.env.snake.length - self.env.initial_snake_length
        pygame.display.set_caption(f'Snake  [Score: {score:02d}]')
        pygame.display.update()
        self.fps_clock.tick(self.FPS_LIMIT)


class QuitRequestedError(RuntimeError):
    """ Gets raised whenever the user wants to quit the game. """
    pass
