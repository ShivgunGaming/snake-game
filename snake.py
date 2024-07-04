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
POWER_UP_DURATION = 10000  # 10 seconds

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
PURPLE = (128, 0, 128)

# Set up the display
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# Clock
clock = pygame.time.Clock()

# Font style
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)


class Snake:
    def __init__(self):
        self.length = 1
        self.speed = INITIAL_SNAKE_SPEED
        self.body = [[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]]
        self.direction = [0, 0]

    def move(self):
        head = self.body[-1].copy()
        head[0] += self.direction[0]
        head[1] += self.direction[1]
        self.body.append(head)
        if len(self.body) > self.length:
            self.body.pop(0)

    def change_direction(self, direction):
        if direction == 'LEFT' and self.direction[0] == 0:
            self.direction = [-SNAKE_BLOCK, 0]
        elif direction == 'RIGHT' and self.direction[0] == 0:
            self.direction = [SNAKE_BLOCK, 0]
        elif direction == 'UP' and self.direction[1] == 0:
            self.direction = [0, -SNAKE_BLOCK]
        elif direction == 'DOWN' and self.direction[1] == 0:
            self.direction = [0, SNAKE_BLOCK]

    def grow(self):
        self.length += 1

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(display, WHITE, [segment[0], segment[1], SNAKE_BLOCK, SNAKE_BLOCK])

    def check_collision(self):
        head = self.body[-1]
        if head[0] >= SCREEN_WIDTH or head[0] < 0 or head[1] >= SCREEN_HEIGHT or head[1] < 0:
            return True
        if head in self.body[:-1]:
            return True
        return False


class Food:
    def __init__(self):
        self.position = self.generate_position()

    def generate_position(self):
        return [
            round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0,
            round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
        ]

    def draw(self):
        pygame.draw.rect(display, GREEN, [self.position[0], self.position[1], SNAKE_BLOCK, SNAKE_BLOCK])


class PowerUp:
    def __init__(self):
        self.position = self.generate_position()
        self.active = True
        self.start_time = 0

    def generate_position(self):
        return [
            round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0,
            round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
        ]

    def draw(self):
        if self.active:
            pygame.draw.rect(display, PURPLE, [self.position[0], self.position[1], SNAKE_BLOCK, SNAKE_BLOCK])

    def activate(self):
        self.active = False
        self.start_time = pygame.time.get_ticks()

    def check_duration(self):
        if not self.active and (pygame.time.get_ticks() - self.start_time > POWER_UP_DURATION):
            self.position = self.generate_position()
            self.active = True


class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.power_up = PowerUp()
        self.score = 0
        self.high_score = self.load_high_score()
        self.level = 1
        self.obstacles = []
        self.paused = False

    def load_high_score(self):
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, 'r') as file:
                return int(file.read())
        return 0

    def save_high_score(self):
        with open(HIGH_SCORE_FILE, 'w') as file:
            file.write(str(self.high_score))

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            pygame.draw.rect(display, RED, obstacle)

    def add_obstacles(self):
        for _ in range(self.level):  # Add more obstacles as the level increases
            self.obstacles.append([round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0,
                                   round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0,
                                   SNAKE_BLOCK, SNAKE_BLOCK])

    def display_score(self):
        value = score_font.render("Your Score: " + str(self.score), True, YELLOW)
        high_value = score_font.render("High Score: " + str(self.high_score), True, YELLOW)
        level_value = score_font.render("Level: " + str(self.level), True, YELLOW)
        display.blit(value, [0, 0])
        display.blit(high_value, [0, 35])
        display.blit(level_value, [0, 70])

    def display_message(self, msg, color, position):
        mesg = font_style.render(msg, True, color)
        display.blit(mesg, position)

    def game_over_screen(self):
        display.fill(BLUE)
        self.display_message("You Lost!", RED, [SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 3])
        self.display_message(f"Score: {self.score}", WHITE, [SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2])
        self.display_message(f"High Score: {self.high_score}", WHITE, [SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 50])
        self.display_message("Press C to Play Again", WHITE, [SCREEN_WIDTH / 3, SCREEN_HEIGHT / 1.5])
        self.display_message("Press M for Main Menu", WHITE, [SCREEN_WIDTH / 3, SCREEN_HEIGHT / 1.5 + 50])
        pygame.display.update()

    def main_menu(self):
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
                        self.reset_game()
                        self.game_loop()
                    if event.key == pygame.K_h:
                        self.display_high_scores()

    def display_high_scores(self):
        display.fill(BLUE)
        self.display_message("High Score", YELLOW, [SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 3])
        self.display_message(f"High Score: {self.high_score}", WHITE, [SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2])
        self.display_message("Press B to go Back", WHITE, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 1.5])
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        self.main_menu()

    def pause_menu(self):
        while self.paused:
            display.fill(BLUE)
            self.display_message("Game Paused", WHITE, [SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 3])
            self.display_message("Press R to Resume", WHITE, [SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2])
            self.display_message("Press M for Main Menu", WHITE, [SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2 + 50])
            self.display_message("Press Q to Quit", WHITE, [SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2 + 100])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.paused = False
                    if event.key == pygame.K_m:
                        self.paused = False
                        self.main_menu()
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()

    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.power_up = PowerUp()
        self.score = 0
        self.level = 1
        self.obstacles = []
        self.paused = False

    def game_loop(self):
        game_over = False

        while not game_over:
            while self.snake.check_collision():
                self.game_over_screen()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            self.reset_game()
                            self.game_loop()
                        elif event.key == pygame.K_m:
                            self.main_menu()
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.snake.change_direction('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction('RIGHT')
                    elif event.key == pygame.K_UP:
                        self.snake.change_direction('UP')
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction('DOWN')
                    elif event.key == pygame.K_p:
                        self.paused = True
                        self.pause_menu()

            if self.paused:
                continue

            self.snake.move()
            if self.snake.body[-1] == self.food.position:
                self.food.position = self.food.generate_position()
                self.snake.grow()
                self.score += 1
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
                self.snake.speed += SPEED_INCREMENT

                if self.score % LEVEL_UP_SCORE == 0 and self.level < FINAL_LEVEL:
                    self.level += 1
                    self.add_obstacles()

            if self.snake.body[-1] == self.power_up.position:
                self.power_up.activate()
                self.snake.speed += 5  # Speed boost

            self.power_up.check_duration()

            for obstacle in self.obstacles:
                if self.snake.body[-1] == obstacle[:2]:
                    game_over = True

            display.fill(BLACK)
            self.food.draw()
            self.power_up.draw()
            self.snake.draw()
            self.draw_obstacles()
            self.display_score()
            pygame.display.update()

            clock.tick(self.snake.speed)

        pygame.quit()
        quit()


if __name__ == "__main__":
    game = Game()
    game.main_menu()
