from Snake import *


# Define the number of episodes to run
NUM_EPISODES = 100000000000

# Define the learning rate (alpha) and discount factor (gamma)
ALPHA = 0.5
GAMMA = 0.9

# Define the possible actions
ACTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

REWARDS = {
    "food": 1,
    "hit_wall": -1,
    "hit_body": -1,
    "normal-move": 0
}

class SnakeGameState:
    def __init__(self, snake:Snake, food:Food):
        self.snake_pos = snake.position  # position of the snake's head
        self.snake_dir = snake.direction  # direction of the snake's movement
        self.food_pos = food.position  # position of the food
        self.obstacles = snake.body  # positions of snake's body

    def is_terminal(self):
        # Check if the snake has hit a wall
        if self.snake_pos < 0 or self.snake_pos >= SCREEN_WIDTH or self.snake_pos < 0 or self.snake_pos >= SCREEN_HEIGHT:
            return True
        # Check if the snake has hit its own body
        if self.snake_pos in self.obstacles:
            return True
        return False


class DoubleQLearningSnake(Snake):
    def __init__(self, learning_rate, discount_factor):
        super().__init__(INITIAL_POSITION,INITIAL_VELOCITY)
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q1_table = {}
        self.q2_table = {}

    def get_action(self, state:SnakeGameState):
        pass

    def update(self, state:SnakeGameState, action, reward, next_state:SnakeGameState):
        pass

    def reset_snake(self):
        self.position = INITIAL_POSITION
        self.velocity = INITIAL_VELOCITY
        self.body = [self.position]
        self.direction = INITIAL_VELOCITY