class TimestepResult(object):
    """
    Represents the information provided to the agent after each timestep.
    """

    def __init__(self, observation, reward, is_episode_end):
        self.observation = observation
        self.reward = reward
        self.is_episode_end = is_episode_end

    def __str__(self):
        field_map = '\n'.join([
            ''.join(str(cell) for cell in row)
            for row in self.observation
        ])
        return f'{field_map}\nR = {self.reward}   end={self.is_episode_end}\n'
