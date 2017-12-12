class BaseAgent(object):
    """ Represents an intelligent agent for the Snake environment. """

    def reset_state(self):
        """ Reset the agent for a new episode. """
        pass

    def next_action(self, observation, reward):
        """
        Choose the next action to take.
        Args:
            observation: observable state for the current timestep.
            reward: reward received at the beginning of the current timestep.
        Returns:
            The index of the action to take next.
        """
        pass

    def end_episode(self):
        """ Notify the agent that the episode has ended. """
        pass
