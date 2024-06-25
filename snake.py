import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake Game")

# Define colors
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

# Define snake properties
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_direction = 'RIGHT'
change_to = snake_direction

# Define food properties
food_pos = [random.randrange(1, 80) * 10, random.randrange(1, 60) * 10]
food_spawn = True

# Set game speed
clock = pygame.time.Clock()
snake_speed = 15

# Font for displaying the score and game-over message
font = pygame.font.SysFont('arial', 35)
small_font = pygame.font.SysFont('arial', 25)

def show_score():
    score = font.render(f'Score: {len(snake_body) - 3}', True, white)
    screen.blit(score, [0, 0])

def game_over():
    message = font.render('Game Over', True, red)
    screen.fill(black)
    screen.blit(message, [screen.get_width() // 2 - message.get_width() // 2, screen.get_height() // 2 - message.get_height() // 2])
    
    restart_button = small_font.render('Restart', True, white)
    restart_rect = restart_button.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
    pygame.draw.rect(screen, blue, restart_rect.inflate(20, 10))
    screen.blit(restart_button, restart_rect)
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return  # Exit the function to restart the game

def reset_game():
    global snake_pos, snake_body, snake_direction, change_to, food_pos, food_spawn
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    snake_direction = 'RIGHT'
    change_to = snake_direction
    food_pos = [random.randrange(1, 80) * 10, random.randrange(1, 60) * 10]
    food_spawn = True

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Validate the direction
    if change_to == 'UP' and not snake_direction == 'DOWN':
        snake_direction = change_to
    if change_to == 'DOWN' and not snake_direction == 'UP':
        snake_direction = change_to
    if change_to == 'LEFT' and not snake_direction == 'RIGHT':
        snake_direction = change_to
    if change_to == 'RIGHT' and not snake_direction == 'LEFT':
        snake_direction = change_to

    # Update the position of the snake
    if snake_direction == 'UP':
        snake_pos[1] -= 10
    if snake_direction == 'DOWN':
        snake_pos[1] += 10
    if snake_direction == 'LEFT':
        snake_pos[0] -= 10
    if snake_direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        food_spawn = False
    else:
        snake_body.pop()

    # Spawn food
    if not food_spawn:
        food_pos = [random.randrange(1, 80) * 10, random.randrange(1, 60) * 10]
    food_spawn = True

    # Fill the screen with a color (black)
    screen.fill(black)

    # Draw the snake
    for pos in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Draw the food
    pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Check for collisions with walls
    if snake_pos[0] < 0 or snake_pos[0] > 790 or snake_pos[1] < 0 or snake_pos[1] > 590:
        game_over()
        reset_game()

    # Check for collisions with itself
    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()
            reset_game()

    # Show score
    show_score()

    # Update the display
    pygame.display.flip()

    # Control the game speed
    clock.tick(snake_speed)

# Quit Pygame
pygame.quit()
sys.exit()
