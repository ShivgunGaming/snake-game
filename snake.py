import pygame
import time
import random
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SNAKE_BLOCK = 10
INITIAL_SNAKE_SPEED = 15
SPEED_INCREMENT = 1
HIGH_SCORE_FILE = "high_score.txt"
LEVEL_UP_SCORE = 5
FINAL_LEVEL = 5

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Set up the display
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# Clock
clock = pygame.time.Clock()

# Font style
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, 'r') as file:
            return int(file.read())
    return 0

def save_high_score(high_score):
    with open(HIGH_SCORE_FILE, 'w') as file:
        file.write(str(high_score))

def message(msg, color, position):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, position)

def display_score(score, high_score, level):
    value = score_font.render("Your Score: " + str(score), True, YELLOW)
    high_value = score_font.render("High Score: " + str(high_score), True, YELLOW)
    level_value = score_font.render("Level: " + str(level), True, YELLOW)
    display.blit(value, [0, 0])
    display.blit(high_value, [0, 35])
    display.blit(level_value, [0, 70])

def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(display, WHITE, [x[0], x[1], snake_block, snake_block])

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(display, RED, obstacle)

def generate_food():
    return round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0, round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

def main_menu():
    menu = True
    while menu:
        display.fill(BLUE)
        
        # Title
        title_font = pygame.font.SysFont(None, 80)
        title_text = title_font.render("Snake Game", True, YELLOW)
        display.blit(title_text, (SCREEN_WIDTH / 2 - title_text.get_width() / 2, SCREEN_HEIGHT / 3 - title_text.get_height()))
        
        # Menu options
        menu_font = pygame.font.SysFont(None, 40)
        start_text = menu_font.render("Press S to Start", True, WHITE)
        high_scores_text = menu_font.render("Press H for High Scores", True, WHITE)
        quit_text = menu_font.render("Press Q to Quit", True, WHITE)
        
        display.blit(start_text, (SCREEN_WIDTH / 2 - start_text.get_width() / 2, SCREEN_HEIGHT / 2))
        display.blit(high_scores_text, (SCREEN_WIDTH / 2 - high_scores_text.get_width() / 2, SCREEN_HEIGHT / 2 + 50))
        display.blit(quit_text, (SCREEN_WIDTH / 2 - quit_text.get_width() / 2, SCREEN_HEIGHT / 2 + 100))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_s:
                    game_loop()
                if event.key == pygame.K_h:
                    display_high_scores()

def display_high_scores():
    high_score = load_high_score()
    display.fill(BLUE)
    message("High Scores", YELLOW, [SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 3])
    message(f"High Score: {high_score}", WHITE, [SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2])
    message("Press B to go Back", WHITE, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 1.5])
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    main_menu()

def game_loop():
    game_over = False
    game_close = False
    game_paused = False

    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx, foody = generate_food()

    score = 0
    high_score = load_high_score()
    snake_speed = INITIAL_SNAKE_SPEED
    level = 1
    obstacles = []

    while not game_over:

        while game_close:
            display.fill(BLUE)
            message("You Lost!", RED, [SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 3])
            message(f"Score: {score}", WHITE, [SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2])
            message(f"High Score: {high_score}", WHITE, [SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 50])
            message("Press C to Play Again", WHITE, [SCREEN_WIDTH / 3, SCREEN_HEIGHT / 1.5])
            message("Press M for Main Menu", WHITE, [SCREEN_WIDTH / 3, SCREEN_HEIGHT / 1.5 + 50])
            
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        game_loop()
                    elif event.key == pygame.K_m:
                        main_menu()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_p:
                    game_paused = not game_paused
        
        if game_paused:
            message("Game Paused! Press P to Resume", RED, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3])
            pygame.display.update()
            continue

        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        display.fill(BLACK)
        pygame.draw.rect(display, GREEN, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(SNAKE_BLOCK, snake_List)
        draw_obstacles(obstacles)
        display_score(score, high_score, level)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food()
            Length_of_snake += 1
            score += 1
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            snake_speed += SPEED_INCREMENT

            if score % LEVEL_UP_SCORE == 0 and level < FINAL_LEVEL:
                level += 1
                for _ in range(level):  # Add more obstacles as the level increases
                    obstacles.append([round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0,
                                      round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0,
                                      SNAKE_BLOCK, SNAKE_BLOCK])

        for obstacle in obstacles:
            if x1 == obstacle[0] and y1 == obstacle[1]:
                game_close = True

        clock.tick(snake_speed)

    pygame.quit()
    quit()

main_menu()
