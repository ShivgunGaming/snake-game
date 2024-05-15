import tkinter as tk
import random

class SnakeGame(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Snake Game")
        self.geometry("400x400")

        self.canvas = tk.Canvas(self, bg="black", width=400, height=400)
        self.canvas.pack()

        self.snake = [(20, 20), (20, 30), (20, 40)]
        self.food = self.create_food()
        self.direction = "Right"
        self.score = 0
        self.game_over_text = None

        self.bind("<KeyPress>", self.change_direction)

        self.draw()

        self.move_snake()

    def draw(self):
        self.canvas.delete("all")

        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0]+10, segment[1]+10, fill="green")

        self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0]+10, self.food[1]+10, fill="red")

        self.canvas.create_text(50, 20, text=f"Score: {self.score}", fill="white")

        if self.game_over_text:
            self.canvas.delete(self.game_over_text)
            self.game_over_text = None

        self.update()

    def create_food(self):
        x = random.randint(0, 39) * 10
        y = random.randint(0, 39) * 10
        return x, y

    def change_direction(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            self.direction = event.keysym

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == "Up":
            head_y -= 10
        elif self.direction == "Down":
            head_y += 10
        elif self.direction == "Left":
            head_x -= 10
        elif self.direction == "Right":
            head_x += 10

        new_head = (head_x, head_y)
        self.snake = [new_head] + self.snake[:-1]

        if new_head == self.food:
            self.snake.append(self.snake[-1])
            self.food = self.create_food()
            self.score += 1

        if head_x < 0 or head_x >= 400 or head_y < 0 or head_y >= 400 or new_head in self.snake[1:]:
            self.game_over()
            return

        self.draw()
        self.after(100, self.move_snake)

    def game_over(self):
        self.game_over_text = self.canvas.create_text(200, 200, text="Game Over! Press 'R' to restart", fill="white", font=("Helvetica", 14))

    def restart_game(self, event):
        self.snake = [(20, 20), (20, 30), (20, 40)]
        self.food = self.create_food()
        self.direction = "Right"
        self.score = 0
        self.draw()
        self.move_snake()

if __name__ == "__main__":
    game = SnakeGame()
    game.bind("r", game.restart_game)
    game.mainloop()
