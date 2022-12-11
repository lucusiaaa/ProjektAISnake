from Snake import *
import time
import numpy as np

# Define the learning rate (alpha) and discount factor (gamma)
ALPHA = 0.1
GAMMA = 0.9

# Define the possible actions
ACTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# Define the size of the state space
STATE_SPACE_SIZE = (SCREEN_WIDTH // BLOCK_SIZE, SCREEN_HEIGHT // BLOCK_SIZE)

# Define the Q-learning agent
class QLearningAgent:
  def __init__(self, learning_rate, discount_factor):
    # Initialize the learning rate and discount factor
    self.learning_rate = learning_rate
    self.discount_factor = discount_factor

    # Initialize the Q-table
    self.q_table = {}

  def get_action(self, state):
    # Get the Q-values for all actions in the current state
    q_values = self.q_table.get(state, [0, 0, 0, 0])

    # Select a random action with probability epsilon, otherwise select the action with the highest Q-value
    epsilon = 0.1
    if random.random() < epsilon:
      action = random.randint(0, 3)
    else:
      action = q_values.index(max(q_values))

    return action

  def update(self, state, action, reward, next_state):
    # Get the Q-value of the current state-action pair
    q_value = self.q_table.get(state, [0, 0, 0, 0])[action]

    # Calculate the TD error
    next_q_values = self.q_table.get(next_state, [0, 0, 0, 0])
    next_q_value = max(next_q_values)
    td_error = reward + self.discount_factor * next_q_value - q_value

    # Update the Q-value of the current state-action pair using the TD error
    q_values = self.q_table.get(state, [0, 0, 0, 0])
    q_values[action] += self.learning_rate * td_error
    self.q_table[state] = q_values



# Define the Q-learning snake class
class QLearningSnake:
  def __init__(self, position, velocity, q_learning_agent):
    # Initialize the snake's position and velocity
    self.position = position
    self.velocity = velocity

    # Initialize the snake's body as a list of blocks
    self.body = [self.position]

    # Initialize the snake's direction as right (1, 0)
    self.direction = (0, 0)

    # Initialize a dictionary to track the state of the keys
    self.keys = {
        pygame.K_UP: False,
        pygame.K_DOWN: False,
        pygame.K_LEFT: False,
        pygame.K_RIGHT: False
    }

    # Initialize a variable to track the time since the last input
    self.last_input_time = 0

    # Set the input repeat rate (in seconds)
    self.input_repeat_rate = 0.1

    # Save a reference to the Q-learning agent
    self.q_learning_agent = q_learning_agent

  def move(self):
    # Update the snake's direction based on the Q-learning agent's action
    state = (round(self.position[0] / BLOCK_SIZE), round(self.position[1] / BLOCK_SIZE))
    action = self.q_learning_agent.get_action(state)
    self.change_direction(action)

    # Update the snake's position based on its velocity
    x, y = self.position
    dx, dy = self.velocity
    self.position = (x + dx, y + dy)

    # Align the snake's position with the grid of blocks
    self.position = (round(self.position[0] / BLOCK_SIZE) * BLOCK_SIZE, round(self.position[1] / BLOCK_SIZE) * BLOCK_SIZE)

    # Check if the new position is within the bounds of the game screen
    if self.position[0] < 0 or self.position[0] >= SCREEN_WIDTH or self.position[1] < 0 or self.position[1] >= SCREEN_HEIGHT:
      # End the game if the snake moves off the screen
      print("Game over! You scored {} points.".format(len(self.body)))
      pygame.quit()
      quit()

    # Check if the new position is on top of the snake's body
    if self.position in self.body[1:]:
      # End the game if the snake collides with itself
      print("Game over! You scored {} points.".format(len(self.body)))
      pygame.quit()
      quit()

    # Add the new position to the front of the snake's body
    self.body.insert(0, self.position)

    # Remove the last element from the snake's body
    self.body.pop()

  def change_direction(self, direction):
    # Check if the new direction is not opposite to the current direction
    if direction != (-self.direction[0], -self.direction[1]):
      # Update the snake's direction
      self.direction = direction

      # Update the snake's velocity based on its direction
      dx, dy = self.direction
      self.velocity = (dx * BLOCK_SIZE, dy * BLOCK_SIZE)

  def draw(self, screen):
    # Draw the snake's body on the screen
    for x, y in self.body:
      # Use the pygame.draw.circle() method to draw a circle at (x, y) with a radius of BLOCK_SIZE // 2
      pygame.draw.circle(screen, (0, 255, 0), (x, y), BLOCK_SIZE // 2)

  def handle_input(self):
    # Get the current time
    current_time = pygame.time.get_ticks()

    # Check if the time since the last input is greater than the input repeat rate
    if current_time - self.last_input_time > self.input_repeat_rate * 1000:
      # Update the time of the last input
      self.last_input_time = current_time

      # Check if the up key is pressed and the snake is not moving down
      if self.keys[pygame.K_UP] and self.direction != (0, 1):
        # Change the snake's direction to up
        self.change_direction((0, -1))

      # Check if the down key is pressed and the snake is not moving up
      elif self.keys[pygame.K_DOWN] and self.direction != (0, -1):
        # Change the snake's direction to down
        self.change_direction((0, 1))

      # Check if the left key is pressed and the snake is not moving right
      elif self.keys[pygame.K_LEFT] and self.direction != (1, 0):
        # Change the snake's direction to left
        self.change_direction((-1, 0))

      # Check if the right key is pressed and the snake is not moving left
      elif self.keys[pygame.K_RIGHT] and self.direction != (-1, 0):
        # Change the snake's direction to right
        self.change_direction((1, 0))

  def update(self, screen):
    # Handle the input events
    self.handle_input()

    # Update the snake's position
    self.move()

    # Check if the snake has eaten the food
    if self.position == food.position:
      # Add a new block to the snake's body
      self.body.append(self.position)

      # Generate a new food item
      food.randomize_position()

      # Update the Q-learning agent
      state = (round(self.position[0] / BLOCK_SIZE), round(self.position[1] / BLOCK_SIZE))
      action = self.q_learning_agent.get_action(state)
      reward = len(self.body)
      next_state = (round(self.position[0] / BLOCK_SIZE), round(self.position[1] / BLOCK_SIZE))
      self.q_learning_agent.update(state, action, reward, next_state)

    # Update the display
    screen.fill(BLACK)
    self.draw(screen)
    pygame.display.update()



# Define the snake game class
class SnakeGame:
  def __init__(self):
    # Initialize the snake and food objects
    self.agent = QLearningAgent(learning_rate=0.1, discount_factor=0.9)
    self.snake = QLearningSnake(INITIAL_POSITION, INITIAL_VELOCITY,self.agent)
    self.food = Food(snake)
    self.clock = pygame.time.Clock()

  def update(self):
    # Update the snake
    self.snake.update(self.screen)

  def draw(self):
    # Update the display
    self.screen.fill(BLACK)
    self.snake.draw(self.screen)
    self.food.draw(self.screen)
    pygame.display.update()


  def handle_input(self):
    # Handle the input events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          self.snake.keys[pygame.K_UP] = True
        elif event.key == pygame.K_DOWN:
          self.snake.keys[pygame.K_DOWN] = True
        elif event.key == pygame.K_LEFT:
          self.snake.keys[pygame.K_LEFT] = True
        elif event.key == pygame.K_RIGHT:
          self.snake.keys[pygame.K_RIGHT] = True
      elif event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
          self.snake.keys[pygame.K_UP] = False
        elif event.key == pygame.K_DOWN:
          self.snake.keys[pygame.K_DOWN] = False
        elif event.key == pygame.K_LEFT:
          self.snake.keys[pygame.K_LEFT] = False
        elif event.key == pygame.K_RIGHT:
          self.snake.keys[pygame.K_RIGHT] = False

  def run(self):
    # Run the game loop
    while True:
      # Handle the input events
      self.handle_input()

      # Update the game
      self.update()

      # Draw the game
      self.draw()

      # Limit the game to 60 frames per second
      self.clock.tick(60)
