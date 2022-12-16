import copy

from DoubleQ import *


class NStepQLearningSnake(Snake):
    def __init__(self, learning_rate, discount_factor, N=3):
        super().__init__(INITIAL_POSITION, INITIAL_VELOCITY)
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q_table = [[0 for action in ACTIONS] for state in range(pow(2, 11))]
        self.n_steps = N

    def get_action(self, state: SnakeGameState):
        # Choose the best action to take in the given state according to the Q-tables
        best_q = max(self.q_table[state.state_representation()][action] for action in ACTIONS)
        best_q = max(best_q)
        # Randomly choose one of the actions with the highest Q-value
        best_actions = [action for action in ACTIONS if
                        self.q_table[state.state_representation()][action] == best_q]
        return random.choice(best_actions)

    def get_greedy_action(self, state: SnakeGameState):
        # Choose the best action to take in the given state according to the Q-tables
        best_q = max(self.q_table[state.state_representation()][action] for action in ACTIONS)
        best_actions = [action for action in ACTIONS if self.q_table[state.state_representation()][action] == best_q]
        return random.choice(best_actions)

    def update(self, state: SnakeGameState, action, reward, next_state):
        # Get the Q-value of the next state-action pair
        next_q = self.q_table[next_state.state_representation()][self.get_greedy_action(next_state)]

        # Initialize the N-step return as the immediate reward
        n_step_return = reward

        # Initialize the list of state-action pairs
        state_action_pairs = [(state, action)]

        # Initialize the current state and action to the next state and action
        cur_state, cur_action = next_state, self.get_greedy_action(next_state)

        # Iterate over the remaining N-1 steps
        for _ in range(self.n_steps - 1):
            # Get the next state and action
            next_state, next_action = self.get_next_state_and_action(cur_state, cur_action)
            # Add the state-action pair to the list
            state_action_pairs.append((cur_state, cur_action))
            # Update the N-step return
            n_step_return = n_step_return + self.discount_factor * next_q
            # Update the current state and action
            cur_state, cur_action = next_state, next_action

        # Iterate over the state-action pairs in reverse order
        for state, action in state_action_pairs[::-1]:
            # Update the Q-value of the state-action pair
            q_value = self.q_table[state.state_representation()][action]
            self.q_table[state.state_representation()][action] = q_value + self.learning_rate * (
                        n_step_return - q_value)
            # Update the N-step return
            n_step_return = n_step_return - reward
            n_step_return = n_step_return / self.discount_factor

    def get_next_state_and_action(self, state: SnakeGameState, action):
        # Create a copy of the snake
        snakeCopy = copy.copy(self)
        # Update the position and velocity of the snake copy based on the action
        snakeCopy.change_direction(action)
        snakeCopy.move()
        # Create a state representing next game state
        if self.position[0] == state.food_pos[0] and self.position[1] == state.food_pos[1]:
            next_state = NStepSnakeGameState(snakeCopy,(0,0))
        else:
            next_state = NStepSnakeGameState(snakeCopy,state.food_pos)
        # Choose the best action to take in the next state according to the two Q-tables
        next_action = snakeCopy.get_greedy_action(next_state)
        return next_state, next_action

    def reset_snake(self):
        self.position = INITIAL_POSITION
        self.velocity = INITIAL_VELOCITY
        self.body = [self.position]
        self.direction = INITIAL_VELOCITY

class NStepSnakeGameState(SnakeGameState):
    def __init__(self, snake: Snake, food_position):
        self.snake_pos = snake.position  # position of the snake's head
        self.snake_dir = snake.direction  # direction of the snake's movement
        self.food_pos = food_position  # position of the food
        self.obstacles = snake.body  # positions of snake's body

nStepSnake = NStepQLearningSnake(ALPHA,GAMMA)
snakeGame = SnakeGame(nStepSnake)
snakeGame.run()