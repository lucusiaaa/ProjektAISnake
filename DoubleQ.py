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
        if self.snake_pos[0] < 0 or self.snake_pos[0] >= SCREEN_WIDTH or self.snake_pos[1] < 0 or self.snake_pos[1] >= SCREEN_HEIGHT:
            return True
        # Check if the snake has hit its own body
        if self.snake_pos in self.obstacles[2:]:
            return True
        return False

    def get_reward(self):
        if self.is_terminal():
            if self.snake_pos in self.obstacles[2:]:
                return REWARDS["hit_body"]
            else:
                return REWARDS["hit_wall"]
        if self.snake_pos == self.food_pos:
            return REWARDS["food"]
        return REWARDS["normal-move"]

class DoubleQLearningSnake(Snake):
    def __init__(self, learning_rate, discount_factor):
        super().__init__(INITIAL_POSITION,INITIAL_VELOCITY)
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q1_table = {}
        self.q2_table = {}

    def get_action(self, state: SnakeGameState):
        # Choose the best action to take in the given state according to the Q-tables
        best_q1 = max(self.q1_table.get((state, action), 0) for action in ACTIONS)
        best_q2 = max(self.q2_table.get((state, action), 0) for action in ACTIONS)
        best_q = max(best_q1, best_q2)
        # Randomly choose one of the actions with the highest Q-value
        best_actions = [action for action in ACTIONS if
                        self.q1_table.get((state, action), 0) == best_q or self.q2_table.get((state, action),
                                                                                             0) == best_q]
        return random.choice(best_actions)

    def update(self, state: SnakeGameState, action, reward, next_state: SnakeGameState):
        pass
        #TODO: naprawić ten syf
        # # Choose the best action to take in the next state according to the two Q-tables
        # next_action = self.get_action(next_state)
        # # Update the Q-value in the first Q-table using the Q-value in the second Q-table
        # self.q1_table[(state, action)] = (1 - self.learning_rate) * self.q1_table.get((state, action), 0) + \
        #                                  self.learning_rate * (reward + self.discount_factor * self.q2_table[
        #     (next_state, next_action)])
        # # Update the Q-value in the second Q-table using the Q-value in the first Q-table
        # self.q2_table[(state, action)] = (1 - self.learning_rate) * self.q2_table.get((state, action), 0) + \
        #                                  self.learning_rate * (reward + self.discount_factor * self.q1_table[
        #     (next_state, next_action)])

    def reset_snake(self):
        self.position = INITIAL_POSITION
        self.velocity = INITIAL_VELOCITY
        self.body = [self.position]
        self.direction = INITIAL_VELOCITY

class SnakeGame:

    def run(self):
        # Create the game clock
        clock = pygame.time.Clock()
        # Create the snake and food objects
        snake = DoubleQLearningSnake(ALPHA, GAMMA)

        for i in range(NUM_EPISODES):
            snake.reset_snake()
            food = Food(snake)
            gameState = SnakeGameState(snake,food)


            # Play the game for a specified number of time steps
            for t in range(MAX_TIME_STEPS):
                # Process the events in the game
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # End the game if the user closes the window
                        pygame.quit()
                        quit()

                # Update the snake's direction based on AI chosen action
                snake.change_direction(snake.get_action(gameState))

                # Update the snake and food objects
                snake.move()
                if snake.position == food.position:
                    # Create a new food object at a random position
                    food = Food(snake)
                    snake.body.append(snake.position)

                new_state = SnakeGameState(snake,food)

                snake.update(gameState,snake.get_action(gameState),gameState.get_reward(),new_state)

                # Clear the screen
                screen.fill(BLACK)
                # Draw the snake and food on the screen
                snake.draw(screen)
                food.draw(screen)
                # Update the game screen
                pygame.display.update()
                # Limit the frame rate to 30 FPS
                clock.tick(15)

snakeGame = SnakeGame()
snakeGame.run()