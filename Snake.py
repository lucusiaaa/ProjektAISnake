import random
import pygame

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define the screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 400

# Define the snake block size
BLOCK_SIZE = 20

# Define the initial position and velocity of the snake
INITIAL_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
INITIAL_VELOCITY = (0, 0)

# Define the maximum number of time steps
MAX_TIME_STEPS = 10000

# Initialize the pygame library
pygame.init()

# Create the game screen
screen = pygame.display.set_mode((700, 700))

# Set the title and background color of the game screen
pygame.display.set_caption("Snake")
screen.fill(BLACK)

# Define the snake class
class Snake:
  def __init__(self, position, velocity):
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

  def move(self):
    # Update the snake's position based on its velocity
    x, y = self.position
    dx, dy = self.velocity
    self.position = (x + dx, y + dy)

    # Align the snake's position with the grid of blocks
    self.position = (round(self.position[0] / BLOCK_SIZE) * BLOCK_SIZE, round(self.position[1] / BLOCK_SIZE) * BLOCK_SIZE)

    # Check if the new position is within the bounds of the game screen
    if __name__ == "__main__":
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


# Define the food class
class Food:
  def __init__(self, snake):
      self.place_food(snake)

  def place_food(self, snake):
    # Generate a random x and y position within the bounds of the game screen
    x = random.randint(0, SCREEN_WIDTH - BLOCK_SIZE)
    y = random.randint(0, SCREEN_HEIGHT - BLOCK_SIZE)

    # Align the food position with the grid of blocks
    self.position = (round(x / BLOCK_SIZE) * BLOCK_SIZE, round(y / BLOCK_SIZE) * BLOCK_SIZE)

    # Check if the new position is on top of the snake's body
    if self.position in snake.body:
      # Place the food at a different position if it is on top of the snake's body
      self.place_food(snake)

  def draw(self, screen):
    # Use the pygame.draw.circle() method to draw a circle at the food's position with a radius of BLOCK_SIZE // 2
    pygame.draw.circle(screen, (255, 0, 0), self.position, BLOCK_SIZE // 2)


if __name__ == "__main__":
  # Create the snake and food objects
  snake = Snake(INITIAL_POSITION, INITIAL_VELOCITY)
  food = Food(snake)

  # Create the game clock
  clock = pygame.time.Clock()

  # Play the game for a specified number of time steps
  for t in range(MAX_TIME_STEPS):
    # Process the events in the game
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        # End the game if the player closes the window
        print("Game over! You scored {} points.".format(len(snake.body)))
        pygame.quit()
        quit()

    # Update the snake's direction based on the user input
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        snake.change_direction((-1, 0))
      elif event.key == pygame.K_RIGHT:
        snake.change_direction((1, 0))
      elif event.key == pygame.K_UP:
        snake.change_direction((0, -1))
      elif event.key == pygame.K_DOWN:
        snake.change_direction((0, 1))

    # Update the snake and food objects
    snake.move()
    if snake.position == food.position:
        # Create a new food object at a random position
        food = Food(snake)
        snake.body.append(snake.position)

    # Clear the screen
    screen.fill(BLACK)

    # Draw the snake and food on the screen
    snake.draw(screen)
    food.draw(screen)

    # Update the game screen
    pygame.display.update()

    # Limit the frame rate to 30 FPS
    clock.tick(15)
