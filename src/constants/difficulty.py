""" Difficulty constants """

DIFFICULTY_EASY = 1
DIFFICULTY_MEDIUM = 2
DIFFICULTY_HARD = 3

MAX_SKULLS = {
    DIFFICULTY_EASY: 10,
    DIFFICULTY_MEDIUM: 20,
    DIFFICULTY_HARD: 30
}

SKULL_SPAWN_RANGE = {
    DIFFICULTY_EASY: (0, 100),
    DIFFICULTY_MEDIUM: (0, 75),
    DIFFICULTY_HARD: (0, 50)
}


class Difficulty:
    def __init__(self, difficulty):
        self.max_skulls = MAX_SKULLS[difficulty]
        self.skull_spawn_range = SKULL_SPAWN_RANGE[difficulty]