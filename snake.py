import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen width and height
WIDTH = 600
HEIGHT = 400

# Set up the main screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Size of each segment
SEGMENT_SIZE = 20

# Initialize game variables
score = 0
snake = [[WIDTH // 2, HEIGHT // 2]]
direction = [0, -1]  # Start with moving up
game_over = False

# Possible directions: up, down, left, right
DIRECTIONS = {
    'UP': [0, -1],
    'DOWN': [0, 1],
    'LEFT': [-1, 0],
    'RIGHT': [1, 0]
}

def draw_snake(snake_body):
    # Draw snake body segments in green
    for segment in snake_body:
        x, y = segment
        pygame.draw.rect(screen, GREEN, (x, y, SEGMENT_SIZE, SEGMENT_SIZE))

def generate_food():
    return [random.randint(0, (WIDTH // SEGMENT_SIZE) - 1) * SEGMENT_SIZE,
            random.randint(0, (HEIGHT // SEGMENT_SIZE) - 1) * SEGMENT_SIZE]

def move_snake():
    global direction
    head = snake[0]
    key = pygame.key.get_pressed()

    # Update direction based on arrow keys pressed
    if key[pygame.K_LEFT] and direction != DIRECTIONS['RIGHT']:
        direction = DIRECTIONS['LEFT']
    elif key[pygame.K_RIGHT] and direction != DIRECTIONS['LEFT']:
        direction = DIRECTIONS['RIGHT']
    elif key[pygame.K_UP] and direction != DIRECTIONS['DOWN']:
        direction = DIRECTIONS['UP']
    elif key[pygame.K_DOWN] and direction != DIRECTIONS['UP']:
        direction = DIRECTIONS['DOWN']

    # Move snake
    head = [head[0] + direction[0], head[1] + direction[1]]
    snake.insert(0, head)

def check_collision():
    head = snake[0]
    # Check if snake hits the boundaries
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        return True
    # Check if snake hits its own body
    for segment in snake[1:]:
        if head == segment:
            return True
    return False

def draw_text(string, color, size):
    font = pygame.font.Font(None, size)
    text_surface = font.render(string, True, color)
    return text_surface

# Main game loop
running = True
clock = pygame.time.Clock()
food = generate_food()

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_SPACE:  # Restart the game
                game_over = False
                snake = [[WIDTH // 2, HEIGHT // 2]]
                direction = [0, -1]
                score = 0
                food = generate_food()

    if game_over:
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))

        game_over_text = draw_text("GAME OVER", RED, 50)
        restart_text = draw_text("Press SPACE to restart", WHITE, 36)

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
    else:
        move_snake()

        if check_collision():
            game_over = True
            continue

        # Check if snake has eaten food
        # fuzzy match
        # Fuzzy match - check if snake head is within 5 coordinates of food
        head_x, head_y = snake[0]
        food_x, food_y = food
        if (abs(head_x - food_x) <= 5 and abs(head_y - food_y) <= 5):
            score += 9999
            food = generate_food()  # Generate new food after eating it
            # Add 5 new segments to the snake
            for _ in range(5):
                snake.append(snake[-1])
        else:
            snake.pop()  # Remove the tail if no food is eaten

        # Draw game elements
        draw_snake(snake)
        pygame.draw.rect(screen, RED, (food[0], food[1], SEGMENT_SIZE, SEGMENT_SIZE))

    pygame.display.flip()
    clock.tick(100)  # Reduced speed to make game playable

pygame.quit()
